#===============================================================================
# objToRib.py
#===============================================================================
import os, sys
from PyQt4 import QtCore

from global_vars import app_global_vars, DEBUG_MODE
from objReader import ObjReader

#
# ObjToRib
#
class ObjToRib ( ObjReader ) :
  #
  # __init__
  #
  def __init__ ( self, objFileName = None ) :
    #
    ObjReader.__init__ ( self, objFileName )
    
    self.rib = None
  #
  # readObjFile
  #
  def readObjFile ( self ) :
    #
    if DEBUG_MODE : print '>> ObjToRib.readObjFile ( %s )' % self.objFileName
