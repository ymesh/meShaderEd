#===============================================================================
# nodeNamesEditor.py.py
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

from ui_nodeNamesEditor import Ui_NodeNamesEditor
#
#
#
class NodeNamesEditor ( QtGui.QWidget ):
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
    self.ui = Ui_NodeNamesEditor ( )
    self.ui.setupUi ( self )
    
  #
  #
  def onAddItem ( self ) :
    print '>> NodeNamesEditor: onAddItem'
    self.emit( QtCore.SIGNAL( "addItem" ) ) 
    
  #
  #
  def onRemoveItem ( self ) :
    print '>> NodeNamesEditor: onRemoveItem'
    self.emit( QtCore.SIGNAL( "removeItem" ) )