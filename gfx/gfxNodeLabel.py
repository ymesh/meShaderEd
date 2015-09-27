"""

	gfxNodeLabel.py

"""
from core.mePyQt import Qt, QtCore, QtGui

from global_vars import app_colors, DEBUG_MODE, GFX_NODE_LABEL_TYPE
from meShaderEd import app_settings

if QtCore.QT_VERSION < 50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# GfxNodeLabel
#
class GfxNodeLabel ( QtModule.QGraphicsItem ) : # QGraphicsWidget QGraphicsItem
	#
	Type = GFX_NODE_LABEL_TYPE
	#
	# __init__
	#
	def __init__ ( self, text, param = None, bgFill = True ) :
		#
		QtModule.QGraphicsItem.__init__ ( self )

		self.text = text
		self.param = param
		self.help = None

		self.normalColor = QtGui.QColor ( 0, 0, 0 )
		self.selectedColor = QtGui.QColor ( 240, 240, 240 )
		self.alternateColor = QtGui.QColor ( 250, 170, 0 )
		self.bgColor = QtGui.QColor ( 140, 140, 140 )
		
		self.PenNormal = QtGui.QPen ( self.normalColor )
		self.PenSelected = QtGui.QPen ( self.selectedColor )
		self.PenAlternate = QtGui.QPen ( self.alternateColor )
		self.bgBrush = QtGui.QBrush ( self.bgColor )
		
		self.pen = self.PenNormal

		self.font = QtGui.QFont ()
		
		self.justify = QtCore.Qt.AlignLeft
		
		self.bgFill = bgFill
		self.selected = False
		self.alternate = False
		self.bold = False
		self.italic = False
		
		self.editable = False
		self.processEvents = False
		self.setFlag ( QtModule.QGraphicsItem.ItemIsMovable, False )
		self.setFlag ( QtModule.QGraphicsItem.ItemIsSelectable, False )
		
		self.rect = QtCore.QRectF ()
	#
	# type
	#
	def type ( self ) : return GfxNodeLabel.Type
	#
	# boundingRect
	#
	def boundingRect ( self ) : return self.rect
	#
	# setWhatsThis
	#
	def setWhatsThis ( self, helpString ) : 
		#
		self.help = helpString
		#self.setAttribute ( QtCore.Qt.WA_CustomWhatsThis, ( self.help is not None ) ) 
		#print '** setWhatsThis = %s' % self.testAttribute ( QtCore.Qt.WA_CustomWhatsThis )
		# PyQt4.QtCore.Qt.WhatsThisCursor
		# PyQt4.QtCore.Qt.WhatsThisRole
	#
	# setNormal
	#
	def setNormal ( self, normal = True ) : 
		#
		if normal :
			self.pen = self.PenNormal
			self.selected = False
			self.alternate = False
	#
	# setSelected
	#
	def setSelected ( self, selected = True ) : 
		#
		self.selected = selected
		if selected :
			self.pen = self.PenSelected
			self.alternate = False
		else :
			self.setNormal ()
	#
	# setAlternate
	#
	def setAlternate ( self, alternate = True ) : 
		#
		self.alternate = alternate
		if alternate :
			self.pen = self.PenAlternate
			self.selected = False
	#
	# setNormalColor
	#
	def setNormalColor ( self, color ) : self.PenNormal = QtGui.QPen ( color ) 
	#
	# setSelectedColor
	#
	def setSelectedColor ( self, color ) : self.PenSelected = QtGui.QPen ( color ) 
	#
	# setAlternateColor
	#
	def setAlternateColor ( self, color ) : self.PenAlternate = QtGui.QPen ( color ) 
	#
	# setBgColor
	#
	def setBgColor ( self, color ) : 
		self.bgColor = color
		self.bgBrush.setColor ( self.bgColor )
	#
	# setBold
	#
	def setBold ( self, bold = True ) :  self.font.setBold ( bold )
	#
	# setItalic
	#
	def setItalic ( self, italic = True ) :  self.font.setItalic ( italic )
	#
	# setText
	#
	def setText ( self, text ) :  self.text = text
	#
	# getLabelSize
	#
	def getLabelSize ( self ) :
		#
		labelFontMetric = QtGui.QFontMetricsF ( self.font )
		lines = self.text.split ( '\n' )
		height = 0
		width = 0
		for line in lines :
			height += labelFontMetric.height () + 1
			width = max ( width, labelFontMetric.width ( line ) ) + 1
		return ( width, height )
	#
	# paint
	#
	def paint ( self, painter, option, widget ) :
		#
		painter.setFont ( self.font )
		if self.bgFill : 
			painter.fillRect ( self.rect, self.bgBrush )
		painter.setPen ( self.pen )
		painter.drawText ( self.rect, self.justify, self.text )
	#
	# setProcessEvents
	#
	def setProcessEvents ( self, process = True ) :
		#
		self.processEvents = process
		#self.setFlag ( QtGui.QGraphicsItem.ItemIsMovable, process )
		self.setFlag ( QtModule.QGraphicsItem.ItemIsSelectable, process )
	#
	# mouseDoubleClickEvent
	#
	"""
	def mouseDoubleClickEvent ( self, event ) :
		#
		if self.processEvents :
			print ">> GfxNodeLabel.mouseDoubleClickEvent"
			if event.button () == QtCore.Qt.LeftButton :
				if event.modifiers () == QtCore.Qt.ControlModifier :
					print '* CTRL dblclick'  
				elif event.modifiers () == QtCore.Qt.AltModifier :
					print '* Alt dblclick'  
		QtGui.QGraphicsItem.mouseDoubleClickEvent ( self, event )
	"""   
	#
	# mousePressEvent
	#
	def mousePressEvent ( self, event ) :
		if self.processEvents :
			#print ">> GfxNodeLabel.mousePressEvent"
			inWhatsThisMode = QtModule.QWhatsThis.inWhatsThisMode ()
			#if inWhatsThisMode :
			#  print '** inWhatsThisMode active'
			from gfx.gfxNode import GfxNode
			parentNode = self.parentItem ()
			if isinstance ( parentNode, GfxNode ) :
				print '* label "%s" of GfxNode "%s"' % ( self.text, parentNode.node.label )
				button = event.button ()
				modifiers = event.modifiers ()
				if button == QtCore.Qt.LeftButton :
					if modifiers == QtCore.Qt.ControlModifier :
						print '* CTRL+LMB (change in shaderParam)' 
						self.param.shaderParam = not self.param.shaderParam
						parentNode.updateGfxNodeParamLabel ( self.param, self, True )
						return
					elif modifiers == QtCore.Qt.AltModifier :
						print '* ALT+LMB ( change detail "uniform/varying")' 
						if self.param.detail == 'varying' :
							self.param.detail = 'uniform'
						else :
							self.param.detail = 'varying' 
						parentNode.updateGfxNodeParamLabel ( self.param, self, True )
						#return
				elif button == QtCore.Qt.RightButton :
					if modifiers == QtCore.Qt.ControlModifier :
						print '* CTRL+RMB change provider "primitive"/"internal"'
						if self.param.provider == 'primitive' :
							self.param.provider = ''
						else :
							self.param.provider = 'primitive' 
						parentNode.updateGfxNodeParamLabel ( self.param, self, True )
						return
			QtCore.QEvent.ignore ( event )
		QtModule.QGraphicsItem.mousePressEvent ( self, event )
	"""
	#
	# mouseMoveEvent
	#
	def mouseMoveEvent ( self, event ) :
		#
		print ">> GfxNodeLabel.mouseMoveEvent"  
		inWhatsThisMode = QtGui.QWhatsThis.inWhatsThisMode ()
		if inWhatsThisMode :
			print '** inWhatsThisMode active'
		#QtCore.QEvent.ignore ( event ) 
		QtGui.QGraphicsItem.mouseMoveEvent ( self, event )
	
	#
	# event
	# The type() can be either QEvent::ToolTip or QEvent::WhatsThis. QWhatsThisClickedEvent.
	def event ( self, event ) :
		#
		print ">> GfxNodeLabel.event"
		if inWhatsThisMode :
			print '** inWhatsThisMode active' 
		return QtGui.QGraphicsItem.event ( self, event )
	#
	#
	#
	"""