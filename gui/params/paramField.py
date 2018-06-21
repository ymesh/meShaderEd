"""

 paramField.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui
from core.signal import Signal

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI

if not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets

#
# ColorFieldEventFilter
#
class ColorFieldEventFilter ( QtCore.QObject ) :
	#
	# __init__
	#
	def __init__ ( self, colorField ) :
		#
		QtCore.QObject.__init__ ( self, None )
		self.colorField = colorField
		#print ( '>>> ColorFieldEventFilter colorField = ' ), colorField
	#
	# eventFilter
	#
	def eventFilter ( self, obj, event ) :
		# check for single click
		if event.type () == QtCore.QEvent.MouseButtonPress:
			#print ( '>>> ColorFieldEventFilter obj = ' ), obj
			if usePyQt4 :
				self.colorField.emit ( QtCore.SIGNAL ( 'clicked(int)' ), self.colorField.idx )
			else :
				self.colorField.clicked.emit ( self.colorField.idx )
			return True
		else:
			return obj.eventFilter ( obj, event )
#
# ColorField for ColorWidget
#
class ColorField ( QtModule.QWidget ) :
	#
	# __init__
	#
	def __init__ ( self, parent, value = None, idx = None ) :
		#
		QtModule.QWidget.__init__ ( self, parent )
		#
		# Define signals for PyQt5
		#
		if not usePyQt4 :
			#
			self.clicked = Signal ()
			#
		#print ( '>>> ColorField.init' )
		self.value = value
		self.idx = idx
		self.buildGui ()
		#self.updateGui ( value )
		
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		#print ( '>>> ColorField.buildGui' )
		# install a custom filter in order to avoid subclassing
		self.colorFieldEventFilter = ColorFieldEventFilter ( self )
		self.colorEdit = QtModule.QLabel ( self )
		self.colorEdit.setMinimumSize ( QtCore.QSize ( UI.COLOR_WIDTH, UI.HEIGHT ) )
		self.colorEdit.setMaximumSize ( QtCore.QSize ( UI.COLOR_WIDTH, UI.HEIGHT ) )
		self.setMinimumSize ( QtCore.QSize ( UI.COLOR_WIDTH, UI.HEIGHT ) )
		self.setMaximumSize ( QtCore.QSize ( UI.COLOR_WIDTH, UI.HEIGHT ) )
		self.colorEdit.installEventFilter ( self.colorFieldEventFilter )
	#
	# updateGui
	#
	def updateGui ( self, value ) :
		#
		#print ( '>>> ColorField.updateGui ' ), value
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