#===============================================================================
# ShaderInfo.py
#===============================================================================
import os, sys
import re
from PyQt4 import QtCore

from global_vars import app_global_vars, DEBUG_MODE, VALID_RSL_PARAM_TYPES

from core.meCommon import parseGlobalVars

from core.params.floatNodeParam        import FloatNodeParam
from core.params.intNodeParam          import IntNodeParam
from core.params.colorNodeParam        import ColorNodeParam
from core.params.stringNodeParam       import StringNodeParam
from core.params.normalNodeParam       import NormalNodeParam
from core.params.pointNodeParam        import PointNodeParam
from core.params.vectorNodeParam       import VectorNodeParam
from core.params.matrixNodeParam       import MatrixNodeParam
from core.params.shaderNodeParam       import ShaderNodeParam
#
# ShaderInfo
#
class ShaderInfo () :
  #
  # __init__
  #
  def __init__ ( self, shaderFileName = None ) :
    #
    self.fileName = parseGlobalVars ( shaderFileName )
    self.name = None
    self.type = None
    self.inputParams = []
    self.outputParams = []
    
    self.parseValueLine = self.parseValueLine_prman
    
    parseValueLineProc = {
       'prman'    : self.parseValueLine_prman
      ,'renderdl' : self.parseValueLine_delight 
      ,'air'      : self.parseValueLine_air
      ,'aqsis'    : self.parseValueLine_aqsis 
      ,'rndr'     : self.parseValueLine_pixie 
      ,'renderdc' : self.parseValueLine_rdc 
    }
    
    self.renderer = app_global_vars [ 'Renderer' ]
    if self.renderer in parseValueLineProc.keys () : self.parseValueLine = parseValueLineProc [ self.renderer ]

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
    paramDetail = None
    paramValue = None
    paramSpace = None
    paramArraySize = None
    
    param = None
    createParamTable = {   'float'  : FloatNodeParam
                          ,'color'  : ColorNodeParam
                          ,'string' : StringNodeParam
                          ,'shader' : ShaderNodeParam
                          ,'normal' : NormalNodeParam
                          ,'point'  : PointNodeParam
                          ,'vector' : VectorNodeParam
                          ,'matrix' : MatrixNodeParam
                       }

    valueIdx = 0
    valueNum = 1
    accumLine = ''
    accumLinesNum = 0
    
    state = 'GET_TYPE'

    for line in inputLines :
      line = line.strip ()
      if line != '' :
        if state == 'GET_TYPE' :
          # get shader name and type
          ( self.name, self.type ) = self.parseShaderNameLine ( line )
          print '>> shader name = %s type = %s' % ( self.name, self.type )
          state = 'GET_PARAM'
        elif state == 'GET_PARAM' :
          # get parameter description 
          ( paramName, paramType, paramDetail, isOutput, paramArraySize ) = self.parseParamLine ( line )
          print '>> paramName = %s type = "%s %s" output = %s ArraySize = %s' % ( paramName, paramDetail, paramType, isOutput, paramArraySize )
          
          if paramType in createParamTable.keys () :
            param = createParamTable [ paramType ] ()
            param.setup ( paramName, paramName, paramDetail )
            param.arraySize = paramArraySize
            param.isInput = not isOutput
            if param.isInput :
              self.inputParams.append ( param )
            else :
              self.outputParams.append ( param )
          else :
            param = None
            print '* Error: unknown param type !' 
          
          valueNum = 1
          if self.renderer == 'prman' :
            if paramArraySize is not None :
              valueNum = paramArraySize
            if paramType == 'matrix' :
              accumLine = ''
              accumLinesNum = 3
          valueIdx = 0
          state = 'GET_VALUE'
        elif state == 'GET_VALUE' :
          # get value ( or arrays elements )
          # print valueIdx, valueNum
          if accumLinesNum > 0 :
            accumLinesNum -= 1
            accumLine += line
            continue
          if self.renderer == 'prman' and paramType == 'matrix' :
            line = accumLine + line
          if paramArraySize is None :
            ( paramValue, paramSpace ) = self.parseValueLine ( line, paramType )
            print '>> paramValue = "%s" paramSpace = "%s"' % ( paramValue, paramSpace )
            if param is not None :
              param.default = paramValue
              param.value = paramValue
              param.space = paramSpace
          else :
            print '* Warning: Arrays are not fully supported yet !'
            if self.renderer == 'prman' :
              ( paramValue, paramSpace ) = self.parseValueLine ( line, paramType, valueIdx )
              print '>> paramValue = "%s" paramSpace = "%s"' % ( paramValue, paramSpace )
              if param is not None :
                param.defaultArray.append ( paramValue )
                param.valueArray.append ( paramValue )
                param.spaceDefArray.append ( paramSpace )
                param.spaceArray.append ( paramSpace )
            else :
              for valueIdx in range ( paramArraySize ) :
                ( paramValue, paramSpace ) = self.parseValueLine ( line, paramType, valueIdx )
                print '>> paramValue = "%s" paramSpace = "%s"' % ( paramValue, paramSpace )
                if param is not None :
                  param.defaultArray.append ( paramValue )
                  param.valueArray.append ( paramValue )
                  param.spaceDefArray.append ( paramSpace )
                  param.spaceArray.append ( paramSpace )
          valueIdx = valueIdx + 1
          if valueIdx >= valueNum : 
            state = 'GET_PARAM'
          else :
            if self.renderer == 'prman' and paramType == 'matrix' :
              accumLine = ''
              accumLinesNum = 3

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
    # print 'parsing param: %s ...' % inputStr
    paramName = None
    paramType = None
    paramDetail = None
    isOutput = False
    paramArraySize = None

    name_pattern_str = '"\w*"' # '"[a-zA-Z0-9_]*"'
    type_pattern_str = '"[][\w\s]*"'
    type_prefix = '(output )?parameter [uniformvaryg ]+ ' #'[\w\s]*' # '*[uniformvaryg ]+ '
    
    p = re.compile ( name_pattern_str )
    if p.match ( inputStr ) :
      paramName = ( p.findall ( inputStr ) [ 0 ]  ).strip ( '"' )
      p = re.compile ( type_pattern_str )
      if p.match ( inputStr ) :
        typeStr = ( p.findall ( inputStr ) [ 1 ]  ).strip ( '"' )

        if 'output' in typeStr : isOutput = True

        for param_type in VALID_RSL_PARAM_TYPES :
          p = re.compile ( type_prefix + param_type )
          if p.match ( typeStr ) : 
            paramType = param_type   
            break
            
        for param_detail in [ 'uniform', 'varying' ] :
          if param_detail in typeStr : 
            paramDetail = param_detail   
            break
       
        match = re.search ( r'\[[\d]*\]$', typeStr )
        
        if match :
          arr_size_str = match.group ().strip ( '[]' )
          if arr_size_str == '' : arr_size_str = '0'
          paramArraySize = int ( arr_size_str )

    return ( paramName, paramType, paramDetail, isOutput, paramArraySize )
  #
  # parseValueLine_prman
  #
  # idxInArray is dummy parameter here and used only for compatibility
  # with other renderers parseValueLine functions 
  #
  def parseValueLine_prman ( self, inputStr, paramType, idxInArray = 0 ) :
    #
    # print 'parsing value: %s ...' % inputStr
    
    paramValue = None
    paramSpace = None
    isValid = False
    
    match = re.search ( r'\ADefault value: ', inputStr )
    if match : 
      isValid = True
    else :
      match = re.search ( r'\AUniform default value: ', inputStr )
      if match :
        isValid = True
    if isValid :    
      valueStr = inputStr.replace ( match.group (), '' )  
      if paramType in [ 'string', 'shader' ] :
        paramValue = valueStr.strip ( '"' )
      elif paramType == 'float' :
        paramValue = float ( valueStr )
      elif paramType in [ 'color', 'point', 'vector', 'normal', 'matrix' ] :
        match = re.search ( r'\A"[A-z]+"', valueStr )
        if match :
          paramSpace = match.group ().strip ( '"' )
        s = re.findall ( r'[+-]?[0-9]+\.[0-9]*', valueStr )
        f = map ( float, s )
        if paramType != 'matrix' : 
          paramValue = [ f[0], f[1], f[2] ]
        else :
          paramValue = [ f[0:4], f[4:8], f[8:12], f[12:16] ]

    return ( paramValue, paramSpace )
  #
  # parseValueLine_delight
  #
  def parseValueLine_delight ( self, inputStr, paramType, idxInArray = 0 ) :
    #
    print 'parsing value: %s ...' % inputStr
    
    paramValue = None
    paramSpace = None
    
    return ( paramValue, paramSpace )
  #
  # parseValueLine_air
  #
  def parseValueLine_air ( self, inputStr, paramType, idxInArray = 0 ) :
    #
    print 'parsing value: %s ...' % inputStr
    
    paramValue = None
    paramSpace = None
    
    return ( paramValue, paramSpace )
  #
  # parseValueLine_aqsis
  #
  def parseValueLine_aqsis ( self, inputStr, paramType, idxInArray = 0 ) :
    #
    print 'parsing value: %s ...' % inputStr
    
    paramValue = None
    paramSpace = None
    
    return ( paramValue, paramSpace )
  #
  # parseValueLine_pixie
  #
  def parseValueLine_pixie ( self, inputStr, paramType, idxInArray = 0 ) :
    #
    print 'parsing value: %s ...' % inputStr
    
    paramValue = None
    paramSpace = None
    
    return ( paramValue, paramSpace )
  #
  # parseValueLine_rdc
  #
  def parseValueLine_rdc ( self, inputStr, paramType, idxInArray = 0 ) :
    #
    print 'parsing value: %s ...' % inputStr
    
    paramValue = None
    paramSpace = None
    
    return ( paramValue, paramSpace )
