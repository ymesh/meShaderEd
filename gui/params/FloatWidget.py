"""

	FloatWidget.py

"""
import math
from decimal import *

from core.mePyQt import QtGui, QtCore
from core.signal import Signal

import gui.ui_settings as UI 
from paramWidget import ParamWidget 

if QtCore.QT_VERSION < 50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# FloatWidget
#
class FloatWidget ( ParamWidget ) :
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		if not self.ignoreSubtype :
			if self.param.subtype == 'selector': 
				self.ui = Ui_FloatWidget_selector()
			elif self.param.subtype == 'switch': 
				self.ui = Ui_FloatWidget_switch()
			elif self.param.subtype == 'slider' or self.param.subtype == 'vslider' : 
				self.ui = Ui_FloatWidget_slider()
			else:
				self.ui = Ui_FloatWidget_field() 
		else :
			self.ui = Ui_FloatWidget_field() 
				 
		self.ui.setupUi ( self )
#
# Ui_FloatWidget_field
#          
class Ui_FloatWidget_field ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, FloatWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		self.widget = FloatWidget
		
		self.floatEdit = QtModule.QLineEdit ( FloatWidget )
		
		self.floatEdit.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
		self.floatEdit.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		spacer = QtModule.QSpacerItem ( 20, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		
		hl.addWidget ( self.floatEdit )
		hl.addItem ( spacer )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( FloatWidget )
		self.connectSignals ( FloatWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, FloatWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			FloatWidget.connect ( self.floatEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
		else :
			self.floatEdit.editingFinished.connect ( self.onFloatEditEditingFinished )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, FloatWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			FloatWidget.disconnect ( self.floatEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
		else :
			self.floatEdit.editingFinished.disconnect ( self.onFloatEditEditingFinished )
	#
	# onFloatEditEditingFinished
	#
	def onFloatEditEditingFinished ( self ) :
		#
		floatStr = self.floatEdit.text ()
		if QtCore.QT_VERSION < 50000 :
			floatValue = floatStr.toFloat () [0]
		else :
			floatValue = float ( floatStr )
		self.widget.param.setValue ( floatValue )
		# self.widget.param.paramChanged ()
	#
	# updateGui
	#
	def updateGui ( self, value ) :
		#
		if QtCore.QT_VERSION < 50000 : 
			self.floatEdit.setText ( QtCore.QString.number(value, 'f', 3) )
		else :
			self.floatEdit.setText ( str ( value ) )
#
# Ui_FloatWidget_switch
#          
class Ui_FloatWidget_switch ( object ) :
	#
	# setupUi
	def setupUi ( self, FloatWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		self.widget = FloatWidget
		
		self.checkBox = QtModule.QCheckBox ( FloatWidget )
		
		self.checkBox.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
		self.checkBox.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
		spacer = QtGui.QSpacerItem ( 20, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		
		hl.addWidget ( self.checkBox )
		hl.addItem ( spacer )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( FloatWidget )
		self.connectSignals ( FloatWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, FloatWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			FloatWidget.connect ( self.checkBox, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onStateChanged )
		else :
			self.checkBox.stateChanged.connect ( self.onStateChanged )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, FloatWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			FloatWidget.disconnect ( self.checkBox, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onStateChanged )
		else :
			self.checkBox.stateChanged.disconnect ( self.onStateChanged )
	# 
	# onStateChanged
	#    
	def onStateChanged ( self, value ) :
		#
		floatValue = self.checkBox.isChecked ()    
		self.widget.param.setValue ( floatValue )
	#
	# updateGui
	#      
	def updateGui ( self, value ) : 
		#
		self.checkBox.setChecked ( value != 0 )  
#
# Ui_FloatWidget_selector
#          
class Ui_FloatWidget_selector ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, FloatWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		self.widget = FloatWidget
		
		self.selector = QtModule.QComboBox ( FloatWidget )
		self.selector.setEditable ( False )
		self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
		self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
		
		rangeList = self.widget.param.getRangeValues ()
		for ( label, value ) in rangeList :
			self.selector.addItem ( label, float( value ) )
		
		spacer = QtModule.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		
		hl.addWidget ( self.selector )
		hl.addItem ( spacer )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( FloatWidget )
		self.connectSignals ( FloatWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, FloatWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			FloatWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			self.selector.activated.connect ( self.onCurrentIndexChanged )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, FloatWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			FloatWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			self.selector.activated.disconnect ( self.onCurrentIndexChanged )
	#
	# onCurrentIndexChanged
	#
	def onCurrentIndexChanged ( self, idx ) :
		#
		( floatValue, ok ) = self.selector.itemData ( idx ).toFloat ()
		self.widget.param.setValue ( float ( floatValue ) )
	#
	# updateGui
	#
	def updateGui ( self, setValue ) :
		# 
		currentIdx = -1
		i = 0
		rangeList = self.widget.param.getRangeValues ()
		for ( label, value ) in rangeList :
			if setValue == value : 
				currentIdx = i
				break
			i += 1
		self.selector.setCurrentIndex ( currentIdx )
#
# Ui_FloatWidget_slider
#          
class Ui_FloatWidget_slider ( object ) :
	#
	# getRangeMultiplier
	#
	def getRangeMultiplier ( self, floatStep ) :
		# 
		multiplier = 1.0
		value = float ( floatStep )
		while not value.is_integer () :
			value *= 10.0
			multiplier *= 10.0
		
		return multiplier
	#
	# setupUi
	#
	def setupUi ( self, FloatWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		hl.setStretch ( 1, 1 )
		
		self.widget = FloatWidget
		
		self.floatEdit = QtModule.QLineEdit( FloatWidget )
		
		self.floatEdit.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
		self.floatEdit.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		
		self.slider = QtModule.QSlider ( QtCore.Qt.Horizontal, FloatWidget )
		
		floatMinVal = 0
		floatMaxVal = 1
		floatStep = 0.1
		
		rangeList = self.widget.param.getRangeValues ()
		if len ( rangeList ) :
			floatMinVal = rangeList [ 0 ]
			floatMaxVal = rangeList [ 1 ]
			floatStep = rangeList [ 2 ]
		
		if floatStep == 0.0 : floatStep = 0.1

		multiplier = self.getRangeMultiplier ( floatStep )
		
		intMinVal = int ( floatMinVal * multiplier )
		intMaxVal = int ( floatMaxVal * multiplier )
		intStep = int ( floatStep * multiplier )
		
		self.slider.setRange ( intMinVal, intMaxVal )
		self.slider.setSingleStep ( intStep )
		
		self.slider.setValue ( int ( self.widget.param.value * multiplier ) )

		hl.addWidget ( self.floatEdit )
		hl.addWidget ( self.slider )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( FloatWidget )
		self.connectSignals ( FloatWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, FloatWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			FloatWidget.connect ( self.floatEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
			FloatWidget.connect ( self.slider, QtCore.SIGNAL ( 'valueChanged(int)' ), self.onSliderValueChanged )
		else :
			self.floatEdit.editingFinished.connect ( self.onFloatEditEditingFinished )
			self.slider.valueChanged.connect ( self.onSliderValueChanged )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, FloatWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			FloatWidget.disconnect ( self.floatEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
			FloatWidget.disconnect ( self.slider, QtCore.SIGNAL ( 'valueChanged(int)' ), self.onSliderValueChanged )
		else :
			self.floatEdit.editingFinished.disconnect ( self.onFloatEditEditingFinished )
			self.slider.valueChanged.disconnect ( self.onSliderValueChanged )
	#
	# onFloatEditEditingFinished
	#
	def onFloatEditEditingFinished ( self ) :
		#
		floatStr = self.floatEdit.text ()
		floatValue = floatStr.toFloat () [ 0 ] 
		self.widget.param.setValue ( floatValue )       
		
		floatMinVal = 0
		floatMaxVal = 1
		floatStep = 0.1
		
		rangeList = self.widget.param.getRangeValues ()
		if len ( rangeList ) :
			floatMinVal = rangeList [ 0 ]
			floatMaxVal = rangeList [ 1 ]
			floatStep = rangeList [ 2 ]
		
		if floatStep == 0.0 : floatStep = 0.1
		
		multiplier = self.getRangeMultiplier ( floatStep )
			
		intMinVal = int ( floatMinVal * multiplier )
		intMaxVal = int ( floatMaxVal * multiplier )
		intStep = int ( floatStep * multiplier )
		
		self.slider.setValue ( int ( floatValue * multiplier ) )
	#
	# onSliderValueChanged
	#
	def onSliderValueChanged ( self, value ) :
		#
		intValue = value #self.slider.value ()
		
		floatMinVal = 0
		floatMaxVal = 1
		floatStep = 0.1
		
		rangeList = self.widget.param.getRangeValues ()
		if len ( rangeList ) :
			floatMinVal = rangeList [ 0 ]
			floatMaxVal = rangeList [ 1 ]
			floatStep = rangeList [ 2 ]
		
		if floatStep == 0.0 : floatStep = 0.1
		
		multiplier = self.getRangeMultiplier ( floatStep ) 
		
		floatValue = float ( intValue ) / float ( multiplier )
		self.widget.param.setValue ( floatValue )
		self.updateGui ( floatValue ) 
	#
	# updateGui
	#
	def updateGui ( self, value ) : 
		#
		if QtCore.QT_VERSION < 50000 : 
			self.floatEdit.setText ( QtCore.QString.number ( value, 'f', 3 ) )
		else :
			self.floatEdit.setText ( str ( value ) )
