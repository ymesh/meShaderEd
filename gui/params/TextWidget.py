#===============================================================================
# TextWidget.py
#
# 
#
#===============================================================================
from PyQt4 import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget 
#
# TextWidget
#
class TextWidget ( ParamWidget ) :
  #
  # buildGui
  #                
  def buildGui ( self ):
    #
    self.ui = Ui_TextWidget_field ()    
    self.ui.setupUi ( self )
#
# Ui_StringWidget_field
#
class Ui_TextWidget_field ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, TextWidget ) :
    #
    self.widget = TextWidget
    self.text_plainTextEdit = QtGui.QPlainTextEdit ( TextWidget )
    self.text_plainTextEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) )
    self.text_plainTextEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT * 4 ) )
        
    self.doc = QtGui.QTextDocument ()
    self.doc.setPlainText ( '' )
    layout = QtGui.QPlainTextDocumentLayout ( self.doc )
    self.doc.setDocumentLayout ( layout )
    self.text_plainTextEdit.setDocument ( self.doc )  
    
    self.widget.hl.addWidget ( self.text_plainTextEdit )
    self.widget.hl.setStretch ( 1, 1 )
    
    QtCore.QMetaObject.connectSlotsByName ( TextWidget )
    self.connectSignals ( TextWidget )
  #
  # connectSignals
  #
  def connectSignals ( self, TextWidget ) :
    TextWidget.connect ( self.text_plainTextEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onTextEditEditingFinished )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, TextWidget ) :
    TextWidget.disconnect ( self.text_plainTextEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onTextEditEditingFinished )
  #
  # onTextEditEditingFinished
  #                     
  def onTextEditEditingFinished ( self ) :
    stringValue = self.text_plainTextEdit.toPlainText ()
    self.widget.param.setValue ( stringValue )
  #
  # updateGui
  #     
  def updateGui ( self, value ) : 
    self.doc.setPlainText ( value )
    self.text_plainTextEdit.setDocument ( self.doc )  


