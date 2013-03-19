#===============================================================================
# node.py
#
#
#
#===============================================================================
import os, sys
from PyQt4 import QtCore


from global_vars import app_global_vars, DEBUG_MODE
from core.node_global_vars import node_global_vars

#from core.nodeParam import NodeParam
#
# Node
#
class Node ( QtCore.QObject ):
  id = 0
  #
  #
  def __init__ ( self, xml_node = None ):
    #
    QtCore.QObject.__init__( self )

    self.id = None
    self.name = None
    self.label = None
    self.type = None

    self.author = None
    self.help = None
    self.icon = None

    self.master = None

    self.code = None
    self.param_code = None
    self.computed_code = None

    self.computedInputParams = None
    self.computedOutputParams = None
    self.computedLocalParams = None
    self.computedIncludes = None
    self.computedLocals = None
    self.computedCode = None

    #self.previewCode = None

    self.inputParams = []
    self.outputParams = []
    self.internals = []
    self.includes = []

    self.inputLinks = {}
    self.outputLinks = {}

    self.childs = set()

    # position from GfxNode
    self.offset = ( 0, 0 )

    if xml_node != None :
      self.parseFromXML ( xml_node )
  #
  #
  @classmethod
  def build ( cls ):
    node = cls ()
    # set unique id while building
    Node.id += 1
    node.id = Node.id
    return node
  #
  #
  def copy ( self ) : assert 0, 'copy needs to be implemented!'
  #
  #
  def addInputParam ( self, param ) :
    param.isInput = True
    # to be sure that name and label is unique
    if param.name in self.getParamsNames () : self.renameParamName ( param, param.name )
    if param.label in self.getParamsLabels () : self.renameParamLabel ( param, param.label )
    self.inputParams.append ( param )
  #
  #
  def addOutputParam ( self, param ) :
    param.isInput = False
    # to be sure that name and label is unique
    if param.name in self.getParamsNames () : self.renameParamName ( param, param.name )
    if param.label in self.getParamsLabels () : self.renameParamLabel ( param, param.label )
    self.outputParams.append ( param )
  #
  #
  def addInternal ( self, newName ) :
    #print '--> add internal: %s' % internal
    internal = newName
    if internal != '' :
      from meCommon import getUniqueName
      internal = getUniqueName ( newName, self.internals )
      self.internals.append ( internal )
    return internal
  #
  #
  def addInclude ( self, newName ) :
    #print '--> add include: %s' % include
    include = newName
    if include != '' :
      from meCommon import getUniqueName
      include = getUniqueName ( newName, self.includes )
      self.includes.append ( include )
    return include
  #
  #
  def attachOutputParamToLink ( self, param, link ):
    if not param in self.outputLinks.keys():
      self.outputLinks[ param ] = []
    self.outputLinks[ param ].append ( link )
  #
  #
  def detachOutputParamFromLink ( self, param, link ):
    if param in self.outputLinks.keys() :
      outputLinks = self.outputLinks[ param ]
      if link in outputLinks :
        outputLinks.remove ( link )
  #
  #
  def attachInputParamToLink ( self, param, link ):
    self.inputLinks[ param ] = link
  #
  #
  def detachInputParamFromLink ( self, param ):
    if param in self.inputLinks.keys() :
      self.inputLinks.pop ( param )
  #
  #
  def isInputParamLinked ( self, param ):
    return param in self.inputLinks.keys()
  #
  #
  def isOutputParamLinked ( self, param ):
    return param in self.outputLinks.keys()
  #
  # getLinkedSrcNode
  #
  # returns node linked to input parameter param,
  # skipping all ConnectorNode
  #
  def getLinkedSrcNode ( self, param ):
    if DEBUG_MODE : print '* getLinkedSrcNode node = %s param = %s' % ( self.label, param.label )
    srcNode = None
    srcParam = None
    if self.isInputParamLinked ( param ) :
      if DEBUG_MODE : print '* isInputParamLinked'
      link = self.inputLinks [ param ]
      if link.srcNode.type == 'connector' :
        if len ( link.srcNode.inputParams ) :
          firstParam = link.srcNode.inputParams [ 0 ]
          ( srcNode, srcParam ) = link.srcNode.getLinkedSrcNode ( firstParam )
        else :
          if DEBUG_MODE : print '* no inputParams at connector %s' % ( link.srcNode.label )  
      else :
        srcNode = link.srcNode  
        srcParam = link.srcParam
    return ( srcNode, srcParam )
  #
  #
  def removeParam ( self, param ):
    if param.isInput :
      if self.isInputParamLinked ( param ) :
        self.detachInputParamFromLink ( param )
      self.inputParams.remove ( param )
    else :
      if self.isOutputParamLinked ( param ) :
        while param in self.outputLinks.keys() :
          self.outputLinks.pop ( param )
      self.outputParams.remove ( param )
  #
  #
  def getInputParamByName ( self, name ):
    result = None
    for param in self.inputParams :
      if param.name == name :
        result = param
        break
    return result
  #
  # getOutputParamByName
  #
  def getOutputParamByName ( self, name ):
    result = None
    for param in self.outputParams :
      if param.name == name :
        result = param
        break
    return result
  #
  # getInputParamValueByName
  #
  def getInputParamValueByName ( self, name ):
    #
    result = None
    srcNode = srcParam = None
    param = self.getInputParamByName ( name )
    ( srcNode, srcParam ) = self.getLinkedSrcNode ( param )
    if srcNode is not None :
      srcNode.computeNode ()
      if self.computed_code is not None :
        self.computed_code += srcNode.computed_code
      result = srcNode.parseGlobalVars ( srcParam.getValueToStr () )
    else :
      result = param.getValueToStr ()

    return result
  #
  # return common list for input and output parameters
  #
  def getParamsList ( self ) :
    params = self.inputParams + self.outputParams
    return params
  #
  # getParamsNames
  #
  def getParamsNames ( self ) :
    names = []
    for pm in self.getParamsList () : names.append ( pm.name )
    return names
  #
  # getParamsLabels
  #
  def getParamsLabels ( self ) :
    labels = []
    for pm in self.getParamsList () : labels.append ( pm.label )
    return labels
  #
  # renameParamName
  #
  def renameParamName ( self, param, newName ):
    # assign new unique name to param
    from meCommon import getUniqueName
    param.name = getUniqueName ( newName, self.getParamsNames() )
    return param.name
  #
  # renameParamLabel
  #
  def renameParamLabel ( self, param, newName ):
    # assign new unique label to param
    from meCommon import getUniqueName
    param.label = getUniqueName ( newName, self.getParamsLabels() )
    return param.label
  #
  # onParamChanged
  #
  def onParamChanged ( self, param ):
    if DEBUG_MODE : print ">> Node: onParamChanged node = %s param = %s" % ( self.label, param.name )
    pass
    #self.emit( QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self, param )
  #
  # getLabel
  #
  def getLabel ( self ) : return self.label
  #
  # getName
  #
  def getName ( self ) : return self.label
  #
  # getInstanceName
  #
  def getInstanceName ( self ) : return self.label
  #
  # getParamName
  #
  def getParamName ( self, param ):
    result = param.name
    if not ( param.provider == 'primitive' or param.isRibParam ) :
      result = self.getInstanceName () + '_' + param.name
    return result
  #
  # getParamDeclaration
  #
  def getParamDeclaration ( self, param ) :
    result = ''
    result += param.typeToStr() + ' '
    result += self.getParamName ( param ) + ' = '
    result += param.getValueToStr() + ';\n'
    return result
  #
  # parseFromXML
  #
  def parseFromXML ( self, xml_node ) :
    #
    id_node = xml_node.attributes ().namedItem ( 'id' )
    if not id_node.isNull () :
      self.id = int ( id_node.nodeValue () )
    else :
      if DEBUG_MODE : print '>> Node::parseFromXML id is None'

    self.name = str ( xml_node.attributes ().namedItem ( 'name' ).nodeValue () )
    self.label = str ( xml_node.attributes ().namedItem ( 'label' ).nodeValue () )
    if self.label == '' : self.label = self.name
    #print '-> parsing from XML node name= %s label= %s' % ( self.name, self.label )

    self.author = str ( xml_node.attributes ().namedItem ( 'author' ).nodeValue () )
    self.type = str ( xml_node.attributes ().namedItem ( 'type' ).nodeValue () )

    help_tag = xml_node.namedItem ( 'help' )
    if not help_tag.isNull() :
      self.help = help_tag.toElement ().text ()
      #print '-> help= %s' % self.help
    self.icon = str ( xml_node.attributes ().namedItem ( 'icon' ).nodeValue () )

