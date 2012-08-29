#===============================================================================
# nodeEditor.py.py
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

from core.node import Node

from ui_nodeEditor import Ui_NodeEditor
#
#
#
class NodeEditor ( QtGui.QWidget ):
  #
  #
  def __init__ ( self, parent, editNode = None ):
    QtGui.QDialog.__init__(self)

    self.editNode = editNode
          
    #self.debugPrint()
    self.buildGui()
  #
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_NodeEditor ( )
    self.ui.setupUi ( self )
    if self.editNode is not None :
      if self.editNode.name != None : self.ui.name_lineEdit.setText ( self.editNode.name ) 
      if self.editNode.label != None : self.ui.label_lineEdit.setText ( self.editNode.label )
      if self.editNode.author != None : self.ui.author_lineEdit.setText ( self.editNode.author )  
      if self.editNode.master != None : self.ui.master_lineEdit.setText ( self.editNode.master ) 
      if self.editNode.icon != None : self.ui.icon_lineEdit.setText ( self.editNode.icon )
      if self.editNode.help != None : 
        doc = QtGui.QTextDocument ()
        doc.setPlainText ( self.editNode.help )
        self.ui.help_plainTextEdit.setDocument ( doc )  
      
      self.ui.id_lineEdit.setText ( str( self.editNode.id ) ) 
      
      self.ui.type_comboBox.setEditable ( False )
      self.ui.type_comboBox.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
      self.ui.type_comboBox.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
      
      currentIdx = -1
      i = 0
      for label in ['rib', 'rib_code', 'rsl_code', 'image', 'surface', 'displacement', 'light', 'volume' ]  :
        self.ui.type_comboBox.addItem ( label )
        if label == self.editNode.type : 
          currentIdx = i
        i += 1
      self.ui.type_comboBox.setCurrentIndex( currentIdx )
      
    
