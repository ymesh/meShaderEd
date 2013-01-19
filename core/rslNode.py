#===============================================================================
# rslNode.py
#
# 
#
#===============================================================================
import os, sys
from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam

from global_vars import app_global_vars, DEBUG_MODE
from core.node_global_vars import node_global_vars

#
# RSL_code
#
class RSL_code ( Node ):
  #
  #
  def __init__ ( self, xml_node = None ):
    #
    Node.__init__ ( self, xml_node )
    #super( FloatNodeParam, self ).__init__ ( xml_param, isRibParam )
    self.shaderName = ''
    #print ">> RSL_code __init__" 
  #
  #
  def copy ( self ):
    if DEBUG_MODE : print '>> RSL_code::copy (%s)' % self.label
    newNode = RSL_code()
    self.copySetup ( newNode )                                
    return newNode 
#
# RSLNode
#
class RSLNode ( Node ):
  #
  #
  def __init__ ( self, xml_node = None ):
    #
    Node.__init__ ( self, xml_node )
    self.shaderName = ''
    #print ">> RSLNode __init__" 
  #
  #
  def copy ( self ):
    if DEBUG_MODE : print '>> RSLNode::copy (%s)' % self.label
    newNode = RSLNode()
    self.copySetup ( newNode )                                
    return newNode 
  #
  #
  def collectComputed ( self, shaderCode, visitedNodes ) :
    #print '>> Node (%s).collectComputed' % self.label
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
        #print '>> Node (%s).collectComputed: local param %s' % ( self.label, declare )
        if param.shaderParam :
          self.computedInputParams += declare
        else :
          self.computedLocalParams += declare 
          
    for param in self.outputParams :
      if not param.type in ['rib', 'surface', 'displacement', 'light', 'volume'] : 
        declare = self.getParamDeclaration ( param )
        if param.provider == 'primitive' : 
          self.computedOutputParams.append( 'output ' + declare )  
        else :
          self.computedLocalParams += declare 
    
    for inc_name in self.includes :      
      self.computedIncludes.append( inc_name )
    #print self.includes
    
    visitedNodes.add ( self )
    
    node_code = str( self.parseLocalVars ( self.code ) )
    
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
      
      shaderCode = begin_code + '\n' + self.computedLocalParams + shaderCode + end_code
    else :
      shaderCode += node_code
    
    return shaderCode  
  
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
  #
  #
  def computeNode ( self ) :
    print '>> RSLNode (%s).computeNode' % self.label
    #
    self.computed_code = ''
    self.execParamCode ()
    
    visitedNodes = set()
    shaderCode = ''
    shaderCode = self.collectComputed ( shaderCode, visitedNodes )
    
    #for node in self.childs :
    #  print '=> %s' % node.label
    
    rslHeader = '/* Generated by meShaderEd */\n\n'
    
    self.shaderName = app_global_vars[ 'ProjectSources' ] + '/' + self.getInstanceName() + '.sl'
    #print '>> RSLNode save file %s' % self.shaderName
    f = open ( self.shaderName, 'w+t' )
    
    # includes are stored in set to prevent duplication 
    for include in set( self.computedIncludes ) :
      rslHeader += '#include \"' + include + '\"\n'
        
    """
    if self.type == 'surface' :
      rslHeader += '#define SURFACE_SHADER %s\n' % self.getInstanceName() 
      rslHeader += 'surface %s ' % self.getInstanceName()
    elif self.type == 'displacement' :
      rslHeader += '#define DISPLACEMENT_SHADER %s\n' % self.getInstanceName() 
      rslHeader += 'displacement %s ' % self.getInstanceName()
    
    rslHeader += '(\n'
    
    rslHeader += self.parseGlobalVars ( self.computedInputParams )
    #rslHeader += self.parseGlobalVars ( self.computedOutputParams )
    # output parameters are stored in set to prevent duplication 
    for out_param in set( self.computedOutputParams ) :
      rslHeader += out_param
    
    rslHeader += ')\n'
    rslHeader += '{\n'
    rslHeader += self.parseGlobalVars ( self.computedLocalParams )
    """
    
    rslCode = self.parseGlobalVars ( shaderCode )
    
    #rslCode += '\n}\n'
    
    f.write ( rslHeader + rslCode )
    f.close ()

    from meShaderEd import app_renderer
    
    compiler =  app_global_vars[ 'ShaderCompiler' ]
    defines_str = app_global_vars[ 'ShaderDefines' ]
    includes_str = app_global_vars[ 'IncludePath' ]

    shaderCmd = [ compiler ]
    
    if includes_str != '' :  
      includes_lst = includes_str.split( ',' )
      for include in includes_lst :
        shaderCmd.append ( '-I' + include.strip() )    
    
    if defines_str != '' :  
      defines_lst = defines_str.split( ',' )
      for define in defines_lst :
        shaderCmd.append ( '-D' + define.strip() )  
      
    shaderCmd.append ( self.shaderName )
    
    os.chdir (  app_global_vars[ 'ProjectShaders' ] )

    print '>> RSLNode shaderCmd = %s' %  ' '.join( shaderCmd ) 
    print '>> ProjectShaders = %s' %  app_global_vars[ 'ProjectShaders' ] 

    from core.meCommon import launchProcess
    
    launchProcess ( shaderCmd )
    
    return self.getInstanceName()
      
