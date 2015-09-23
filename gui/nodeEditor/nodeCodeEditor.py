"""
 
 nodeCodeEditor.py

 ver. 1.0.0
 Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
 
 Dialog for managing node code
 
"""
from core.mePyQt import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars

import gui.ui_settings as UI
from codeSyntaxHighlighter import CodeSyntaxHighlighter

from ui_nodeCodeEditor import Ui_NodeCodeEditor

if QtCore.QT_VERSION < 50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
	
#
# NodeCodeEditor
#
class NodeCodeEditor ( QtModule.QWidget ):
	#
	# __init__
	#
	def __init__ ( self, parent, editNodeCode = None ) :
		#
		QtModule.QWidget.__init__ ( self, parent )
		
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
	def setNodeCode ( self, editNodeCode, mode = 'SL', readOnly = False ) :
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
			self.ui.textEdit.setFont ( font )
			self.ui.textEdit.setLineWrapMode ( QtGui.QTextEdit.NoWrap )
			self.ui.textEdit.setReadOnly ( readOnly )
		else :
			code = ''
		self.ui.textEdit.setPlainText ( code )
				
				
				
		
