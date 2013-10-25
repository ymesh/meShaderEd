"""

 rslNode.py
 
 ver. 1.0.0
 Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)

"""
import os, sys
from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from core.meCommon import *

from global_vars import app_global_vars, DEBUG_MODE, VALID_RSL_SHADER_TYPES
from core.node_global_vars import node_global_vars
#
# RSLNode
#
class RSLNode ( Node ) :
  #
  # __init__
  #
  def __init__ ( self, xml_node = None ) :
    #
    Node.__init__ ( self, xml_node )
    self.shaderName = ''
  #
  # copy
  #
  def copy ( self ) :
    if DEBUG_MODE : print '>> RSLNode( %s ).copy' % self.label
    newNode = RSLNode ()
    self.copySetup ( newNode )
    return newNode
  #
  # collectComputed
  #
  def collectComputed ( self, computedCode, visitedNodes, CodeOnly = False ) :
    #    
    self.computedInputParamsList = []
    self.computedOutputParamsList = []
    self.computedLocalParamsList = []    
    self.computedIncludesList = []

    for param in self.inputParams :
      ( srcNode, srcParam ) = self.getLinkedSrcNode ( param )
      if srcNode is not None :
        if not srcNode in visitedNodes :
          computedCode = srcNode.collectComputed ( computedCode, visitedNodes, CodeOnly )

          self.computedInputParamsList = srcNode.computedInputParamsList + self.computedInputParamsList
          self.computedLocalParamsList = srcNode.computedLocalParamsList + self.computedLocalParamsList
          self.computedOutputParamsList += srcNode.computedOutputParamsList
          self.computedIncludesList += srcNode.computedIncludesList
      else :
        if param.shaderParam :
          self.computedInputParamsList.append ( ( param, self ) ) # += declare
        else :
          self.computedLocalParamsList.append ( ( param, self ) ) # += declare

    for param in self.outputParams :
      if not param.type in ['rib', 'surface', 'displacement', 'light', 'volume'] :
        if param.provider == 'primitive' or param.shaderParam :
          self.computedOutputParamsList.append ( ( param, self ) ) # += ( 'output ' + declare )
        else :
          self.computedLocalParamsList.append ( ( param, self ) ) # += declare

    for inc_name in self.includes :
      self.computedIncludesList.append ( inc_name )

    visitedNodes.add ( self )

    if self.code is not None :
      node_code = str ( self.parseLocalVars ( self.code ) )
  
      if self.type in [ 'surface', 'displacement', 'light', 'volume' ] :
        # find begin block position '{' for inserting computed code
        block_begin_pos = 0
        parserStart = 0
        parserPos = 0
  
        while parserPos != -1 :
          parserPos = node_code.find ( '{', parserStart )
          if parserPos != -1 :
            # skip global vars case defined as ${VARNAME}
            if node_code[ parserPos-1:parserPos ] != '$' :
              block_begin_pos = parserPos + 1
              break
            parserStart = parserPos + 1
  
        #print '> Code insert position = %d' % block_begin_pos
        #print '> insert code at %s' % node_code[ block_begin_pos: ]
  
        begin_code = node_code [ 0:block_begin_pos ]
        end_code = node_code[ block_begin_pos + 1 : ]
  
        shaderCode = self.getHeader () 
        shaderCode += begin_code + '\n' 
        shaderCode += self.getComputedLocals ()
        shaderCode += computedCode
        shaderCode += end_code
      else :
        shaderCode = computedCode + self.getHeader () + node_code      
        
    return shaderCode
  #
  # RSL specific parser
  #
  def parseLocalVars ( self, parsedStr ) :
    #
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
            ( srcNode, srcParam ) = self.getLinkedSrcNode ( param )
            if srcNode is not None :
              resultStr += srcNode.getParamName ( srcParam )
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
  #
  # getComputedInputParams
  #
  def getComputedInputParams ( self ) :
    #
    params_str = ''
    for ( param, node ) in self.computedInputParamsList :
      params_str += node.getParamDeclaration ( param )
    return params_str
  #
  # getComputedOutputParams
  #
  def getComputedOutputParams ( self ) :
    #
    params_str = ''
    for ( param, node ) in self.computedOutputParamsList :
      params_str += 'output ' + node.getParamDeclaration ( param )
    return params_str
  #
  # getComputedLocals
  #
  def getComputedLocals ( self ) :
    #
    params_str = ''
    for ( param, node ) in self.computedLocalParamsList :
      params_str += node.getParamDeclaration ( param )
    return params_str
  #
  # getHeader
  #
  def getHeader ( self ) :
    #
    if self.type in VALID_RSL_SHADER_TYPES :     
      rslHeader =  '/*\n'
      rslHeader += ' * %s\n' % ( self.getInstanceName () + '.sl' )
      rslHeader += ' * Generated by meShaderEd ver.${version}\n' 
      rslHeader += ' */\n\n'
      # includes are stored in set to prevent duplication
      for include in set ( self.computedIncludesList ) :
        rslHeader += '#include \"' + include + '\"\n'
    else :
      rslHeader = '\n'
      rslHeader +=  '/*\n'
      rslHeader += ' * RSL code node: %s (%s)\n' % ( self.label,  self.name )
      rslHeader += ' */\n' 
    
    return rslHeader
  #
  # getComputedCode
  #
  def getComputedCode ( self, CodeOnly = False ) :
    #
    computedCode = ''
    
    self.execControlCode ()

    self.visitedNodes = set ()

    computedCode = self.collectComputed ( computedCode, self.visitedNodes, CodeOnly )
    computedCode = self.parseGlobalVars ( computedCode )
    
    return computedCode     
  #
  # writeShader
  #
  def writeShader ( self, shaderCode, shaderName ) :
    #
    self.shaderName = normPath ( shaderName )
    f = open ( self.shaderName, 'w+t' )
    f.write ( shaderCode )
    f.close ()
  #
  # compileShader
  #
  def compileShader ( self, compileDir = '' ) :
    #
    from meShaderEd import app_renderer
  
    compiler =  app_global_vars [ 'ShaderCompiler' ]
    defines_str = app_global_vars [ 'ShaderDefines' ]
    includes_str = app_global_vars [ 'IncludePath' ]

    shaderCmd = [ compiler ]

    if includes_str != '' :
      includes_lst = includes_str.split ( ',' )
      for include in includes_lst :
        shaderCmd.append ( '-I' + include.strip () )

    if defines_str != '' :
      defines_lst = defines_str.split( ',' )
      for define in defines_lst :
        shaderCmd.append ( '-D' + define.strip () )
  
    shaderCmd.append ( self.shaderName )

    if compileDir == '' : compileDir = app_global_vars[ 'ProjectShaders' ]
    os.chdir ( compileDir )

    print '>> RSLNode shaderCmd = %s' %  ' '.join ( shaderCmd )
    print '>> compileDir = %s' % compileDir

    from core.meCommon import launchProcess

    launchProcess ( shaderCmd )
    
  #
  # computeNode
  #
  def computeNode ( self, CodeOnly = False ) :
    #
    print '>> RSLNode (%s).computeNode CodeOnly = %s' % ( self.label, CodeOnly )
    #
    shaderCode = self.getComputedCode ()
   
    if shaderCode != '' and not CodeOnly :
        
      shaderName = os.path.join ( app_global_vars [ 'ProjectSources' ], self.getInstanceName () + '.sl' )      
      self.writeShader ( shaderCode, shaderName )
      self.compileShader ()
      
    return self.shaderName

