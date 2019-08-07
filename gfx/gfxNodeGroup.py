"""

 gfxNodeGroup.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui
from core.signal import Signal

from gfx.gfxNode import GfxNode

from global_vars import app_colors, DEBUG_MODE, GFX_NODE_GROUP_TYPE, VALID_RSL_PARAM_TYPES
from meShaderEd import app_settings

import gui.ui_settings as UI

if not usePyQt5 :
    QtModule = QtGui
else :
    from core.mePyQt import QtWidgets
    QtModule = QtWidgets
#
# GfxNode
#
class GfxNodeGroup ( GfxNode ) : 
    #
    Type = GFX_NODE_GROUP_TYPE
    #
    # __init__
    #
    def __init__ ( self, node ) :
        #
        GfxNode.__init__ ( self, node )
        
        self.PenBorderNormal = QtGui.QPen ( 
            QtGui.QBrush ( self.normalColor ),
            3.0,
            QtCore.Qt.SolidLine,
            QtCore.Qt.RoundCap,
            QtCore.Qt.RoundJoin 
        )

        self.PenBorderSelected = QtGui.QPen (
            QtGui.QBrush ( self.selectedColor ),
            3.0,
            QtCore.Qt.SolidLine,
            QtCore.Qt.RoundCap,
            QtCore.Qt.RoundJoin 
        )


