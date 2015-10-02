"""

 PointWidget.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

import gui.ui_settings as UI 
from paramWidget import ParamWidget

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# PointWidget
#
class PointWidget ( ParamWidget ) :
	#
	# PointWidget
	#
	def buildGui ( self ) :
		#
		self.ui = Ui_PointWidget_field () 
		self.ui.setupUi ( self )
#
# Ui_PointWidget_field
#          
class Ui_PointWidget_field ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, PointWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		self.widget = PointWidget
		
		self.floatEdit0 = QtModule.QLineEdit ( PointWidget )
		self.floatEdit1 = QtModule.QLineEdit ( PointWidget )
		self.floatEdit2 = QtModule.QLineEdit ( PointWidget )
		
		self.floatEdit0.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
		self.floatEdit1.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		self.floatEdit2.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		
		self.floatEdit0.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		self.floatEdit1.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		self.floatEdit2.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		
		self.selector = QtModule.QComboBox ( PointWidget )
		self.selector.setEditable ( False )
		#self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
		self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
		
		for label in [ "current", "shader", "object", "camera", "world", "raster", "NDC", "screen" ] :
			self.selector.addItem ( label )
		if self.widget.param.space != None :
			self.selector.setCurrentIndex ( self.selector.findText ( self.widget.param.space ) )  
		
		spacer = QtModule.QSpacerItem ( 20, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		
		hl.addWidget ( self.floatEdit0 )
		hl.addWidget ( self.floatEdit1 )
		hl.addWidget ( self.floatEdit2 )
		hl.addWidget ( self.selector )
		hl.addItem ( spacer )
		
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( PointWidget )
		self.connectSignals ( PointWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, PointWidget ) :
		#
		if usePyQt4 :
			PointWidget.connect ( self.floatEdit0, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
			PointWidget.connect ( self.floatEdit1, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
			PointWidget.connect ( self.floatEdit2, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
			PointWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			self.floatEdit0.editingFinished.connect ( self.onFloatEditEditingFinished )
			self.floatEdit1.editingFinished.connect ( self.onFloatEditEditingFinished )
			self.floatEdit2.editingFinished.connect ( self.onFloatEditEditingFinished )
			self.selector.activated.connect ( self.onCurrentIndexChanged ) 
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, PointWidget ) :
		#
		if usePyQt4 :
			PointWidget.disconnect ( self.floatEdit0, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
			PointWidget.disconnect ( self.floatEdit1, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
			PointWidget.disconnect ( self.floatEdit2, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
			PointWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			self.floatEdit0.editingFinished.disconnect ( self.onFloatEditEditingFinished )
			self.floatEdit1.editingFinished.disconnect ( self.onFloatEditEditingFinished )
			self.floatEdit2.editingFinished.disconnect ( self.onFloatEditEditingFinished )
			self.selector.activated.disconnect ( self.onCurrentIndexChanged )  
	#
	# onFloatEditEditingFinished
	#
	def onFloatEditEditingFinished ( self ) :
		#
		floatStr0 = self.floatEdit0.text ()
		floatStr1 = self.floatEdit1.text ()
		floatStr2 = self.floatEdit2.text ()
		f0 = floatStr0.toFloat ()[0]
		f1 = floatStr1.toFloat ()[0] 
		f2 = floatStr2.toFloat ()[0]
		
		self.widget.param.setValue ( [ f0, f1, f2 ] )
	#
	# onCurrentIndexChanged
	#
	def onCurrentIndexChanged ( self, idx ) :
		#
		space = str ( self.selector.currentText () ) 
		if space == 'current' : space = None
		self.widget.param.space = space
	#
	# updateGui
	#
	def updateGui ( self, value ) : 
		#
		if usePyQt4 :
			self.floatEdit0.setText ( QtCore.QString.number( value [0], 'f', 3 ) )
			self.floatEdit1.setText ( QtCore.QString.number( value [1], 'f', 3 ) )
			self.floatEdit2.setText ( QtCore.QString.number( value [2], 'f', 3 ) )
		else :
			self.floatEdit0.setText ( str ( value [0] ) )
			self.floatEdit1.setText ( str ( value [1] ) )
			self.floatEdit2.setText ( str ( value [2] ) )
