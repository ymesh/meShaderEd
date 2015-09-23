"""

	gfxNote.py

"""
from core.mePyQt import QtCore, QtGui

from gfx.gfxNodeLabel import GfxNodeLabel

from global_vars import DEBUG_MODE, GFX_NOTE_TYPE
from meShaderEd import app_settings

if QtCore.QT_VERSION < 50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
	
#
# GfxNote
#
class GfxNote ( QtModule.QGraphicsItem ):
	#
	Type = GFX_NOTE_TYPE
	#
	# __init__
	#
	def __init__ ( self, node ) :
		#
		QtModule.QGraphicsItem.__init__ ( self )

		self.label_widget = None
		self.text_widget = None
		
		self.headerFont = QtGui.QFont ()
		self.paramsFont = QtGui.QFont ()
		
		self.x_offset = 10
		self.y_offset = 10
		self.radius = 10

		# node parameters
		self.showBorder = True
		self.justify = QtCore.Qt.AlignLeft # left:center:right
		self.text = ''
		self.opacity = 0.5
		self.bgColor = QtGui.QColor ( 128, 128, 128 )
		self.textColor = QtGui.QColor ( 0, 0, 0 )
		self.selectedColor = QtGui.QColor ( 250, 250, 250 )
		
		self.node = node
		
		if self.node is not None :
			self.updateGfxNode ()
			( x, y ) = self.node.offset
			self.setPos ( x, y )
		
		self.PenBorderNormal = QtGui.QPen( QtGui.QBrush ( self.textColor ),
																	 1.0,
																	 QtCore.Qt.SolidLine,
																	 QtCore.Qt.RoundCap,
																	 QtCore.Qt.RoundJoin )

		self.PenBorderSelected = QtGui.QPen( QtGui.QBrush ( self.selectedColor ),
																	 2.0,
																	 QtCore.Qt.SolidLine,
																	 QtCore.Qt.RoundCap,
																	 QtCore.Qt.RoundJoin )

		self.bgColor.setAlphaF ( self.opacity )
		
		self.BrushNodeNormal = QtGui.QBrush ( self.bgColor )

		# flag (new from QT 4.6...)
		self.setFlag ( QtGui.QGraphicsItem.ItemSendsScenePositionChanges )
		self.setFlag ( QtGui.QGraphicsItem.ItemSendsGeometryChanges )
		#self.setFlag ( QtGui.QGraphicsItem.ItemIsFocusable )

		# qt graphics stuff
		self.setFlag ( QtGui.QGraphicsItem.ItemIsMovable )
		self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
		self.setZValue ( 1 )  
	#
	# type
	#
	def type ( self ) : return GfxNote.Type
	#
	# remove
	#
	def remove ( self ) :
		#
		if DEBUG_MODE : print '>> GfxNote remove gfxNode (temp)'
		self.scene().emit ( QtCore.SIGNAL ( 'onGfxNodeRemoved' ), self )
	#
	# updateNodeLabel
	#
	def updateNodeLabel ( self ) :
		#
		self.label_widget.setText ( self.node.label )
		self.setupGeometry ()
		self.update ()
	#
	# updateGfxNode
	#
	def updateGfxNode ( self ) :
		# remove all children
		for item in self.childItems () : self.scene ().removeItem ( item )
		self.setupParameters ()
		self.setupGeometry ()
	#
	# setupParameters
	#
	def setupParameters ( self ) :
		#
		if self.node is not None :
			#
			# get known node parametres
			#
			for name in [ 'text_color', 'bg_color', 'opacity', 'border', 'justify', 'text' ] :
				param = self.node.getInputParamByName ( name )
				if param is not None :
					if name == 'text' :
						self.text = param.value
						#print '* text = %s' % self.text
					elif name == 'border' :
						self.showBorder = param.value
						#print '* showBorder = %s' % self.showBorder
					elif name == 'opacity' :
						self.opacity = param.value
						#print '* opacity = %f' % self.opacity
					elif name == 'bg_color' :
						r = param.value [0] 
						g = param.value [1] 
						b = param.value [2] 
						self.bgColor = QtGui.QColor ( r * 255, g * 255, b * 255 )
					elif name == 'text_color' :
						r = param.value [0] 
						g = param.value [1] 
						b = param.value [2] 
						self.textColor = QtGui.QColor ( r * 255, g * 255, b * 255 )
						#print '* text_color = %f %f %f' % ( r, g, b )
					elif name == 'justify' :
						if param.value == 0 :
							self.justify = QtCore.Qt.AlignLeft
						elif param.value == 1 :
							self.justify = QtCore.Qt.AlignHCenter
						elif param.value == 2 :
							self.justify = QtCore.Qt.AlignRight
			
			self.label_widget = GfxNodeLabel ( self.node.label, bgFill = False )
			self.label_widget.setBold ()
			self.label_widget.setNormalColor ( self.textColor )
			if self.isSelected () : self.label_widget.setSelected ()

			self.text_widget = GfxNodeLabel ( self.text, bgFill = False )
			self.text_widget.setNormalColor ( self.textColor )
			self.text_widget.setNormal ( True )
			self.text_widget.justify = self.justify
			
			self.label_widget.setParentItem ( self )
			self.text_widget.setParentItem ( self )
	#
	# setupGeometry
	#
	def setupGeometry ( self ) :
		#
		wi = 80 # minimal node width
		hi = 0
		x = self.x_offset
		y = self.y_offset
		
		( wi_label, hi_label ) = self.label_widget.getLabelSize ()
		self.label_widget.rect = QtCore.QRectF ( x, y, wi_label, hi_label )
		
		( wi_text, hi_text ) = self.text_widget.getLabelSize ()
		self.text_widget.rect = QtCore.QRectF ( x, y + hi_label + self.y_offset , wi_text, hi_text )
		
		wi_max = max ( wi,  wi_label, wi_text ) + 2 * self.x_offset 
		hi_max = hi_label + hi_text + 3 * self.y_offset
		
		self.rect = QtCore.QRectF ( 0, 0, wi_max, hi_max )  
	#
	# boundingRect
	#
	def boundingRect ( self ) :
		#print ( "GfxNode.boundingRect" )
		bound_rect = QtCore.QRectF ( self.rect )
		#bound_rect.adjust( -8, 0, 8, 0 )
		return bound_rect
	#
	# shape
	#
	def shape ( self ) :
		#
		shape = QtGui.QPainterPath ()
		shape.addRect ( self.boundingRect () )
		#shape += self.header['input'].shape()
		#shape += self.header['output'].shape()
		return shape
	#
	# itemChange
	#
	def itemChange ( self, change, value ) :
		#
		if change == QtGui.QGraphicsItem.ItemSelectedHasChanged : #ItemSelectedChange:
			self.label_widget.setSelected ( value.toBool () )
			if value.toBool () :
				items = self.scene ().items ()
				for i in range ( len ( items ) - 1, -1, -1 ) :
					if items [ i ].parentItem() is None :
						if items [ i ] != self :
							items [ i ].stackBefore ( self )
				#scene.setFocusItem ( self )
		elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
			from meShaderEd import getDefaultValue
			grid_snap = getDefaultValue ( app_settings, 'WorkArea', 'grid_snap' )
			grid_size = int ( getDefaultValue ( app_settings, 'WorkArea', 'grid_size' )  )
			x = self.x ()
			y = self.y ()
			if grid_snap :
				#if DEBUG_MODE : print '* snap to grid  (size = %d)' % grid_size
				x -= ( x % grid_size )
				y -= ( y % grid_size )
				self.setPos ( x, y )
			#if DEBUG_MODE : print '* GfxNode.itemChange = ItemPositionHasChanged (%f, %f)' % ( x, y )
			self.node.offset = ( x, y )
			#self.adjustLinks ()
		return QtGui.QGraphicsItem.itemChange ( self, change, value )
	#
	# paint
	#
	def paint ( self, painter, option, widget ) :
		# print ( ">> GfxNode.paint" )
		painter.setRenderHint ( QtGui.QPainter.Antialiasing )
		painter.setRenderHint ( QtGui.QPainter.SmoothPixmapTransform )

		self.paintFrame ( painter )
	#
	# paintFrame
	#
	def paintFrame ( self, painter ) :
		#print ( ">> GfxNode.paintWindowFrame" )
		pen = self.PenBorderNormal
		brush = self.BrushNodeNormal
		
		self.bgColor.setAlphaF ( self.opacity )
		brush.setColor ( self.bgColor )
		
		if self.isSelected () : pen = self.PenBorderSelected

		if not self.showBorder : 
			pen.setStyle ( QtCore.Qt.NoPen )
		else :
			pen.setStyle ( QtCore.Qt.SolidLine )
				
		painter.setPen ( pen )
		painter.setBrush ( brush )
		painter.drawRoundedRect ( self.rect, self.radius, self.radius, QtCore.Qt.AbsoluteSize ) 
