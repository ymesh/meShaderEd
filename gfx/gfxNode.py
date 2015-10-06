"""

 gfxNode.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui
from core.signal import Signal

from gfx.gfxNodeLabel import GfxNodeLabel
from gfx.gfxNodeConnector import GfxNodeConnector
from gfx.gfxLink import GfxLink

from global_vars import app_colors, DEBUG_MODE, GFX_NODE_TYPE, VALID_RSL_PARAM_TYPES
from meShaderEd import app_settings
import gui.ui_settings as UI

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# GfxNode
#
class GfxNode ( QtModule.QGraphicsItem ) : # QtModule.QGraphicsItem QtModule.QGraphicsItem
	#
	Type = GFX_NODE_TYPE
	#
	# __init__
	#
	def __init__ ( self, node ) :
		#
		QtModule.QGraphicsItem.__init__ ( self )

		self.node = node
		self.header = {}

		self.outputParamLabels = []
		self.inputParamLabels = []

		self.outputConnectors = []
		self.inputConnectors = []

		self.headerFont = QtGui.QFont ()
		self.paramsFont = QtGui.QFont ()

		self.x_offset = 10
		self.y_offset = 10
		self.radius = UI.NODE_RADIUS

		self.swatchSize = UI.SWATCH_SIZE
		self.hasSwatch = False

		self.shadow_offset = UI.SHADOW_OFFSET
		self.shadow_opacity = UI.SHADOW_OPACITY
		
		self.normalColor = QtGui.QColor ( 0, 0, 0 )
		self.selectedColor = QtGui.QColor ( 250, 250, 250 )
		alternateColor = QtGui.QColor ( 240, 140, 0 )
		self.bgColor = self.get_bg_color () 
		
		self.shadowColor = QtGui.QColor ( 0, 0, 0 )
		self.shadowColor.setAlphaF ( self.shadow_opacity )
		
		self.PenBorderNormal = QtGui.QPen( QtGui.QBrush ( self.normalColor ),
																	 1.0,
																	 QtCore.Qt.SolidLine,
																	 QtCore.Qt.RoundCap,
																	 QtCore.Qt.RoundJoin )

		self.PenBorderSelected = QtGui.QPen( QtGui.QBrush ( self.selectedColor ),
																	 2.0,
																	 QtCore.Qt.SolidLine,
																	 QtCore.Qt.RoundCap,
																	 QtCore.Qt.RoundJoin )

		self.PenNodeShaderParam = QtGui.QPen( QtGui.QColor( 250, 250, 250 ) )

		self.BrushNodeNormal = QtGui.QBrush ( self.bgColor )
		self.BrushShadow = QtGui.QBrush ( self.shadowColor )
		self.PenShadow = QtGui.QPen ( self.shadowColor )

		self.collapse = None # 'input' 'output' 'all'

		if self.node is not None :
			self.connectSignals ()
			self.updateGfxNode ()
			( x, y ) = self.node.offset
			self.setPos ( x, y )

		# flag (new from QT 4.6...)
		self.setFlag ( QtModule.QGraphicsItem.ItemSendsScenePositionChanges )
		self.setFlag ( QtModule.QGraphicsItem.ItemSendsGeometryChanges )

		# qt graphics stuff
		self.setFlag ( QtModule.QGraphicsItem.ItemIsMovable )
		self.setFlag ( QtModule.QGraphicsItem.ItemIsSelectable )
		self.setZValue ( 1 )
	#
	# connectSignals
	#
	def connectSignals ( self ) :
		#
		if usePyQt4 :
			QtCore.QObject.connect ( self.node, QtCore.SIGNAL ( 'nodeUpdated' ), self.onUpdateNode )
			QtCore.QObject.connect ( self.node, QtCore.SIGNAL ( 'nodeParamsUpdated' ), self.onUpdateNodeParams )
		else :
			self.node.nodeUpdated.connect ( self.onUpdateNode )
			self.node.nodeParamsUpdated.connect ( self.onUpdateNodeParams )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self ) :
		#
		if usePyQt4 :
			QtCore.QObject.disconnect ( self.node, QtCore.SIGNAL ( 'nodeUpdated' ), self.onUpdateNode )
			QtCore.QObject.disconnect ( self.node, QtCore.SIGNAL ( 'nodeParamsUpdated' ), self.onUpdateNodeParams )
		else :
			self.node.nodeUpdated.disconnect ( self.onUpdateNode )
			self.node.nodeParamsUpdated.disconnect ( self.onUpdateNodeParams )
	#
	# type
	#
	def type ( self ) : return GfxNode.Type
	#
	# get_bg_color
	#
	def get_bg_color ( self ) :
		#
		bg = QtGui.QColor ( 128, 128, 128 )
		
		if self.node.format == 'rsl' :
			bg = app_colors [ 'rsl_node_bg' ] 
		elif self.node.format == 'rib' :
			bg = app_colors [ 'rib_node_bg' ] 
		elif self.node.format == 'image' :
			bg = app_colors [ 'image_node_bg' ]
		return bg
	#
	# onUpdateNode
	#
	def onUpdateNode ( self, foo_param = None ) :
		#
		if DEBUG_MODE : print '>> GfxNode( %s ).onUpdateNode' % ( self.node.label )
		self.updateGfxNodeParams ( True )
		self.updateNodeLabel ()
		if usePyQt4 :
			self.scene().emit ( QtCore.SIGNAL ( 'nodeUpdated' ), self )
		else :
			self.scene().nodeUpdated.emit ( self )
	#
	# onUpdateNodeParams
	#
	def onUpdateNodeParams ( self, forceUpdate = False ) :
		#
		if DEBUG_MODE : print '>> GfxNode( %s ).onUpdateNodeParams' % ( self.node.label )
		self.updateGfxNodeParams ( forceUpdate )
		if usePyQt4 :
			self.scene().emit ( QtCore.SIGNAL ( 'gfxNodeParamChanged' ), self )
		else :
			self.scene().gfxNodeParamChanged.emit ( self )
	#
	# updateGfxNodeParams
	#
	def updateGfxNodeParams ( self, forceUpdate = False  ) :
		#
		if DEBUG_MODE : print '>> GfxNode( %s ).updateGfxNodeParams' % ( self.node.label )
		inpGeomChanged = self.updateInputParams ()
		outGeomChanged = self.updateOutputParams ()
		if forceUpdate or inpGeomChanged or outGeomChanged :
			self.setupGeometry ()
			self.update ()
			self.adjustLinks ()
	#
	# updateGfxNode
	#
	def updateGfxNode ( self, removeLinks = True ) :
		#
		if DEBUG_MODE : print '>> GfxNode( %s ).updateGfxNode' % ( self.node.label )
		if removeLinks :
			# remove all GfxLinks
			for connect in self.inputConnectors : connect.removeAllLinks ()
			for connect in self.outputConnectors : connect.removeAllLinks ()
			self.outputConnectors = []
			self.inputConnectors = []
		# remove all children
		for item in self.childItems () : 
			self.scene ().removeItem ( item )
		self.header = {}
		self.setupHeader ()
		self.outputParamLabels = []
		self.inputParamLabels = []
		
		self.setupParams ( self.node.outputParams, self.outputParamLabels, self.outputConnectors, removeLinks )
		self.setupParams ( self.node.inputParams, self.inputParamLabels, self.inputConnectors, removeLinks )
		self.setupGeometry ()
		self.update ()
	#
	# getInputConnectorByParam
	#
	def getInputConnectorByParam ( self, param ) :
		#
		connector = None
		for cnt in self.inputConnectors :
			if cnt.param == param :
				connector = cnt
				break
		return connector
	#
	# getOutputConnectorByParam
	#
	def getOutputConnectorByParam ( self, param ) :
		#
		connector = None
		for cnt in self.outputConnectors :
			if cnt.param == param :
				connector = cnt
				break
		return connector
	#
	# remove
	#
	def remove ( self ) :
		#
		if DEBUG_MODE : print '>> GfxNode.remove'
		self.disconnectSignals ()
		for connect in self.inputConnectors : connect.removeAllLinks ()
		for connect in self.outputConnectors : connect.removeAllLinks ()
		if usePyQt4 :
			self.scene().emit ( QtCore.SIGNAL ( 'onGfxNodeRemoved' ), self )
		else :
			self.scene().onGfxNodeRemoved.emit ( self )
	#
	# updateNodeLabel
	#
	def updateNodeLabel ( self ) :
		#
		self.header [ 'label' ].setText ( self.node.label )
		self.setupGeometry ()
		self.update ()
		self.adjustLinks ()
	#
	# updateInputParams
	#
	def updateInputParams ( self ) : return self.updateParams ( self.node.inputParams, self.inputParamLabels )
	#
	# updateOutputParams
	#
	def updateOutputParams ( self ) : return self.updateParams ( self.node.outputParams, self.outputParamLabels )
	#
	# updateParams
	#
	def updateParams ( self, params, labels ) :
		#
		if DEBUG_MODE : print ( '>> GfxNode.updateParams' )
		geomChanged = False
		i = 0
		for param in params : # for i in range( len( self.node.inputParams )) :
			if param.type != 'control' :
				if param.provider != 'attribute' :
					if i >= len ( labels ) :
						label = self.addGfxNodeParam ( param )
						geomChanged = True
					else :
						label = labels [ i ]
						if param.label != label.text :
							label.setText ( param.label )
							geomChanged = True
						self.updateGfxNodeParamLabel ( param, label )
					i += 1
		return geomChanged
	#
	# setupGeometry
	#
	def setupGeometry ( self ) :
		#
		( wi_header, hi_header ) = self.getHeaderSize ()
		( wi_output, hi_output ) = self.getParamsSize ( self.outputParamLabels )
		( wi_input, hi_input ) = self.getParamsSize ( self.inputParamLabels )

		wi_max = max ( wi_header, wi_output, wi_input ) + 2 * self.x_offset
		hi_max = hi_header + hi_output + hi_input + 3 * self.y_offset

		self.rect = QtCore.QRectF ( 0, 0, wi_max, hi_max )
		self.setupHeaderGeometry ( self.x_offset, self.y_offset )
		self.setupOutputParamsGeometry ( wi_max - self.x_offset, hi_header + 2 * self.y_offset )
		self.setupInputParamsGeometry ( self.x_offset, hi_header + 2 * self.y_offset + hi_output )
	#
	# shadowRect
	#
	def shadowRect ( self ) :
		#
		shadowRect = QtCore.QRectF ( self.rect )
		shadowRect.translate ( self.shadow_offset, self.shadow_offset )
		return shadowRect
	#
	# boundingRect
	#
	def boundingRect ( self ) :
		#
		bound_rect = QtCore.QRectF ( self.rect ).united( self.shadowRect () )
		bound_rect.adjust( -8, 0, 8, 0 )
		return bound_rect
	#
	# shape
	#
	def shape ( self ) :
		#
		shape = QtGui.QPainterPath ()
		shape.addRect ( self.boundingRect () )
		return shape
	#
	# setupHeader
	#
	def setupHeader ( self ) :
		#
		if self.node.type != 'variable' :
			self.header [ 'label' ] = GfxNodeLabel ( self.node.label )

			self.header [ 'label' ].setBgColor ( self.bgColor )
			self.header [ 'label' ].setNormalColor ( self.normalColor )
			self.header [ 'label' ].setBold ()
			self.header [ 'label' ].setSelected ( self.isSelected () )
			
			if self.node.help is not None :
				self.header [ 'label' ].setWhatsThis ( self.node.help )
			
			self.header [ 'name' ] = GfxNodeLabel ( self.node.name )

			self.header [ 'name' ].setBgColor ( self.bgColor )
			self.header [ 'name' ].setNormalColor ( self.normalColor )
			self.header [ 'name' ].setItalic ()
			self.header [ 'name' ].setProcessEvents ( False )

			if self.hasSwatch : self.header [ 'swatch' ] = GfxNodeSwatch ( self.swatchSize )

			#self.header['input'] = GfxNodeConnector( 6 )
			#self.header['output'] = GfxNodeConnector( 6 )
	#
	# getHeaderSize
	#
	def getHeaderSize ( self ) :
		#
		wi = 80 # minimal node width
		hi = 0
		if self.node.type != 'variable' :
			( wi_label, hi_label ) = self.header [ 'label' ].getLabelSize ()
			( wi_name, hi_name ) = self.header [ 'name' ].getLabelSize()
			hi = ( hi_label + hi_name )
			wi = max ( wi, ( self.x_offset + max ( wi_label, wi_name ) ) )

			if self.hasSwatch :
				hi = max ( self.swatchSize, hi )
				wi += self.swatchSize

		return ( wi, hi )
	#
	# setupHeaderGeometry
	#
	def setupHeaderGeometry ( self, x, y ) :
		#
		if self.node.type != 'variable' :
			wi_header = self.rect.width ()
			if self.hasSwatch :
				self.header [ 'swatch' ].rect.moveTo ( x, y )
				#self.header['input'].rect.moveTo( x - self.x_offset - self.header['input'].radius,
				#                                  y + self.swatchSize / 2 - self.header['input'].radius )
				#self.header['output'].rect.moveTo( wi_header - self.header['output'].radius,
				#                                  y + self.swatchSize / 2 - self.header['output'].radius )
				x += self.header [ 'swatch' ].rect.width () + self.x_offset

			( wi, hi ) = self.header [ 'label' ].getLabelSize ()
			self.header [ 'label' ].rect = QtCore.QRectF ( x, y, wi, hi )
			y += hi
			( wi, hi ) = self.header [ 'name' ].getLabelSize()
			self.header [ 'name' ].rect = QtCore.QRectF ( x, y, wi, hi )

			# parent controls from header
			for ctrl in self.header.keys() : self.header [ ctrl ].setParentItem ( self )
	#
	# setupOutputParamsGeometry
	#
	def setupOutputParamsGeometry ( self, xs, ys ) :
		#
		y = ys
		hi = 0
		for label in self.outputParamLabels :
			( wi, hi ) = label.getLabelSize ()
			label.rect = QtCore.QRectF ( xs - wi, y, wi, hi )
			y += hi
			label.setParentItem ( self )
		# wi_header = self.rect.width()
		y = ys
		x = xs + self.x_offset
		for connector in self.outputConnectors :
			connector.rect.moveTo ( x - connector.radius, y + hi / 2 - connector.radius )
			y += hi
			connector.setParentItem ( self )
			
	#
	# setupInputParamsGeometry
	#
	def setupInputParamsGeometry ( self, xs, ys ) :
		#
		y = ys
		hi = 0
		for label in self.inputParamLabels :
			( wi, hi ) = label.getLabelSize ()
			label.rect = QtCore.QRectF ( xs, y, wi, hi )
			y += hi
			label.setParentItem ( self )

		y = ys
		x = xs - self.x_offset
		for connector in self.inputConnectors :
			connector.rect.moveTo ( x - connector.radius, y + hi / 2 - connector.radius )
			y += hi
			connector.setParentItem ( self )
	#
	# getParamsSize
	#
	def getParamsSize ( self, paramLabels ) :
		#
		wi = 0
		hi = 0
		for label in paramLabels :
			( wi_label, hi_label ) = label.getLabelSize()
			hi += hi_label
			wi = max ( wi, wi_label )
		return ( wi, hi )
	#
	# updateGfxNodeParamLabel
	#
	def updateGfxNodeParamLabel ( self, param, label, forceUpdate = False ) :
		#
		if param.type in VALID_RSL_PARAM_TYPES :
			label.setNormal ()
			isVarying = ( param.detail == 'varying' )
			isPrimitive = ( param.provider == 'primitive' )
			label.setItalic ( isVarying ) 
			label.setSelected ( param.shaderParam  ) 
			label.setAlternate ( isPrimitive  ) 
			# this allows to change param.shaderParam attribute by CTRL-click on label
			# and switch param.provide to "primitive" by ALT-click
			label.setProcessEvents ( True ) 
			if forceUpdate :
				self.update () 
				if usePyQt4 :
					self.scene ().emit ( QtCore.SIGNAL ( 'gfxNodeParamChanged' ), self, param ) 
				else :
					self.scene ().gfxNodeParamChanged.emit ( self, param )
	#
	# addGfxNodeParam
	#
	def addGfxNodeParam ( self, param ) :
		#
		if DEBUG_MODE : print ">> GfxNode.addGfxNodeParam (%s)" % param.label
		if param.isInput :
			labels = self.inputParamLabels
			connectors = self.inputConnectors
		else :
			labels = self.outputParamLabels
			connectors = self.outputConnectors
		label = GfxNodeLabel ( param.label, param )
		label.setBgColor ( self.bgColor )
		label.setNormalColor ( self.normalColor )
		if not param.isInput : label.setBold ()
			
		if param.help is not None :
			label.setWhatsThis ( self.node.help )
		
		self.updateGfxNodeParamLabel ( param, label )

		labels.append ( label )

		connector = GfxNodeConnector ( param, UI.CONNECTOR_RADIUS, node = None )
		if not param.isInput : 
			connector.singleLinkOnly = False
		connectors.append ( connector )
	#
	# removeGfxNodeParam
	#
	def removeGfxNodeParam ( self, param ) :
		#
		if DEBUG_MODE : print ">> GfxNode.removeGfxNodeParam (%s)" % param.label
		if param.isInput :
			labels = self.inputParamLabels
			connectors = self.inputConnectors
		else :
			labels = self.outputParamLabels
			connectors = self.outputConnectors
		i = 0
		for label in list ( labels ) :
			if label.param == param :
				labels.pop ( i )
				self.scene ().removeItem ( label )

				connector = connectors.pop ( i )
				connector.remove () 
				self.scene ().removeItem ( connector )

			i += 1
	#
	# setupParams
	#
	def setupParams ( self, params, labels, connectors, updateConnectors = True ):
		#
		for param in params :
			# ignore attributes
			if param.provider != 'attribute' :
				label = GfxNodeLabel ( param.label, param )
				label.setBgColor ( self.bgColor )
				label.setNormalColor ( self.normalColor )
				if not param.isInput : label.setBold ()
					
				if param.help is not None :
					label.setWhatsThis ( self.node.help )
				
				if param.type in VALID_RSL_PARAM_TYPES :
					label.setNormal ()
					isVarying = ( param.detail == 'varying' )
					isPrimitive = ( param.provider == 'primitive' )
					label.setItalic ( isVarying ) 
					label.setSelected ( param.shaderParam  ) 
					label.setAlternate ( isPrimitive  ) 
					# this allows to change param.shaderParam attribute by CTRL-click on label
					# and switch param.provide to "primitive" by ALT-click
					label.setProcessEvents ( True )   
				labels.append ( label )
				if updateConnectors :
					connector = GfxNodeConnector ( param, UI.CONNECTOR_RADIUS, node = None )
					if not param.isInput : connector.singleLinkOnly = False
					connectors.append ( connector )
	#
	# adjustLinks
	#
	def adjustLinks ( self ) :
		# invalidate all the links attached
		for connect in self.inputConnectors : connect.adjustLinks ()
		for connect in self.outputConnectors : connect.adjustLinks ()
	#
	# itemChange
	#
	def itemChange ( self, change, value ) :
		#
		if change == QtModule.QGraphicsItem.ItemSelectedHasChanged : #ItemSelectedChange: QGraphicsItem
			if self.node.type != 'variable' :
				# variable node has not header
				#if  not usePyQt5 :
				#	self.header [ 'label' ].setSelected ( value.toBool () )
				#else :
				self.header [ 'label' ].setSelected ( value )
				#self.header['swatch'].isNodeSelected = self.isNodeSelected
			if value == 1 :
				items = self.scene ().items ()
				for i in range ( len ( items ) - 1, -1, -1 ) :
					if items [ i ].parentItem() is None :
						if items [ i ] != self :
							items [ i ].stackBefore ( self )
				#scene.setFocusItem ( self )
		elif change == QtModule.QGraphicsItem.ItemPositionHasChanged :
			from meShaderEd import getDefaultValue
			grid_snap = bool ( getDefaultValue ( app_settings, 'WorkArea', 'grid_snap' ) )
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
			self.adjustLinks ()
			#return QtCore.QPointF ( x, y )
		#return super( GfxNode, self ).itemChange ( change, value )
		return QtModule.QGraphicsItem.itemChange ( self, change, value )
	
	#
	# paint
	#
	def paint ( self, painter, option, widget ) :
		# print ( ">> GfxNode.paint" )
		painter.setRenderHint ( QtGui.QPainter.Antialiasing )
		painter.setRenderHint ( QtGui.QPainter.SmoothPixmapTransform )

		self.paintShadow ( painter )
		self.paintFrame ( painter )
	#
	# paintShadow
	#
	def paintShadow ( self, painter ) :
		#
		painter.setBrush ( self.BrushShadow )
		painter.setPen ( self.PenShadow )
		painter.drawRoundedRect ( self.shadowRect (), self.radius, self.radius, QtCore.Qt.AbsoluteSize )
	#
	# paintFrame
	#
	def paintFrame ( self, painter ) :
		#print ( ">> GfxNode.paintWindowFrame" )
		pen = self.PenBorderNormal
		brush = self.BrushNodeNormal
		if self.isSelected () :
			pen =  self.PenBorderSelected
			# brush = self.BrushNodeSelected

		painter.setPen ( pen )
		painter.setBrush ( brush )

		# painter.drawRect ( self.rect )
		painter.drawRoundedRect ( self.rect, self.radius, self.radius, QtCore.Qt.AbsoluteSize )
		# Qt::SizeMode mode = Qt::AbsoluteSize Qt.RelativeSize

