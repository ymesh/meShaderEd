#===============================================================================
# swatch.py
#
#
#
#===============================================================================
import os, sys
from PyQt4 import QtCore

from global_vars import app_global_vars, DEBUG_MODE
from core.node_global_vars import node_global_vars
import gui.ui_settings as UI
#
# Node
#
class SwatchInfo ( QtCore.QObject ) :
  #
  # __init__
  #
  def __init__ ( self, node = None, param = None ) :
    #
    QtCore.QObject.__init__( self )

    self.enabled = False
    
    self.type = 'surface' # displace, volume, light, manifold
    self.node = node
    
    self.param = param # [Color, Opacity], [P,N], [Cl,], [Q, Qdu, Qdv ]  
    
    self.shape = 'sphere' 
    self.scale = 1.0
    self.swatch_size = UI.SWATCH_SIZE
    self.render_size = UI.SWATCH_SIZE
    self.shadingRate = 1.0
    self.raytrace = False
    self.dispbound = 0.1
    self.frame = 1
    self.mode = 'manual' # auto