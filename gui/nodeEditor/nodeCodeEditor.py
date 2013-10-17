"""
 
 nodeCodeEditor.py

 ver. 1.0.0
 Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
 
 Dialog for managing node code
 
"""
import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars

import gui.ui_settings as UI
from gui.codeSyntaxHighlighter import CodeSyntaxHighlighter

from ui_nodeCodeEditor import Ui_NodeCodeEditor
#
# NodeCodeEditor
#
class NodeCodeEditor ( QtGui.QWidget ):
  #
  # __init__
  #
  def __init__ ( self, parent, editNodeCode = None ) :
    #
    QtGui.QWidget.__init__ ( self, parent )
    
    self.editNodeCode = editNodeCode
     
    #self.debugPrint()
    self.buildGui()
  #
  # buildGui
  #
  def buildGui ( self ) :
    # build the gui created with QtDesigner
    self.ui = Ui_NodeCodeEditor ( )
    self.ui.setupUi ( self )
    
  #
  # setNodeCode
  #
  def setNodeCode ( self, editNodeCode, mode = 'SL' ) :
    #
    self.editNodeCode = editNodeCode
    
    if self.editNodeCode is not None : 
      code = self.editNodeCode
      
      doc = QtGui.QTextDocument ()
      
      font = QtGui.QFont( 'Monospace' )
      font.setFixedPitch ( True )
      font.setPointSize ( UI.FONT_HEIGHT )
  
      codeSyntax = CodeSyntaxHighlighter ( doc, mode )
      
      self.ui.textEdit.setDocument ( doc )  
      self.ui.textEdit.setTabStopWidth ( UI.TAB_SIZE )
      self.ui.textEdit.setCurrentFont ( font )
      self.ui.textEdit.setLineWrapMode ( QtGui.QTextEdit.NoWrap )
    else :
      code = ''
    self.ui.textEdit.setPlainText ( code )
        
        
        
    
