"""

 ColorWidget.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui
from core.signal import Signal

import gui.ui_settings as UI 
from global_vars import VALID_RSL_COLOR_SPACES
from paramWidget import ParamWidget 
from paramField import ColorField

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# FloatWidget
#
class ColorWidget ( ParamWidget ) :
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		# Define signals for PyQt5
		#
		if usePySide or usePyQt5 :
			#
			self.clicked = Signal ()
			#
		if self.param.isArray () :
			self.ui = Ui_ColorWidget_array () 
		else :
			self.ui = Ui_ColorWidget_field () 
		self.ui.setupUi ( self )
#
# ColorEditEventFilter
#
class ColorEditEventFilter ( QtCore.QObject ) :
	#
	# __init__
	#
	def __init__ ( self, ColorWidget ) :
		#
		QtCore.QObject.__init__ ( self, None )
		self.ColorWidget = ColorWidget
	#
	# eventFilter
	#
	def eventFilter ( self, obj, event ) :
		# check for single click
		if event.type () == QtCore.QEvent.MouseButtonPress:
			#print ( '>>> ColorEditEventFilter obj = ' ), obj
			if usePyQt4 :
				self.ColorWidget.emit ( QtCore.SIGNAL ( 'clicked(QObject)' ), obj )
			else :
				self.ColorWidget.clicked.emit ( obj )
			return True
		else:
			return obj.eventFilter ( obj, event )    
#
# Ui_ColorWidget_field
# 
class Ui_ColorWidget_field ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, ColorWidget ) :
		#
		print ( '>> Ui_ColorWidget_field.setupUi (%s)' % ColorWidget.param.label )
		self.widget = ColorWidget
		
		self.colorEdit = QtModule.QLabel ( ColorWidget )
		self.colorEdit.setMinimumSize ( QtCore.QSize ( UI.COLOR_WIDTH, UI.HEIGHT ) )
		self.colorEdit.setMaximumSize ( QtCore.QSize ( UI.COLOR_WIDTH, UI.HEIGHT ) )
		
		self.selector = QtModule.QComboBox ( ColorWidget )
		self.selector.setEditable ( False )
		self.selector.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.COMBO_HEIGHT ) )
		
		for label in VALID_RSL_COLOR_SPACES :
			self.selector.addItem ( label )
		if self.widget.param.space != None :
			self.selector.setCurrentIndex ( self.selector.findText ( self.widget.param.space ) )
			
		sp = QtModule.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, UI.SP_EXPAND, UI.SP_MIN )
		
		hl = QtModule.QHBoxLayout ()
		hl.setContentsMargins ( UI.SPACING, UI.SPACING, UI.SPACING, UI.SPACING )
		hl.setSpacing ( UI.SPACING )
		
		hl.addWidget ( self.colorEdit )
		hl.addWidget ( self.selector )
		hl.addItem ( sp )
		self.widget.param_vl.addLayout ( hl )
		
		# install a custom filter in order to avoid subclassing
		self.colorEventFilter = ColorEditEventFilter ( ColorWidget )
		self.colorEdit.installEventFilter ( self.colorEventFilter )
		
		self.connectSignals ( ColorWidget )
		QtCore.QMetaObject.connectSlotsByName ( ColorWidget )
	#
	# connectSignals
	#  
	def connectSignals ( self, ColorWidget ) :
		# register signal propertyChanged for updating the gui
		#self.connect( self.colorProperty, QtCore.SIGNAL('propertyChanged()'), self.onPropertyChanged )
		if usePyQt4 :
			ColorWidget.connect ( ColorWidget, QtCore.SIGNAL ( 'clicked(QObject)' ), self.onClicked )
			ColorWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged ) 
		else :
			ColorWidget.clicked.connect ( self.onClicked )
			self.selector.activated.connect ( self.onCurrentIndexChanged ) 
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, ColorWidget ) :
		# register signal propertyChanged for updating the gui
		#self.disconnect( self.colorProperty, QtCore.SIGNAL('propertyChanged()'), self.onPropertyChanged )
		if usePyQt4 : 
			ColorWidget.disconnect ( ColorWidget, QtCore.SIGNAL ( 'clicked(QObject)' ), self.onClicked )
			ColorWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			ColorWidget.clicked.disconnect ( self.onClicked )
			self.selector.activated.disconnect ( self.onCurrentIndexChanged ) 
	#
	# onClicked
	#
	def onClicked ( self, colorEdit = None ) : 
		#print ( ">> ColorWidget::onClicked " ), colorEdit
		redValue = int ( self.widget.param.value [0] * 255 )
		greenValue = int ( self.widget.param.value [1] * 255 )
		blueValue = int ( self.widget.param.value [2] * 255 )
		newColor = QtModule.QColorDialog.getColor ( QtGui.QColor ( redValue, greenValue, blueValue ), self.widget )
		if newColor.isValid () :
			newValue = [ newColor.redF (), newColor.greenF (), newColor.blueF () ]
			self.widget.param.setValue ( newValue )
			#self.widget.param.paramChanged ()
			self.updateGui ( self.widget.param.value )
	#
	# onCurrentIndexChanged
	#
	def onCurrentIndexChanged ( self, idx, param = None ) :
		#
		print ( ">> ColorWidget.onCurrentIndexChanged " ), param
		space = str ( self.selector.currentText () ) 
		if space == 'rgb' : space = None
		self.widget.param.space = space
	#
	# updateGui
	#
	def updateGui ( self, value ) :
		#
		r = value [0] 
		g = value [1] 
		b = value [2] 
		
		pixmap = QtGui.QPixmap ( UI.COLOR_WIDTH, UI.HEIGHT )
		pixmap.fill ( QtCore.Qt.transparent )
		painter = QtGui.QPainter ()
		painter.begin ( pixmap )
		painter.setRenderHint ( QtGui.QPainter.Antialiasing, True )
		
		color = QtGui.QColor ( r * 255, g * 255, b * 255 )
		
		painter.setPen ( QtCore.Qt.NoPen )
		painter.setBrush ( color )  
		painter.drawRect ( 0.0, 0.0, UI.COLOR_WIDTH, UI.HEIGHT )
		painter.end ()
		
		self.colorEdit.setPixmap ( pixmap )
#
# Ui_ColorWidget_array
# 
class Ui_ColorWidget_array ( object ) :
	#
	# setupUi
	#
	def setupUi ( self, ColorWidget ) :
		#
		print ( '>> Ui_ColorWidget_array.setupUi (%s)' % ColorWidget.param.label ) 
		self.widget = ColorWidget
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
			self.labels.append ( QtModule.QLabel ( ColorWidget ) )
			self.labels [ i ].setMinimumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
			self.labels [ i ].setMaximumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
			self.labels [ i ].setAlignment ( QtCore.Qt.AlignRight )
			self.labels [ i ].setText ( '[' + str ( i ) + ']' )
			
			elem = []
			
			elem.append ( ColorField ( ColorWidget, self.widget.param.value [ i ], i ) )
			elem.append ( QtModule.QComboBox ( ColorWidget ) )
			
			elem [ 1 ].setEditable ( False )
			elem [ 1 ].setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
			
			for label in VALID_RSL_COLOR_SPACES :
				elem [ 1 ].addItem ( label )
			space = self.widget.param.spaceArray [ i ]
			if space != None :
				elem [ 1 ].setCurrentIndex ( elem [ 1 ].findText ( space ) )

			self.controls.append ( elem )
			
			sp = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
		
			hl = QtModule.QHBoxLayout ()
			hl.setContentsMargins ( UI.SPACING, UI.SPACING, UI.SPACING, UI.SPACING )
			hl.setSpacing ( UI.SPACING )
			
			hl.addWidget ( self.labels [ i ] )
			hl.addWidget ( elem [ 0 ] )
			hl.addWidget ( elem [ 1 ] ) 
			hl.addItem ( sp )
			self.widget.param_vl.addLayout ( hl )
			
			
		
		self.connectSignals ( ColorWidget )
		QtCore.QMetaObject.connectSlotsByName ( ColorWidget )
	#
	# connectSignals
	#  
	def connectSignals ( self, ColorWidget ) :
		#
		for i in range ( self.widget.param.arraySize ) :
			elem = self.controls [ i ]
			if usePyQt4 :
				ColorWidget.connect ( elem [ 0 ], QtCore.SIGNAL ( 'clicked(int)' ), self.onClicked )
				ColorWidget.connect ( elem [ 1 ], QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged ) 
			else :
				elem [ 0 ].clicked.connect ( self.onClicked )
				elem [ 1 ].activated.connect ( self.onCurrentIndexChanged ) 
	#
	# disconnectSignals
	#
	def disconnectSignals ( self, ColorWidget ) :
		# 
		for i in range ( self.widget.param.arraySize ) :
			elem = self.controls [ i ]
			if usePyQt4 : 
				ColorWidget.disconnect ( elem [ 0 ], QtCore.SIGNAL ( 'clicked(int)' ), self.onClicked )
				ColorWidget.disconnect ( elem [ 1 ], QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
			else :
				elem [ 0 ].clicked.disconnect ( self.onClicked )
				elem [ 1 ].activated.disconnect ( self.onCurrentIndexChanged ) 
	#
	# onClicked
	#
	def onClicked ( self, idx = None ) :  
		print ( ">>> ColorWidget.onClicked idx = " ), idx 
		if idx is not None :
			redValue   = int ( self.widget.param.value [ idx ][0] * 255 )
			greenValue = int ( self.widget.param.value [ idx ][1] * 255 )
			blueValue  = int ( self.widget.param.value [ idx ][2] * 255 )
			newColor = QtModule.QColorDialog.getColor ( QtGui.QColor ( redValue, greenValue, blueValue ), self.widget )
			if newColor.isValid () :
				newValue = [ newColor.redF (), newColor.greenF (),newColor.blueF () ]
				self.widget.param.value [ idx ] = newValue
				self.updateGui ( self.widget.param.value, idx )
	#
	# onCurrentIndexChanged
	#
	def onCurrentIndexChanged ( self, idx, param = None ) :
		#
		# TODO: spaces should be stored in separate spaces array
		#
		print ( ">> ColorWidget.onCurrentIndexChanged " ), param
		for i in range ( self.widget.param.arraySize ) :
			space = str ( self.controls [ i ][ 1 ].currentText () ) 
			if space == 'rgb' : space = None
			self.widget.param.space = space
	#
	# updateGui
	#
	def updateGui ( self, value, idx = None ) :
		#
		if idx is None :
			for i in range ( self.widget.param.arraySize ) :
				self.controls [ i ][0].updateGui ( value [ i ] )
		else :
			self.controls [ idx ][0].updateGui ( value [ idx ] )
