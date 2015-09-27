"""

 IntWidget.py

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
# IntWidget
#
class IntWidget ( ParamWidget ) :
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		if not self.ignoreSubtype :
			if self.param.subtype == 'selector' : 
				self.ui = Ui_IntWidget_selector ()
			elif self.param.subtype == 'switch' : 
				self.ui = Ui_IntWidget_switch ()
			elif self.param.subtype == 'slider' or self.param.subtype == 'vslider' : 
				self.ui = Ui_IntWidget_slider ()
			else:
				self.ui = Ui_IntWidget_field () 
		else :
			self.ui = Ui_IntWidget_field () 
				 
		self.ui.setupUi ( self )
#
# Ui_IntWidget_field
#          
class Ui_IntWidget_field ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, IntWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		self.widget = IntWidget
		
		self.intEdit = QtModule.QLineEdit ( IntWidget )
		
		self.intEdit.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		self.intEdit.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		spacer = QtModule.QSpacerItem ( 20, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		
		hl.addWidget ( self.intEdit )
		hl.addItem ( spacer )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( IntWidget )
		self.connectSignals ( IntWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, IntWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			IntWidget.connect ( self.intEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onIntEditEditingFinished )
		else :
			self.intEdit.editingFinished.connect ( self.onIntEditEditingFinished )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, IntWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			IntWidget.disconnect ( self.intEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onIntEditEditingFinished )
		else :
			self.intEdit.editingFinished.disconnect ( self.onIntEditEditingFinished )
	#
	#  onIntEditEditingFinished
	#
	def onIntEditEditingFinished ( self ) :
		#
		intStr = self.intEdit.text ()
		if QtCore.QT_VERSION < 50000 :
			intValue = intStr.toInt () [ 0 ] 
		else :
			intValue = int ( intStr )
		self.widget.param.setValue (  intValue )      
	#
	# updateGui
	def updateGui ( self, value ):
		#
		if QtCore.QT_VERSION < 50000 : 
			self.intEdit.setText ( QtCore.QString.number ( value ) )
		else :
			self.intEdit.setText ( str ( value ) )
#
# Ui_IntWidget_switch
#          
class Ui_IntWidget_switch ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, IntWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		self.widget = IntWidget
		
		self.checkBox = QtModule.QCheckBox ( IntWidget )
		
		self.checkBox.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) ) 
		self.checkBox.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
		spacer = QtModule.QSpacerItem ( 20, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		
		hl.addWidget ( self.checkBox )
		hl.addItem ( spacer )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( IntWidget )
		self.connectSignals ( IntWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, IntWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			IntWidget.connect ( self.checkBox, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onStateChanged )
		else :
			self.checkBox.stateChanged.connect ( self.onStateChanged )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, IntWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			IntWidget.disconnect ( self.checkBox, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onStateChanged )
		else :
			self.checkBox.stateChanged.disconnect ( self.onStateChanged )
	# 
	# onStateChanged 
	#
	def onStateChanged ( self, value ) :
		#
		intValue = self.checkBox.isChecked ()    
		self.widget.param.setValue ( intValue )
	#
	# updateGui
	#
	def updateGui ( self, value ) : 
		#
		self.checkBox.setChecked ( value != 0 )  
#
# Ui_IntWidget_selector
#          
class Ui_IntWidget_selector ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, IntWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		self.widget = IntWidget
		
		self.selector = QtModule.QComboBox ( IntWidget )
		self.selector.setEditable ( False )
		self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
		self.selector.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.COMBO_HEIGHT ) )
		
		rangeList = self.widget.param.getRangeValues ()
		
		for ( label, value ) in rangeList : self.selector.addItem ( label, int( value ) )
		
		spacer = QtModule.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		
		hl.addWidget ( self.selector )
		hl.addItem ( spacer )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( IntWidget )
		self.connectSignals ( IntWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, IntWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			IntWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			self.selector.activated.connect ( self.onCurrentIndexChanged ) 
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, IntWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			IntWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			self.selector.activated.disconnect ( self.onCurrentIndexChanged ) 
	#
	# onCurrentIndexChanged
	#
	def onCurrentIndexChanged ( self, idx ) :
		#
		if QtCore.QT_VERSION < 50000 :
			( intValue, ok ) = self.selector.itemData ( idx ).toInt ()
		else :
			intValue = self.selector.itemData ( idx )
		self.widget.param.setValue ( int ( intValue ) )
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
# Ui_IntWidget_slider
#          
class Ui_IntWidget_slider ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, IntWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		hl.setStretch ( 1, 1 )
		
		self.widget = IntWidget
		
		self.intEdit = QtGui.QLineEdit ( IntWidget )
		
		self.intEdit.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
		self.intEdit.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
		
		self.slider = QtModule.QSlider ( QtCore.Qt.Horizontal, IntWidget )
		
		intMinVal = 0
		intMaxVal = 10
		intStep = 1
		
		rangeList = self.widget.param.getRangeValues ()
		
		if len ( rangeList ) :
			intMinVal = rangeList [ 0 ]
			intMaxVal = rangeList [ 1 ]
			intStep   = rangeList [ 2 ]
		
		if intStep == 0 : intStep = 1
		
		self.slider.setRange ( intMinVal, intMaxVal )
		self.slider.setSingleStep ( intStep )
		
		self.slider.setValue ( int ( self.widget.param.value ) )

		hl.addWidget ( self.intEdit )
		hl.addWidget ( self.slider )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( IntWidget )
		self.connectSignals ( IntWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, IntWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			IntWidget.connect ( self.intEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onIntEditEditingFinished )
			IntWidget.connect ( self.slider, QtCore.SIGNAL ( 'valueChanged(int)' ), self.onSliderValueChanged )
		else :
			self.intEdit.editingFinished.connect ( self.onIntEditEditingFinished )
			self.slider.valueChanged.connect ( self.onSliderValueChanged )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, IntWidget ) :
		#
		if QtCore.QT_VERSION < 50000 :
			IntWidget.disconnect ( self.intEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onIntEditEditingFinished )
			IntWidget.disconnect ( self.slider, QtCore.SIGNAL ( 'valueChanged(int)' ), self.onSliderValueChanged )
		else :
			self.intEdit.editingFinished.disconnect ( self.onIntEditEditingFinished )
			self.slider.valueChanged.disconnect ( self.onSliderValueChanged )
	#
	# onIntEditEditingFinished
	#
	def onIntEditEditingFinished ( self ) :
		#
		intStr = self.intEdit.text ()
		if QtCore.QT_VERSION < 50000 :
			intValue = intStr.toInt () [ 0 ] 
		else :
			intValue = int ( intStr )
		self.widget.param.setValue ( intValue )    
		self.slider.setValue ( intValue )
	#
	# onSliderValueChanged
	#
	def onSliderValueChanged ( self, value ) :
		#
		self.widget.param.setValue ( value )
		self.updateGui ( value) 
		#self.widget.param.paramChanged ()
	#
	# updateGui
	#
	def updateGui ( self, value ) :
		# 
		if QtCore.QT_VERSION < 50000 :
			self.intEdit.setText ( QtCore.QString.number ( value ) )
		else :
			self.intEdit.setText ( str ( value ) ) 
