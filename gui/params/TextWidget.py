"""

 TextWidget.py
 
"""
from core.mePyQt import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget

if QtCore.QT_VERSION < 50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# TextWidget
#
class TextWidget ( ParamWidget ) :
	#
	# buildGui
	#                
	def buildGui ( self ) :
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
		hl = QtModule.QHBoxLayout ()
		hl.setStretch ( 1, 1 )
		
		self.widget = TextWidget
		self.text_plainTextEdit = QtModule.QPlainTextEdit ( TextWidget )
		self.text_plainTextEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) )
		self.text_plainTextEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT * 4 ) )
				
		self.doc = QtGui.QTextDocument ()
		self.doc.setPlainText ( '' )
		layout = QtModule.QPlainTextDocumentLayout ( self.doc )
		self.doc.setDocumentLayout ( layout )
		self.text_plainTextEdit.setDocument ( self.doc )  
		
		hl.addWidget ( self.text_plainTextEdit )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( TextWidget )
		self.connectSignals ( TextWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, TextWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			TextWidget.connect ( self.text_plainTextEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onTextEditEditingFinished )
		else :
			self.text_plainTextEdit.textChanged.connect ( self.onTextEditEditingFinished )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, TextWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			TextWidget.disconnect ( self.text_plainTextEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onTextEditEditingFinished )
		else :
			self.text_plainTextEdit.textChanged.connect ( self.onTextEditEditingFinished )
	#
	# onTextEditEditingFinished
	#                     
	def onTextEditEditingFinished ( self ) :
		#
		stringValue = self.text_plainTextEdit.toPlainText ()
		self.widget.param.setValue ( stringValue )
	#
	# updateGui
	#     
	def updateGui ( self, value ) :
		# 
		self.doc.setPlainText ( value )
		self.text_plainTextEdit.setDocument ( self.doc )  


