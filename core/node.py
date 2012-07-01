#===============================================================================
# node.py
#
# 
#
#===============================================================================
import os, sys
from PyQt4 import QtCore

from global_vars import app_global_vars
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
  def addInputParam ( self, param ) :
    self.inputParams.append ( param ) 
  #
  #
  def addOutputParam ( self, param ) :
    self.outputParams.append ( param ) 
  #
  #
  def addInternal ( self, internal ) :
    #print '--> add internal: %s' % internal
    if internal != '' : self.internals.append ( internal )
  #
  #
  def addInclude ( self, include ) :
    #print '--> add include: %s' % include
    if include != '' : self.includes.append ( include )
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
  def getInputParamByName ( self, name ):
    result = None
    for param in self.inputParams :
      if param.name == name :
        result = param  
        break
    return result
  #
  #    
  def getOutputParamByName ( self, name ):
    result = None
    for param in self.outputParams :
      if param.name == name :
        result = param  
        break
    return result
  #
  #    
  def getInputParamValueByName ( self, name ):
    #
    result = None
    param = self.getInputParamByName ( name )
    
    if self.isInputParamLinked ( param ) :
      link = self.inputLinks[ param ]
      
      link.printInfo ()
      link.srcNode.computeNode()
      
      if self.computed_code is not None :
        self.computed_code += link.srcNode.computed_code
      
      result = link.srcNode.parseGlobalVars ( link.srcParam.getValueToStr () )
    else :
      result = param.getValueToStr ()
    
    return result
  #
  #
  def onParamChanged ( self, param ):
    print ">> Node: onParamChanged node = %s param = %s" % ( self.label, param.name )  
    #self.emit( QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self, param ) 
  #
  #
  def getLabel ( self ) : return self.label 
  #
  #
  def getName ( self ) : return self.label 
  #
  #
  def getInstanceName ( self ) : return self.label 
  #
  #
  def getParams ( self ) :
     return self.label 
  #
  #    
  def getParamName ( self, param ):
    result = param.name
    if not ( param.provider == 'primitive' or param.isRibParam ) :
      result = self.getInstanceName () + '_' + param.name
    return result
  #
  #  
  def getParamDeclaration ( self, param ) :
    result = ''
    result += param.typeToStr() + ' '
    result += self.getParamName ( param ) + ' = '
    result += param.getValueToStr() + ';\n'  
    return result
  #
  #
  #
  def parseFromXML ( self, xml_node ) :
    #
    id_node = xml_node.attributes().namedItem( 'id' )
    if not id_node.isNull() :
      self.id = int ( id_node.nodeValue() )
    else :
      pass
      print ':: id is None'
    self.name = str ( xml_node.attributes().namedItem( 'name' ).nodeValue() )
    self.label = str ( xml_node.attributes().namedItem( 'label' ).nodeValue() )
    if self.label == '' : self.label = self.name
    #print '-> parsing from XML node name= %s label= %s' % ( self.name, self.label )
    
    self.author = str ( xml_node.attributes().namedItem( 'author' ).nodeValue() )
    self.type = str ( xml_node.attributes().namedItem( 'type' ).nodeValue() )
    
    help_tag = xml_node.namedItem ( 'help' )
    if not help_tag.isNull() :
      self.help = help_tag.toElement().text()
      #print '-> help= %s' % self.help
      
    from core.nodeParam import *
    
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
                         
    input_tag = xml_node.namedItem ( 'input' )
    if not input_tag.isNull() :
      xml_paramList = input_tag.toElement().elementsByTagName ( 'property' )
      for i in range( 0, xml_paramList.length() ) :
        xml_param = xml_paramList.item( i )
        param_type = str( xml_param.attributes().namedItem( 'type' ).nodeValue() )
        #
        # some parameters (String, Color, Point, Vector, Normal, Matrix ...)
        # have different string interpretation in RIB
        #
        isRibParam = ( self.type == 'rib' or self.type == 'rib_code' )
        param = createParamTable[ param_type ]( xml_param, isRibParam )
        param.isInput = True
        self.addInputParam ( param )
        print '--> param = %s value = %s (isRibParam = %d )' % ( param.label, param.getValueToStr(), isRibParam )
    
    output_tag = xml_node.namedItem ( 'output' )
    if not output_tag.isNull() :
      xml_paramList = output_tag.toElement().elementsByTagName ( 'property' )
      for i in range( 0, xml_paramList.length() ) :
        xml_param = xml_paramList.item( i )
        param_type = str( xml_param.attributes().namedItem( 'type' ).nodeValue() )
        #
        # some parameters (Color, Point, Vector, Normal, Matrix ...)
        # have different string interpretation in RIB
        #
        isRibParam = ( self.type == 'rib' )
        param = createParamTable[ param_type ]( xml_param, isRibParam )
        param.isInput = False
        self.addOutputParam ( param ) 
        #print '--> param = %s value = %s' % ( param.label, param.getValueToStr() )
    
    internal_tag = xml_node.namedItem ( 'internal' )
    if not internal_tag.isNull() :
      xml_internalList = internal_tag.toElement().elementsByTagName ( 'variable' )
      for i in range( 0, xml_internalList.length() ) :
        var_tag = xml_internalList.item( i )
        var = str ( var_tag.attributes().namedItem( 'name' ).nodeValue() )
        self.addInternal ( var )
          
    include_tag = xml_node.namedItem ( 'include' )
    if not include_tag.isNull() :
      xml_includeList = include_tag.toElement().elementsByTagName ( 'file' )
      for i in range( 0, xml_includeList.length() ) :
        inc_tag = xml_includeList.item( i )
        inc = str ( inc_tag.attributes().namedItem( 'name' ).nodeValue() )
        self.addInclude ( inc )
        
    offset_tag = xml_node.namedItem ( 'offset' )
    if not offset_tag.isNull() :
      x = float ( offset_tag.attributes().namedItem( 'x' ).nodeValue() )
      y = float ( offset_tag.attributes().namedItem( 'y' ).nodeValue() )
      self.offset = ( x, y )
      
    param_code_tag = xml_node.namedItem ( 'param_code' )
    if not param_code_tag.isNull() :
      self.param_code = str( param_code_tag.toElement().text() )
      
    code_tag = xml_node.namedItem ( 'code' )
    if not code_tag.isNull() :
      self.code = str( code_tag.toElement().text() )
    
  #
  #
  #  
  def parseToXML ( self, dom ) :
    #
    xml_node = dom.createElement( 'node' )
    
    xml_node.setAttribute ( 'id', str( self.id ) )
    xml_node.setAttribute ( 'name', self.name )
    if self.label != None : xml_node.setAttribute ( 'label', self.label )
    if self.type != None : xml_node.setAttribute ( 'type', self.type )
    if self.author != None : xml_node.setAttribute ( 'author', self.author )
    
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
  #
  def collectComputed ( self, shaderCode, visitedNodes ) :
    print '>> Node (%s).collectComputed' % self.label
    #
    self.computedInputParams = ''
    self.computedLocals = ''
    self.computedLocalParams = ''
    self.computedIncludes = []
    self.computedOutputParams = []
    
    #self.computedCode = ''
    
    for param in self.inputParams :
      if self.isInputParamLinked ( param ) :
        link = self.inputLinks[ param ]
        
        if not link.srcNode in visitedNodes :
          #link.printInfo ()
          shaderCode = link.srcNode.collectComputed ( shaderCode, visitedNodes )
        
          #if self.computedCode is not None :
          #self.computedCode = link.srcNode.computedCode + self.computedCode
          
          self.computedInputParams = link.srcNode.computedInputParams + self.computedInputParams
          self.computedLocalParams = link.srcNode.computedLocalParams + self.computedLocalParams
          
          for out_param in link.srcNode.computedOutputParams :
            self.computedOutputParams.append( out_param )  
          
          for inc_name in link.srcNode.computedIncludes : 
            self.computedIncludes.append( inc_name )  
      
      else :    
        declare = self.getParamDeclaration ( param )
        print '>> Node (%s).collectComputed: local param %s' % ( self.label, declare )
        if param.shaderParam :
          self.computedInputParams += declare
        else :
          self.computedLocalParams += declare 
          
    for param in self.outputParams :
      if not param.type in ['surface', 'displacement', 'light', 'volume'] : 
        declare = self.getParamDeclaration ( param )
        if param.provider == 'primitive' : 
          self.computedOutputParams.append( 'output ' + declare )  
        else :
          self.computedLocalParams += declare 
    
    for inc_name in self.includes :      
      self.computedIncludes.append( inc_name )
    #print self.includes
    
    visitedNodes.add ( self )
    shaderCode += self.parseLocalVars ( self.code )
    
    return shaderCode
  #
  #
  def computeNode ( self ) : 
    print '>> Node (%s).computeNode' % self.label
    self.execParamCode ()
  #
  #
  def execParamCode ( self ) :
    #
    if self.param_code != None :
      param_code = self.param_code.lstrip()
      if param_code != '' :
        exec param_code  
  #
  #
  def parseGlobalVars ( self, parsedStr ) :
    #print '-> parseGlobalVars in %s' % parsedStr
    resultStr = ''
    parserStart = 0
    parserPos = 0
    
    while parserPos != -1 :
      parserPos = parsedStr.find ( '$', parserStart )
      if parserPos != -1 :
        # 
        if parserPos != 0 :
          resultStr += parsedStr [ parserStart : parserPos ]
        
        # check global vars first
        if parsedStr [ ( parserPos + 1 ) : ( parserPos + 2 ) ] == '{' :
          globStart = parserPos + 2
          parserPos = parsedStr.find ( '}', globStart )
          global_var_name = parsedStr [ globStart : ( parserPos ) ]
          
          print '-> found global var %s' % global_var_name
          
          if global_var_name in app_global_vars.keys() : 
            resultStr += app_global_vars [ global_var_name ]
          elif global_var_name in node_global_vars.keys() :
            if global_var_name == 'INSTANCENAME' : resultStr += self.getInstanceName ()
            elif global_var_name == 'NODELABEL' : resultStr += self.getLabel ()
            elif global_var_name == 'NODENAME' : resultStr += self.getName ()
            elif global_var_name == 'PARAMS' : resultStr += self.getParams ()
        else :
          # keep $ sign for otheer, non ${...} cases
          resultStr += '$'
          
      #print 'parserPos = %d parserStart = %d' % ( parserPos, parserStart )
      if parserPos != -1 :
        parserStart = parserPos + 1
    
    resultStr += parsedStr [ parserStart: ]
    
    return resultStr
  #
  # RSL specific parser
  #
  def parseLocalVars ( self, parsedStr ) :
    #print '-> parseLocalVars in %s' % parsedStr
    resultStr = ''
    parserStart = 0
    parserPos = 0
    
    while parserPos != -1 :
      parserPos = parsedStr.find ( '$', parserStart )
      if parserPos != -1 :
        # 
        if parserPos != 0 :
          resultStr += parsedStr [ parserStart : parserPos ]
        
        # check local variables
        if parsedStr [ ( parserPos + 1 ) : ( parserPos + 2 ) ] == '(' :
          globStart = parserPos + 2
          parserPos = parsedStr.find ( ')', globStart )
          local_var_name = parsedStr [ globStart : ( parserPos ) ]
          
          #print '> Node(%s).parseLocalVars: found local var %s' % ( self.label, local_var_name )
          #
          # check if variable is input parameter name
          #
          param = self.getInputParamByName ( local_var_name ) 
          if param is not None :
            if self.isInputParamLinked ( param ) :
              link = self.inputLinks[ param ]
              resultStr += link.srcNode.getParamName ( link.srcParam )  
            else :
              resultStr += self.getParamName ( param )       
          else :
            #
            # check if variable is output parameter name
            #
            param = self.getOutputParamByName ( local_var_name )
            if param is not None :
              resultStr += self.getParamName ( param )        
            else :
              #
              # check if this is just local variable 
              #
              if local_var_name in self.internals :
                resultStr += self.getInstanceName () + '_' + local_var_name
              else :
                print '> Node(%s).parseLocalVars: ERROR. Local var %s is not defined !' % ( self.label, local_var_name )  
        else :
          # keep $ sign for otheer, non $(...) cases
          resultStr += '$'
          
      #print 'parserPos = %d parserStart = %d' % ( parserPos, parserStart )
      if parserPos != -1 :
        parserStart = parserPos + 1
    
    resultStr += parsedStr [ parserStart: ]
    
    return resultStr
  
