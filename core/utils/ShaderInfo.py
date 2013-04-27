#===============================================================================
# ShaderInfo.py
#===============================================================================
import os, sys
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
      self.get ()
  #
  # get
  #
  def get ( self ) :
    #
    if DEBUG_MODE : print '>> ShaderInfo.get ( %s ) by "%s"' % ( self.fileName, app_global_vars [ 'ShaderInfo' ] )
    # app_global_vars [ 'ShaderCompiler' ]
    # app_global_vars [ 'SLO' ]
    from core.meCommon import launchProcess
    
    cmdList = []
    cmdList.append ( app_global_vars [ 'ShaderInfo' ] )
    cmdList.append ( self.fileName )
    
    tmpDir = app_global_vars [ 'TempPath' ]
    
    stdoutLog = os.path.join ( tmpDir, 'stdout-%s.log' % os.path.basename ( self.fileName ) )
    stderrLog = os.path.join ( tmpDir, 'stderr-%s.log' % os.path.basename ( self.fileName ) )
    
    launchProcess ( cmdList, stdoutLog, stderrLog )
    
    stdout = file ( stdoutLog, 'r' )
    stderr = file ( stderrLog, 'r' )
    
    print '>> %s stdoutLog : %s' % ( app_global_vars [ 'ShaderInfo' ], stdout.read () )
    print '>> %s stderrLog : %s' % ( app_global_vars [ 'ShaderInfo' ], stderr.read () )
    
    stdout.close ()
    stderr.close ()
