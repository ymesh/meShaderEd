#===============================================================================
# ShaderInfo.py
#===============================================================================
import os, sys
import re
from PyQt4 import QtCore

from global_vars import app_global_vars, DEBUG_MODE

from core.nodeParam import FloatNodeParam
from core.nodeParam import IntNodeParam
from core.nodeParam import ColorNodeParam
from core.nodeParam import StringNodeParam
from core.nodeParam import NormalNodeParam
from core.nodeParam import PointNodeParam
from core.nodeParam import VectorNodeParam
from core.nodeParam import MatrixNodeParam
#
# ShaderInfo
#
class ShaderInfo () :
  #
  # __init__
  #
  def __init__ ( self, shaderFileName = None ) :
    #
    self.fileName = shaderFileName
    self.name = None
    self.type = None
    self.inputParams = []
    self.outputParams = []

    if self.fileName is not None :
      self.parseParamsInfo ( self.getShaderInfo () )
  #
  # getShaderInfo
  #
  def getShaderInfo ( self, methods = False ) :
    #
    inputLines = []
    if DEBUG_MODE : print '>> ShaderInfo.get ( %s ) by "%s"' % ( self.fileName, app_global_vars [ 'ShaderInfo' ] )
    # app_global_vars [ 'ShaderCompiler' ]
    # app_global_vars [ 'SLO' ]
    from core.meCommon import launchProcess

    cmdList = []
    cmdList.append ( app_global_vars [ 'ShaderInfo' ] )
    if methods :
      cmdList.append ( '--methods' )
    cmdList.append ( self.fileName )

    tmpDir = app_global_vars [ 'TempPath' ]

    stdoutLog = os.path.join ( tmpDir, 'stdout-%s.log' % os.path.basename ( self.fileName ) )
    stderrLog = os.path.join ( tmpDir, 'stderr-%s.log' % os.path.basename ( self.fileName ) )

    launchProcess ( cmdList, stdoutLog, stderrLog )

    stdout = file ( stdoutLog, 'r' )
    stderr = file ( stderrLog, 'r' )

    inputLines = stdout.read ().split ( '\n' )

    stdout.close ()
    stderr.close ()
    return  inputLines
  #
  # parseParamsInfo
  #
  def parseParamsInfo ( self, inputLines ) :
    #
    self.name = None
    self.type = None

    paramName = None
    paramType = None
    isOutput = False
    paramArraySize = None
    paramDetail = None
    paramValue = None
    paramSpace = None

    state = 'GET_TYPE'

    for line in inputLines :
      line = line.strip ()
      if line != '' :
        if state == 'GET_TYPE' :
          ( self.name, self.type ) = self.parseShaderNameLine ( line )
          print '>> shader name = %s type = %s' % ( self.name, self.type )
          state = 'GET_PARAM'
        elif state == 'GET_PARAM' :
          print line
          ( paramName, paramType, paramDetail, isOutput, paramArraySize ) = self.parseParamLine ( line )
          print '>> param name = %s type = "%s %s" output = %s' % ( paramName, paramDetail, paramType, isOutput )
          state = 'GET_VALUE'
        elif state == 'GET_VALUE' :
          print line
          state = 'GET_PARAM'

  #
  # parseShaderNameLine
  #
  def parseShaderNameLine ( self, inputStr ) :
    #
    ( type, name ) = inputStr.split ( ' ' )
    return ( name.strip ( '"' ), type )
  #
  # parseParamLine
  #
  def parseParamLine ( self, inputStr ) :
    #
    paramName = None
    paramType = None
    paramDetail = None
    isOutput = False
    paramArraySize = None

    name_pattern_str = '"\w*"' # '"[a-zA-Z0-9_]*"'
    type_pattern_str = '"[][\w\s]*"'
    output_pattern_str = 'output parameter*'
    prefix = '[\w\s]*' # '*[uniformvaryg]+ '
        
    p = re.compile ( name_pattern_str )
    if p.match ( inputStr ) :
      paramName = ( p.findall ( inputStr ) [ 0 ]  ).strip ( '"' )
      p = re.compile ( type_pattern_str )
      if p.match ( inputStr ) :
        typeStr = ( p.findall ( inputStr ) [ 1 ]  ).strip ( '"' )
        #print typeStr
        p = re.compile ( output_pattern_str )
        if p.match ( typeStr ) :
          isOutput = True
        for tp in [ 'float', 'color', 'point', 'normal', 'vector', 'matrix', 'string', 'shader' ] :
          p = re.compile ( prefix + tp )
          if p.match ( typeStr ) : 
            paramType = tp   
            break
 
    return ( paramName, paramType, paramDetail, isOutput, paramArraySize )
