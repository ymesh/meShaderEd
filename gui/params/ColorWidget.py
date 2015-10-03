"""

 ColorWidget.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui
from core.signal import Signal

import gui.ui_settings as UI 
from paramWidget import ParamWidget 

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# FloatWidget
#
class ColorWidget ( ParamWidget ) :
	"""
	#
	# __init__
	#
	def __init__ ( self, param, gfxNode, ignoreSubtype = False ) :
		#
		ParamWidget.__init__ ( self, param, gfxNode, ignoreSubtype = False )
		#
		# Define signals for PyQt5
		#
		if QtCore.QT_VERSION >= 0x50000 :
			#
			self.clicked = Signal ()
	"""
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
		#print "eventFilter created..." 
	#
	# eventFilter
	#
	def eventFilter ( self, obj, event ) :
		# check for single click
		if event.type () == QtCore.QEvent.MouseButtonPress:
			#print "eventFilter = MouseButtonPress" 
			if usePyQt4 :
				self.ColorWidget.emit ( QtCore.SIGNAL ( 'clicked()' ) )
			else :
				self.ColorWidget.clicked.emit ()
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
		hl = QtModule.QHBoxLayout ()
		self.widget = ColorWidget
		self.colorEdit = QtModule.QLabel ( ColorWidget )
		
		self.colorEdit.setMinimumSize ( QtCore.QSize ( UI.COLOR_WIDTH, UI.HEIGHT ) )
		self.colorEdit.setMaximumSize ( QtCore.QSize ( UI.COLOR_WIDTH, UI.HEIGHT ) )

		self.colorEdit.setObjectName ( 'colorEdit' )
		
		self.selector = QtModule.QComboBox ( ColorWidget )
		self.selector.setEditable ( False )
		#self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
		self.selector.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.COMBO_HEIGHT ) )
		
		for label in [ "rgb", "hsv", "hsl", "xyz", "XYZ", "YIQ" ] :
			self.selector.addItem ( label )
		if self.widget.param.space != None :
			self.selector.setCurrentIndex ( self.selector.findText ( self.widget.param.space ) )
			
		spacer = QtModule.QSpacerItem ( 20, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		
		hl.addWidget ( self.colorEdit )
		hl.addWidget ( self.selector )
		hl.addItem ( spacer )
		self.widget.param_vl.addLayout ( hl )
		
		self.connectSignals ( ColorWidget )
		
		QtCore.QMetaObject.connectSlotsByName ( ColorWidget )
		
		# install a custom filter in order to avoid subclassing
		self.colorEventFilter = ColorEditEventFilter ( ColorWidget )
		self.colorEdit.installEventFilter ( self.colorEventFilter )
		
	#
	# connectSignals
	#  
	def connectSignals ( self, ColorWidget ) :
		# register signal propertyChanged for updating the gui
		#self.connect( self.colorProperty, QtCore.SIGNAL('propertyChanged()'), self.onPropertyChanged )
		if usePyQt4 :
			ColorWidget.connect ( ColorWidget, QtCore.SIGNAL ( 'clicked()' ), self.onClicked )
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
			ColorWidget.disconnect ( ColorWidget, QtCore.SIGNAL ( 'clicked()' ), self.onClicked )
			ColorWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
		else :
			ColorWidget.clicked.disconnect ( self.onClicked )
			self.selector.activated.disconnect ( self.onCurrentIndexChanged ) 
	#
	# onClicked
	#
	def onClicked ( self ) : 
		print( ">> ColorWidget::onClicked" )
		redValue = int ( self.widget.param.value [0] * 255 )
		greenValue = int ( self.widget.param.value [1] * 255 )
		blueValue = int ( self.widget.param.value [2] * 255 )
		colorSelected = QtModule.QColorDialog.getColor ( QtGui.QColor ( redValue, greenValue, blueValue ), self.widget )
		if colorSelected.isValid () :
			newValue = ( colorSelected.redF (),
									 colorSelected.greenF (),
									 colorSelected.blueF ())        
			self.widget.param.setValue ( newValue )
			#self.widget.param.paramChanged ()
			self.updateGui ( self.widget.param.value )
	#
	# onCurrentIndexChanged
	#
	def onCurrentIndexChanged ( self, idx ) :
		#
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


