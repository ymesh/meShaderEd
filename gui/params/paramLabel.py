"""

 paramLabel.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui 
from core.signal import Signal

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
	
#
# ParamLabel -- editable parameter label
#
class ParamLabel ( QtModule.QLabel ) :
	#
	# __init__
	#
	def __init__ ( self, parent, param = None ) :
		#
		#super ( QtModule.QLabel, self ).__init__ ( parent )
		QtModule.QLabel.__init__ ( self, parent )
		self.widget = parent
		self.param = param
		if param is not None :
			if param.label != '' :
				label_text = param.label
			else :
				label_text = param.name
			self.setText ( label_text )
			if self.param.provider == 'primitive' :
				primitiveColor = QtGui.QColor ( 240, 150, 0 )
				palette = QtGui.QPalette ()
				palette.setColor ( QtGui.QPalette.WindowText, primitiveColor )
				self.setPalette ( palette )
			if self.param.detail == 'varying' :
				font = QtGui.QFont ()
				font.setItalic ( True )
				self.setFont ( font )
		#self.setScaledContents ( True )
		#self.setMouseTracking ( True ) 
		self.buildGui ()
		self.updateGui ()
		self.connectSignals ()
	#
	#  __del__
	#
	def __del__ ( self ) :
		#
		self.disconnectSignals ()
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		self.editLabel = QtModule.QLineEdit ( self )
		self.editLabel.setText ( self.text () )
		self.editLabel.setVisible ( False )
	#
	# updateGui
	#
	def updateGui ( self ) :
		#
		pass
	#
	# connectSignals
	#
	def connectSignals ( self ) :
		#
		if  usePyQt4 :
			self.connect ( self.editLabel, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditingFinished )
		else :
			self.editLabel.editingFinished.connect ( self.onEditingFinished )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self ) :
		#
		if  usePyQt4 :
			self.disconnect ( self.editLabel, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditingFinished )
		else :
			self.editLabel.editingFinished.disconnect ( self.onEditingFinished )
	"""
	#
	# mouseMoveEvent  
	#
	def mouseMoveEvent ( self, event ) :
		#
		if DEBUG_MODE : print ">> ParamLabel( %s ).mouseMoveEvent" % self.param.name
		QtGui.QWidget.mouseMoveEvent ( self, event )
	"""
	#
	# onEditingFinished
	#
	def onEditingFinished ( self ) :
		#
		if DEBUG_MODE : print ">> ParamLabel( %s ).onEditingFinished" % self.param.name
		oldLabel = self.param.label
		newLabel = str ( self.editLabel.text () ).strip ()
		if newLabel != oldLabel :
			newLabel = self.widget.gfxNode.node.renameParamLabel ( self.param, newLabel )
			self.setText ( newLabel )
			self.editLabel.setText ( newLabel )
			self.adjustSize ()
			self.editLabel.adjustSize ()
			self.param.paramChanged ()
		self.setVisible ( True )
		self.editLabel.setVisible ( False )
	#
	# mouseDoubleClickEvent
	#
	def mouseDoubleClickEvent ( self, event ) :
		#
		button = event.button () 
		if button == QtCore.Qt.LeftButton :
			#if DEBUG_MODE : print ">> ParamLabel( %s ).mouseDoubleClickEvent" % self.param.name
			parentLayout = self.parent ().layout ()
			editWidth = parentLayout.columnMinimumWidth ( 0 ) - self.mapToParent ( QtCore.QPoint ( 0, 0 ) ).x () 
			self.setFixedWidth ( editWidth )
			self.editLabel.setFixedWidth ( editWidth )
			self.editLabel.setVisible ( True )
			
			return
		QtModule.QWidget.mouseDoubleClickEvent ( self, event )
	#
	# mousePressEvent
	#
	def mousePressEvent ( self, event ) :
		#
		#if DEBUG_MODE : print ">> ParamLabel( %s ).mousePressEvent" % self.param.name
		button = event.button () 
		modifiers =event.modifiers ()
		if button == QtCore.Qt.LeftButton :
			if modifiers == QtCore.Qt.ControlModifier :
				if DEBUG_MODE : print '* CTRL+LMB (change in shaderParam)' 
				self.param.shaderParam = not self.param.shaderParam
				self.param.paramChanged ()
				return
			elif modifiers == QtCore.Qt.AltModifier :
				if DEBUG_MODE : print '* ALT+LMB ( change detail "uniform/varying")' 
				if self.param.detail == 'varying' :
					self.param.detail = 'uniform'
				else :
					self.param.detail = 'varying' 
				self.param.paramChanged ()
				return
		elif button == QtCore.Qt.RightButton :
			if modifiers == QtCore.Qt.ControlModifier :
				if DEBUG_MODE : print '* CTRL+RMB change provider "primitive"/"internal"'
				if self.param.provider == 'primitive' :
					self.param.provider = ''
				else :
					self.param.provider = 'primitive' 
				self.param.paramChanged ()
				return
			elif modifiers == QtCore.Qt.AltModifier :
				if DEBUG_MODE : print '* ALT+RMB "enable"/"disable" parameter'
				self.param.enabled = not self.param.enabled
				self.param.paramChanged ()
		QtModule.QWidget.mousePressEvent ( self, event )    
