#===============================================================================
# nodeParamEditor.py
#
# ver. 1.0.0
# Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
# 
# Dialog for managing node 
# 
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars

import gui.ui_settings as UI

from ui_nodeParamEditor import Ui_NodeParamEditor
#
#
#
class NodeParamEditor ( QtGui.QWidget ):
  #
  #
  def __init__ ( self, parent ):
    QtGui.QDialog.__init__(self)

          
    #self.debugPrint()
    self.buildGui()
  #
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_NodeParamEditor ( )
    self.ui.setupUi ( self )
    
    # correct UI sizes for some controls
    self.ui.check_display.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    self.ui.check_display.setMaximumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    
    self.ui.check_shader.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    self.ui.check_shader.setMaximumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    
  #
  #
  def onAddItem ( self ) :
    print '>> NodeParamEditor: onAddItem'
    self.emit( QtCore.SIGNAL( "addItem" ) ) 
    
  #
  #
  def onRemoveItem ( self ) :
    print '>> NodeParamEditor: onRemoveItem'
    self.emit( QtCore.SIGNAL( "removeItem" ) )