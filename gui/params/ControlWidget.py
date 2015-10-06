"""

 ControlWidget.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI
from paramWidget import ParamWidget

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
	
#
# ControlWidget
#
class ControlWidget ( ParamWidget ) :
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		if not self.ignoreSubtype :
			if self.param.subtype == 'button':
				self.ui = Ui_ControlWidget_button ()
			else:
				self.ui = Ui_ControlWidget_field ()
		else :
			self.ui = Ui_ControlWidget_field ()

		self.ui.setupUi ( self )
#
# Ui_ControlWidget_field
#
class Ui_ControlWidget_field ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, ControlWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		hl.setStretch ( 1, 1 )
		
		self.widget = ControlWidget

		self.stringEdit = QtModule.QLineEdit ( ControlWidget )

		self.stringEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
		self.stringEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )

		hl.addWidget ( self.stringEdit )
		self.widget.param_vl.addLayout ( hl )

		QtCore.QMetaObject.connectSlotsByName ( ControlWidget )
		self.connectSignals ( ControlWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, ControlWidget ) :
		#
		if usePyQt4 :
			ControlWidget.connect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
		else :
			self.stringEdit.editingFinished.connect (  self.onStringEditEditingFinished )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, ControlWidget ) :
		#
		if usePyQt4 :
			ControlWidget.disconnect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
		else :
			self.stringEdit.editingFinished.disconnect (  self.onStringEditEditingFinished )
	#
	# onStringEditEditingFinished
	#
	def onStringEditEditingFinished ( self ) :
		#
		stringValue = self.stringEdit.text ()
		self.widget.param.setValue ( str ( stringValue ) )
	#
	# updateGui
	#
	def updateGui ( self, value ) :
		#
		self.stringEdit.setText ( value )
#
# Ui_ControlWidget_button
#
class Ui_ControlWidget_button ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, ControlWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		hl.setStretch ( 1, 1 )
		
		self.widget = ControlWidget

		self.button = QtModule.QPushButton ( self.widget.param.btext, ControlWidget )
		#self.button.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
		#self.button.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.COMBO_HEIGHT ) )

		spacer = QtModule.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )

		hl.addWidget ( self.button )
		hl.addItem ( spacer )
		self.widget.param_vl.addLayout ( hl )

		QtCore.QMetaObject.connectSlotsByName ( ControlWidget )
		self.connectSignals ( ControlWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, ControlWidget ) :
		#
		if usePyQt4 :
			ControlWidget.connect ( self.button, QtCore.SIGNAL ( 'clicked()' ), self.onClicked )
		else :
			self.button.clicked.connect ( self.onClicked )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, ControlWidget ) :
		#
		if usePyQt4 :
			ControlWidget.disconnect ( self.button, QtCore.SIGNAL ( 'clicked()' ), self.onClicked )
		else :
			self.button.clicked.disconnect ( self.onClicked )
	#
	# onClicked
	#
	def onClicked ( self ) :
		#
		if DEBUG_MODE : print ( '>> Ui_ControlWidget_button.clicked()' )
		self.widget.param.execControlCode ( self.widget.gfxNode.node )
	#
	# updateGui
	#
	def updateGui ( self, value ) :
		#
		pass
		#self.button.setText ( value )
