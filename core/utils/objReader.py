#===============================================================================
# objReader.py
#===============================================================================
import os, sys
from PyQt4 import QtCore

from global_vars import app_global_vars, DEBUG_MODE
from core.geomData import GeomData
#
# ObjReader
#
class ObjReader () :
  #
  # __init__
  #
  def __init__ ( self, objFileName = None ) :
    #
    self.fileName = objFileName

    self.geomData = None
    self.geomGroup = None
    self.material = None

    self.geomGroupList = []

    if self.fileName is not None :
      self.file = open ( self.fileName, 'r' )
      if self.file is not None :
        self.readFile ()
        self.file.close ()

  #
  # readFile
  #
  def readFile ( self ) :
    #
    if DEBUG_MODE : print '>> ObjReader.readFile ( %s )' % self.fileName
    for line in self.file :
      line = line.strip ()
      if line.startswith ( ('#', '$') ) :
        print line
      elif line.startswith ( ('o', 'g') ) :
        tokens = line.split ( ' ' )
        geom_type = tokens [ 0 ]
        geom_name = ''
        if len ( tokens ) > 1 :
          geom_name = tokens [ 1 ]
        print '> %s name = "%s"' % ( geom_type, geom_name )
      else :
        pass
