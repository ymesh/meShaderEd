#===============================================================================
# imageNode.py
#
#
#
#===============================================================================
import os, sys
from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# ImageNode
#
class ImageNode( Node ):
  #
  #
  def __init__ ( self, xml_node = None ):
    #
    Node.__init__( self, xml_node )
    self.imageName = ''
    if DEBUG_MODE : print ">> ImageNode __init__"
  #
  #
  def copy ( self ):
    if DEBUG_MODE : print '>> ImageNode::copy (%s)' % self.label
    newNode = ImageNode()
    self.copySetup ( newNode )
    return newNode
  #
  #
  """
  def getInputParamValueByName ( self, name ):
    #
    result = None
    param = self.getInputParamByName ( name )

    if self.isInputParamLinked ( param ) :
      link = self.inputLinks[ param ]
      srcNode = link.srcNode
      link.printInfo ()

      #while ( srcNode.type = 'connector' )

      srcNode.computeNode ()

      if self.computed_code is not None :
        self.computed_code += srcNode.computed_code

      result = srcNode.parseGlobalVars ( srcParam.getValueToStr () )
    else :
      result = param.getValueToStr ()

    return result
  """
  #
  #
  def computeNode ( self ) :
    print '>> ImageNode (%s).computeNode' % self.label
    #
    # inside param_code, imageName value can be assigned from different
    # input parameters

    self.execParamCode ()

    return self.imageName

  #
  # Hmmm... Not really sure why this is here....
  #
  """
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

          print '-> found local var %s' % local_var_name

          param = self.getInputParamByName ( local_var_name )
          if param is not None :
            value = self.getInputParamValueByName ( local_var_name )
            resultStr += value
          else :
            param = self.getOutputParamByName ( local_var_name )
            if param is not None :
              resultStr += param.getValueToStr ()
            else :
              print '-> ERRPR: local var %s is not defined !' % local_var_name
        else :
          # keep $ sign for otheer, non $(...) cases
          resultStr += '$'

      #print 'parserPos = %d parserStart = %d' % ( parserPos, parserStart )
      if parserPos != -1 :
        parserStart = parserPos + 1

    resultStr += parsedStr [ parserStart: ]

    return resultStr
    """
