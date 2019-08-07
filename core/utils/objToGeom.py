#===============================================================================
# objToGeom.py
#===============================================================================
import os, sys
from PyQt4 import QtCore

from global_vars import app_global_vars, DEBUG_MODE
from objReader import ObjReader

#
# ObjToGeom
#
class ObjToGeom ( ObjReader ) :
    #
    # __init__
    #
    def __init__ ( self, objFileName = None ) :
        #
        ObjReader.__init__ ( self, objFileName )
        
        self.geom = None

    #
    # readObj
    #
    def readObj ( self ) :
        #
        if DEBUG_MODE : print '>> ObjToGeom.readObj ( %s )' % self.objFileName