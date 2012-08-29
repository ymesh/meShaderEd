#===============================================================================
# nodeCodeEditor.py
#
# ver. 1.0.0
# Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
# 
# Dialog for managing node code
# 
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars

import gui.ui_settings as UI

from ui_nodeCodeEditor import Ui_NodeCodeEditor
#
#
#
class NodeCodeEditor ( QtGui.QWidget ):
  #
  #
  def __init__ ( self, parent, editNode = None, codeType = None ):
    QtGui.QDialog.__init__ ( self )
    
    self.editNode = editNode
    self.codeType = codeType      
    #self.debugPrint()
    self.buildGui()
  #
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_NodeCodeEditor ( )
    self.ui.setupUi ( self )
    if self.editNode is not None :
      if self.codeType is not None :
        doc = QtGui.QTextDocument ()
        
        textCharFormat = QtGui.QTextCharFormat ()
        textCharFormat.setFontFixedPitch ( True )
        
        self.ui.textEdit.setCurrentCharFormat ( textCharFormat )
        
        codeText = None
        if self.codeType == 'code' : 
          codeText = self.editNode.code
        elif self.codeType == 'param_code' :
          codeText = self.editNode.param_code
        
        if codeText is not None :
          doc.setPlainText ( codeText )
        
        self.ui.textEdit.setDocument ( doc )  
        self.ui.textEdit.setTabStopWidth ( UI.TAB_SIZE )
        
    