#    from core.nodeParam import *
#    createParamTable = {   'float':FloatNodeParam
#                            ,'int':IntNodeParam
#                            ,'color':ColorNodeParam
#                            ,'string':StringNodeParam
#                            ,'normal':NormalNodeParam
#                            ,'point':PointNodeParam
#                            ,'vector':VectorNodeParam
#                            ,'matrix':MatrixNodeParam
#                            ,'surface':SurfaceNodeParam
#                            ,'displacement':DisplacementNodeParam
#                            ,'volume':VolumeNodeParam
#                            ,'light':LightNodeParam
#                            ,'rib':RibNodeParam
#                            ,'text':TextNodeParam
#                            ,'transform':TransformNodeParam
#                            ,'image':ImageNodeParam
#                         }

    input_tag = xml_node.namedItem ( 'input' )
    if not input_tag.isNull () :
      xml_paramList = input_tag.toElement ().elementsByTagName ( 'property' )
      for i in range ( 0, xml_paramList.length () ) :
        xml_param = xml_paramList.item ( i )
        #param_type = str( xml_param.attributes().namedItem( 'type' ).nodeValue() )
        #
        # some parameters (String, Color, Point, Vector, Normal, Matrix ...)
        # have different string interpretation in RIB
        #
        isRibParam = ( self.type == 'rib' or self.type == 'rib_code' )
        param = createParamFromXml ( xml_param, isRibParam, True ) # #param.isInput = True
        #param = createParamTable[ param_type ]( xml_param, isRibParam )
        #param.isInput = True
        self.addInputParam ( param )
        #print '--> param = %s value = %s (isRibParam = %d )' % ( param.label, param.getValueToStr(), isRibParam )

    output_tag = xml_node.namedItem ( 'output' )
    if not output_tag.isNull () :
      xml_paramList = output_tag.toElement ().elementsByTagName ( 'property' )
      for i in range ( 0, xml_paramList.length () ) :
        xml_param = xml_paramList.item ( i )
        #param_type = str( xml_param.attributes().namedItem( 'type' ).nodeValue() )
        #
        # some parameters (Color, Point, Vector, Normal, Matrix ...)
        # have different string interpretation in RIB
        #
        isRibParam = ( self.type == 'rib' or self.type == 'rib_code' )
        param = createParamFromXml ( xml_param, isRibParam, False ) # #param.isInput = False
        #param = createParamTable[ param_type ]( xml_param, isRibParam )
        #param.isInput = False
        self.addOutputParam ( param )
        #print '--> param = %s value = %s' % ( param.label, param.getValueToStr() )

    internal_tag = xml_node.namedItem ( 'internal' )
    if not internal_tag.isNull () :
      xml_internalList = internal_tag.toElement ().elementsByTagName ( 'variable' )
      for i in range ( 0, xml_internalList.length () ) :
        var_tag = xml_internalList.item ( i )
        var = str ( var_tag.attributes ().namedItem ( 'name' ).nodeValue () )
        self.addInternal ( var )

    include_tag = xml_node.namedItem ( 'include' )
    if not include_tag.isNull () :
      xml_includeList = include_tag.toElement ().elementsByTagName ( 'file' )
      for i in range ( 0, xml_includeList.length () ) :
        inc_tag = xml_includeList.item ( i )
        inc = str ( inc_tag.attributes ().namedItem ( 'name' ).nodeValue () )
        self.addInclude ( inc )

    offset_tag = xml_node.namedItem ( 'offset' )
    if not offset_tag.isNull() :
      x = float ( offset_tag.attributes ().namedItem ( 'x' ).nodeValue () )
      y = float ( offset_tag.attributes ().namedItem ( 'y' ).nodeValue () )
      self.offset = ( x, y )

    param_code_tag = xml_node.namedItem ( 'param_code' )
    if not param_code_tag.isNull() :
      self.param_code = str ( param_code_tag.toElement ().text () )

    code_tag = xml_node.namedItem ( 'code' )
    if not code_tag.isNull () :
      self.code = str ( code_tag.toElement ().text () )
  #
  # parseToXML
  #
  def parseToXML ( self, dom ) :
    #
    xml_node = dom.createElement ( 'node' )
    if DEBUG_MODE : print '>> Node::parseToXML (id=%d)' % ( self.id )
    if self.id is None :
      if DEBUG_MODE : print '>> Node::parseToXML id is None'
    xml_node.setAttribute ( 'id', str( self.id ) )
    xml_node.setAttribute ( 'name', self.name )
    if self.label != None : xml_node.setAttribute ( 'label', self.label )
    if self.type != None : xml_node.setAttribute ( 'type', self.type )
    if self.author != None : xml_node.setAttribute ( 'author', self.author )
    if self.icon != None : xml_node.setAttribute ( 'icon', self.icon )

    if self.help != None :
      # append node help (short description)
      help_tag = dom.createElement ( 'help' )
      help_text = dom.createTextNode ( self.help )
      help_tag.appendChild ( help_text )
      xml_node.appendChild ( help_tag )

    input_tag = dom.createElement ( 'input' )
    for param in self.inputParams :
      #print '--> parsing param to XML: %s ...' % param.name
      input_tag.appendChild ( param.parseToXML ( dom )  )
    xml_node.appendChild ( input_tag )

    output_tag = dom.createElement ( 'output' )
    for param in self.outputParams :
      #print '--> parsing param to XML: %s ...' % param.name
      output_tag.appendChild ( param.parseToXML ( dom )  )
    xml_node.appendChild ( output_tag )

    internal_tag = dom.createElement ( 'internal' )
    for var in self.internals :
      var_tag = dom.createElement( 'variable' )
      var_tag.setAttribute ( 'name', var )
      internal_tag.appendChild ( var_tag )
    xml_node.appendChild ( internal_tag )

    include_tag = dom.createElement ( 'include' )
    for inc in self.includes :
      inc_tag = dom.createElement( 'file' )
      inc_tag.setAttribute ( 'name', inc )
      include_tag.appendChild ( inc_tag )
    xml_node.appendChild ( include_tag )

    if self.param_code != None :
      param_code_tag = dom.createElement ( 'param_code' )
      param_code_data = dom.createCDATASection ( self.param_code )
      param_code_tag.appendChild ( param_code_data )
      xml_node.appendChild ( param_code_tag )

    if self.code != None :
      code_tag = dom.createElement ( 'code' )
      code_data = dom.createCDATASection ( self.code )
      code_tag.appendChild ( code_data )
      xml_node.appendChild ( code_tag )

    if self.offset != None :
      ( x, y ) = self.offset
      offset_tag = dom.createElement ( 'offset' )
      offset_tag.setAttribute ( 'x', x )
      offset_tag.setAttribute ( 'y', y )
      xml_node.appendChild ( offset_tag )

    return xml_node
  #
  # computeNode
  #
  def computeNode ( self ) :
    if DEBUG_MODE : print '>> Node (%s).computeNode' % self.label
    self.execParamCode ()
  #
  # execParamCode
  #
  def execParamCode ( self ) :
    #
    if self.param_code != None :
      param_code = self.param_code.lstrip ()
      if param_code != '' :
        exec param_code
  #
  # getComputedParamList
  #
  def getComputedParamList ( self ) :
    #print '-> getComputedParamList'

    param_list = self.computedInputParams
    # rslHeader += self.parseGlobalVars ( self.computedOutputParams )
    # output parameters are stored in set to prevent duplication
    for out_param in set ( self.computedOutputParams ) :
      param_list += out_param
    return param_list
  #
  # parseGlobalVars
  #
  def parseGlobalVars ( self, parsedStr ) :
    #print '-> parseGlobalVars in %s' % parsedStr
    resultStr = ''
    parserStart = 0
    parserPos = 0

    while parserPos != -1 :
      parserPos = str ( parsedStr ).find ( '$', parserStart )
      if parserPos != -1 :
        #
        if parserPos != 0 :
          resultStr += parsedStr [ parserStart : parserPos ]

        # check global vars first
        if parsedStr [ ( parserPos + 1 ) : ( parserPos + 2 ) ] == '{' :
          globStart = parserPos + 2
          parserPos = str( parsedStr ).find ( '}', globStart )
          global_var_name = parsedStr [ globStart : ( parserPos ) ]

          #print '-> found global var %s' % global_var_name

          if global_var_name in app_global_vars.keys() :
            resultStr += app_global_vars [ global_var_name ]
          elif global_var_name in node_global_vars.keys() :
            if global_var_name == 'INSTANCENAME' : resultStr += self.getInstanceName ()
            elif global_var_name == 'NODELABEL' : resultStr += self.getLabel ()
            elif global_var_name == 'NODENAME' : resultStr += self.getName ()
            elif global_var_name == 'PARAMS' : resultStr += self.getComputedParamList ()
        else :
          # keep $ sign for otheer, non ${...} cases
          resultStr += '$'

      #print 'parserPos = %d parserStart = %d' % ( parserPos, parserStart )
      if parserPos != -1 :
        parserStart = parserPos + 1

    resultStr += parsedStr [ parserStart: ]

    return resultStr
  #
  # copySetup
  #
  def copySetup ( self, newNode ) :
    if DEBUG_MODE : print '>> Node::copySetup (%s)' % self.label
    newNode.id = self.id
    name = self.name
    if name is None :
      name = str( self.type )
    newNode.name = name
    label = self.label
    if label is None :
      label = name
    newNode.label = label
    newNode.type = self.type
    newNode.author = self.author
    newNode.help = self.help
    newNode.icon = self.icon
    newNode.master = self.master

    import copy
    newNode.code = copy.copy ( self.code )
    newNode.param_code = copy.copy ( self.param_code )
    #self.computed_code = None

    newNode.internals = copy.copy ( self.internals )
    newNode.includes = copy.copy ( self.includes )

    if len ( newNode.inputParams ) :
      if DEBUG_MODE : print '>> Node::copySetup %s inputParams cleared ' % newNode.label
      newNode.inputParams = []
    for param in self.inputParams :
      newNode.inputParams.append ( param.copy () )

    if len ( newNode.outputParams ) :
      if DEBUG_MODE : print '>> Node::copySetup %s outputParams cleared ' % newNode.label
      newNode.outputParams = []
    for param in self.outputParams :
      newNode.outputParams.append ( param.copy () )
    return newNode
