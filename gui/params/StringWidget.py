"""

 StringWidget.py

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
# StringWidget
#
class StringWidget ( ParamWidget ) :
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		if self.param.isArray () :
			self.ui = Ui_StringWidget_array ()
		else :	
			if not self.ignoreSubtype :
				if self.param.subtype == 'selector': 
					self.ui = Ui_StringWidget_selector ()
				elif self.param.subtype == 'file':
					self.ui = Ui_StringWidget_file () 
				else:
					self.ui = Ui_StringWidget_field () 
			else :
				self.ui = Ui_StringWidget_field ()
		self.ui.setupUi ( self )
#
# Ui_StringWidget_field
#
class Ui_StringWidget_field ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, StringWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		hl.setStretch ( 1, 1 )
		
		self.widget = StringWidget
		
		self.stringEdit = QtModule.QLineEdit ( StringWidget )
		
		self.stringEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
		self.stringEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
		
		hl.addWidget ( self.stringEdit )
		self.widget.param_vl.addLayout ( hl )
		
		QtCore.QMetaObject.connectSlotsByName ( StringWidget )
		self.connectSignals ( StringWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, StringWidget ) :
		#
		if  usePyQt4 :
			StringWidget.connect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
		else :
			self.stringEdit.editingFinished.connect ( self.onStringEditEditingFinished )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, StringWidget ) :
		#
		if  usePyQt4 :
			StringWidget.disconnect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
		else :
			self.stringEdit.editingFinished.disconnect ( self.onStringEditEditingFinished )
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
		self.stringEdit.setText ( str ( value ) )

#
# Ui_StringWidget_array
#
class Ui_StringWidget_array ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, StringWidget ) :
		#
		self.widget = StringWidget
		self.labels = []
		self.controls = []
		
		font = QtGui.QFont ()
		labelFontMetric = QtGui.QFontMetricsF ( font )
		label_wi = 0
		char_wi = labelFontMetric.width ( 'x' )
		array_size = self.widget.param.arraySize
		if array_size > 0 :
			label_wi =  char_wi * ( len ( str ( array_size - 1 ) ) + 2 ) # [0]
		
		for i in range ( self.widget.param.arraySize ) :
			self.labels.append ( QtModule.QLabel ( StringWidget ) )
			self.labels [ i ].setMinimumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
			self.labels [ i ].setMaximumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
			self.labels [ i ].setAlignment ( QtCore.Qt.AlignRight )
			self.labels [ i ].setText ( '[' + str ( i ) + ']' )
		
			self.controls.append ( QtModule.QLineEdit ( StringWidget ) )
			self.controls [ i ].setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) )
			self.controls [ i ].setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
			
			hl = QtModule.QHBoxLayout ()
			hl.setStretch ( 0, 0 )
			hl.setStretch ( 1, 1 )
			hl.addWidget ( self.labels [ i ] )
			hl.addWidget ( self.controls [ i ] )
			self.widget.param_vl.addLayout ( hl )
		
		self.connectSignals ( StringWidget )
		QtCore.QMetaObject.connectSlotsByName ( StringWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, StringWidget ) :
		#
		for i in range ( self.widget.param.arraySize ) :
			if  usePyQt4 :
				StringWidget.connect ( self.controls [ i ], QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
			else :
				self.controls [ i ].editingFinished.connect ( self.onStringEditEditingFinished )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, StringWidget ) :
		#
		for i in range ( self.widget.param.arraySize ) :
			if  usePyQt4 :
				StringWidget.disconnect ( self.controls [ i ], QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
			else :
				self.controls [ i ].editingFinished.disconnect ( self.onStringEditEditingFinished )
	#
	# onStringEditEditingFinished
	#
	def onStringEditEditingFinished ( self ) :
		#
		arrayValue = []
		
		for i in range ( self.widget.param.arraySize ) :
			stringValue = self.controls [ i ].text ()
			arrayValue.append ( stringValue )
			
		self.widget.param.setValue ( arrayValue )
	#
	# updateGui
	#
	def updateGui ( self, value ) :
		# 
		for i in range ( self.widget.param.arraySize ) :
			self.controls [ i ].setText ( str ( value [ i ] ) )
#
# Ui_StringWidget_selector
#          
class Ui_StringWidget_selector ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, StringWidget ) :
		#
		
		self.widget = StringWidget
		
		self.selector = QtModule.QComboBox ( StringWidget )
		self.selector.setEditable ( False )
		self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
		self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
		
		rangeList = self.widget.param.getRangeValues ()
		
		for ( label, value ) in rangeList :
			#print "label = %s value = %s" % ( label, value )
			self.selector.addItem ( label, value )
		
		sp = QtModule.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, UI.SP_EXPAND, UI.SP_MIN )
		
		hl = QtModule.QHBoxLayout ()
		hl.addWidget ( self.selector )
		hl.addItem ( sp )
		self.widget.param_vl.addLayout ( hl )
		
		self.connectSignals ( StringWidget )
		QtCore.QMetaObject.connectSlotsByName ( StringWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, StringWidget ) :
		#
		if usePyQt4 :
			StringWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			self.selector.activated.connect ( self.onCurrentIndexChanged )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, StringWidget ) :
		#
		if usePyQt4 :
			StringWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			self.selector.activated.disconnect ( self.onCurrentIndexChanged )
	#
	# onCurrentIndexChanged
	#
	def onCurrentIndexChanged ( self, idx ) :
		#
		#pass
		if usePyQt4 :
			stringValue = self.selector.itemData ( idx ).toString ()
		else :
			stringValue = str ( self.selector.itemData ( idx ) )
		#print ">> Ui_StringWidget_selector idx = %d setValue = %s" % ( idx, stringValue )
		self.widget.param.setValue ( str ( stringValue ) )
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
# Ui_StringWidget_file
#
class Ui_StringWidget_file ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, StringWidget ) :
		#
		hl = QtModule.QHBoxLayout ()
		hl.setStretch ( 1, 1 )
		
		self.widget = StringWidget
		
		self.stringEdit = QtModule.QLineEdit ( StringWidget )
		
		self.stringEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
		self.stringEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
		
		self.btnBrowseDir = QtModule.QToolButton ( StringWidget )
		self.btnBrowseDir.setText ( '...' )
		self.btnBrowseDir.setMinimumSize ( QtCore.QSize ( UI.BROWSE_WIDTH, UI.HEIGHT ) )
		self.btnBrowseDir.setMaximumSize ( QtCore.QSize ( UI.BROWSE_WIDTH, UI.HEIGHT ) )
		
		hl.addWidget ( self.stringEdit )
		hl.addWidget ( self.btnBrowseDir )
		self.widget.param_vl.addLayout ( hl )
		QtCore.QMetaObject.connectSlotsByName ( StringWidget )
		self.connectSignals ( StringWidget )
	#
	# connectSignals
	#
	def connectSignals ( self, StringWidget ) :
		#
		if usePyQt4 :
			StringWidget.connect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
			StringWidget.connect ( self.btnBrowseDir, QtCore.SIGNAL ( 'clicked()' ), self.onBrowseFile )
		else :
			self.stringEdit.editingFinished.connect ( self.onStringEditEditingFinished )
			self.btnBrowseDir.clicked.connect ( self.onBrowseFile )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, StringWidget ) :
		#
		if usePyQt4 :
			StringWidget.disconnect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
			StringWidget.disconnect ( self.btnBrowseDir, QtCore.SIGNAL ( 'clicked()' ), self.onBrowseFile )
		else :
			self.stringEdit.editingFinished.disconnect ( self.onStringEditEditingFinished )
			self.btnBrowseDir.clicked.disconnect ( self.onBrowseFile )
	#
	# onStringEditEditingFinished
	#
	def onStringEditEditingFinished ( self ) :
		#
		stringValue = self.stringEdit.text ()
		self.widget.param.value = str ( stringValue )
		#self.widget.param.paramChanged ()
	#
	# onBrowseFile
	#
	def onBrowseFile ( self ) :
		#
		if DEBUG_MODE : print '>> Ui_StringWidget_file onBrowseFile'
		typeFilter = ''
		rangeList = self.widget.param.getRangeValues ()
		
		for ( label, value ) in rangeList :
			if DEBUG_MODE : print "label = %s value = %s" % ( label, value )
			typeFilter += ( label + ' ' + value + ';;' )
			#self.selector.addItem ( label, value )
		#print '>> Ui_StringWidget_file typeFilter = %s' % typeFilter   
		
		curDir = app_global_vars [ 'ProjectPath' ]
		
		if usePyQt4 :
			filename = QtModule.QFileDialog.getOpenFileName ( self.widget, 'Select file', curDir, typeFilter )
		else :
			( filename, filter ) = QtModule.QFileDialog.getOpenFileName ( self.widget, 'Select file', curDir, typeFilter )
		
		if filename != '' : 
			self.widget.param.setValue ( str ( filename ) )
			self.updateGui ( self.widget.param.value )
	#
	# updateGui
	#
	def updateGui ( self, value ) :
		# 
		self.stringEdit.setText ( value )    
