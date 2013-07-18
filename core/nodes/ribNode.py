#===============================================================================
# ribNode.py
#===============================================================================
import os, sys
from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam

from global_vars import app_global_vars, DEBUG_MODE
from core.node_global_vars import node_global_vars
#
# RIBNode
#
class RIBNode ( Node ) :
  #
  # __init__
  #
  def __init__ ( self, xml_node = None ) :
    #
    Node.__init__ ( self, xml_node )
    self.ribName = ''
  #
  # copy
  #
  def copy ( self ) :
    #
    if DEBUG_MODE : print '>> RIBNode( %s ).copy' % self.label
    newNode = RIBNode ()
    self.copySetup ( newNode )
    return newNode
  #
  # getInputParamValueByName
  #
  def getInputParamValueByName ( self, name ) :
    #
    result = None
    srcNode = srcParam = None
    param = self.getInputParamByName ( name )
    ( srcNode, srcParam ) = self.getLinkedSrcNode ( param )
    if srcNode is not None :
      srcNode.computeNode ()
      #if self.computed_code is not None :
      #  self.computed_code += link.srcNode.computed_code

      if srcNode.type in [ 'rib', 'rib_code' ] :
        #result = '## start code from :' + link.srcNode.label
        result = srcNode.parseLocalVars ( srcNode.code )
        #result += '## end code from :' + link.srcNode.label
      else :
        result = srcNode.parseGlobalVars ( srcParam.getValueToStr () )
    else :
      result = param.getValueToStr ()
    return result
  #
  # computeNode
  #
  def computeNode ( self ) :
    #print '>> RIBNode (%s).computeNode' % self.label
    #
    # inside code, imageName value can be assigned from different
    # input parameters
    #
    self.execControlCode ()

    self.ribName = app_global_vars[ 'TempPath' ] + '/' + self.getInstanceName() + '.rib'

    ribCode = self.parseLocalVars ( self.code )
    ribCode = self.parseGlobalVars ( ribCode )

    print '>> RIBNode save file %s' % self.ribName

    f = open ( self.ribName, 'w+t' )
    f.write ( ribCode )
    f.close ()

    from meShaderEd import app_renderer

    renderer = app_global_vars [ 'Renderer' ]
    flags = app_global_vars [ 'RendererFlags' ]
    renderCmd = [ renderer ]
    if  flags != '' :  renderCmd.append ( flags )
    renderCmd.append ( self.ribName )

    print '>> RIBNode renderCmd = %s' %  ' '.join( renderCmd )

    # call the process
    from core.meCommon import launchProcess

    launchProcess ( renderCmd )

    return self.ribName
  #
  # parseLocalVars
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

          # print '-> found local var %s' % local_var_name

          param = self.getInputParamByName ( local_var_name )
          if param is not None :
            value = self.getInputParamValueByName ( local_var_name )
            resultStr += value
          else :
            param = self.getOutputParamByName ( local_var_name )
            if param is not None :
              resultStr += param.getValueToStr ()
            else :
              print '!! local var %s is not defined !' % local_var_name
        else :
          # keep $ sign for otheer, non $(...) cases
          resultStr += '$'

      #print 'parserPos = %d parserStart = %d' % ( parserPos, parserStart )
      if parserPos != -1 :
        parserStart = parserPos + 1

    resultStr += parsedStr [ parserStart: ]

    return resultStr