#
# name and type must be specified in xml
#
def createParamFromXml ( xml_param, isRibParam, isInput = True ) :
  from core.nodeParam import FloatNodeParam
  from core.nodeParam import IntNodeParam
  from core.nodeParam import ColorNodeParam
  from core.nodeParam import StringNodeParam
  from core.nodeParam import NormalNodeParam
  from core.nodeParam import PointNodeParam
  from core.nodeParam import VectorNodeParam
  from core.nodeParam import MatrixNodeParam
  from core.nodeParam import SurfaceNodeParam
  from core.nodeParam import DisplacementNodeParam
  from core.nodeParam import VolumeNodeParam
  from core.nodeParam import LightNodeParam
  from core.nodeParam import RibNodeParam
  from core.nodeParam import TextNodeParam
  from core.nodeParam import TransformNodeParam
  from core.nodeParam import ImageNodeParam

  param = None
  createParamTable = {   'float':FloatNodeParam
                          ,'int':IntNodeParam
                          ,'color':ColorNodeParam
                          ,'string':StringNodeParam
                          ,'normal':NormalNodeParam
                          ,'point':PointNodeParam
                          ,'vector':VectorNodeParam
                          ,'matrix':MatrixNodeParam
                          ,'surface':SurfaceNodeParam
                          ,'displacement':DisplacementNodeParam
                          ,'volume':VolumeNodeParam
                          ,'light':LightNodeParam
                          ,'rib':RibNodeParam
                          ,'text':TextNodeParam
                          ,'transform':TransformNodeParam
                          ,'image':ImageNodeParam
                       }
  param_type = str( xml_param.attributes().namedItem( 'type' ).nodeValue() )
  if param_type in createParamTable.keys() :
    param = createParamTable[ param_type ]( xml_param, isRibParam )
    param.isInput = isInput
  else :
    print '* Error: unknown param type !'
  return param
