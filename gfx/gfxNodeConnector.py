"""

	gfxNodeConnector.py

"""
import copy
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui
from core.signal import Signal

from meShaderEd import app_settings
from global_vars import DEBUG_MODE, GFX_NODE_CONNECTOR_TYPE
import gui.ui_settings as UI
if not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# GfxNodeConnector
#
class GfxNodeConnector ( QtModule.QGraphicsItem ) : #QtModule.QGraphicsItem
	#
	Type = GFX_NODE_CONNECTOR_TYPE
	isRound = True
	#
	# __init__
	#
	def __init__ ( self, param = None, radius = UI.CONNECTOR_RADIUS, isRound = True, node = None ) :
		#
		QtModule.QGraphicsItem.__init__ ( self )
		self.paramsBrushes = {   'c' : QtGui.QBrush ( QtGui.QColor ( QtCore.Qt.darkRed ) )
														,'f' : QtGui.QBrush ( QtGui.QColor ( QtCore.Qt.lightGray ) )
														,'m' : QtGui.QBrush ( QtGui.QColor ( QtCore.Qt.darkYellow ) )
														,'p' : QtGui.QBrush ( QtGui.QColor ( QtCore.Qt.darkCyan ) )
														,'s' : QtGui.QBrush ( QtGui.QColor ( QtCore.Qt.darkGreen ) )
														,'v' : QtGui.QBrush ( QtGui.QColor ( QtCore.Qt.darkMagenta ) )
														,'n' : QtGui.QBrush ( QtGui.QColor ( QtCore.Qt.darkBlue ) )
														,'I' : QtGui.QBrush ( QtGui.QColor ( 'white' ) )
														,'G' : QtGui.QBrush ( QtGui.QColor ( 'red' ) )
														,'R' : QtGui.QBrush ( QtGui.QColor ( 'orange' ) )
												 }
		self.brush = QtGui.QBrush ( QtGui.QColor ( 140, 140, 140 ) ) # ( 128, 128, 128 ) ( 132, 132, 132 )
		self.PenBorderNormal = QtGui.QPen ( QtGui.QColor ( 0, 0, 0 ) )
		self.PenBorderSelected = QtGui.QPen ( QtGui.QColor ( 240, 240, 240 ), 2.0 )

		self.isNodeSelected = False
		self.isRound = isRound
		self.radius = radius
		self.rect = QtCore.QRectF ( 0, 0, radius*2, radius*2 )
		self.param = param  # Node parameter
		self.links = []     # gfxLinks list
		self.singleLinkOnly = True
		self.state = 'idle'

		self.node = node  # is not None if this "ConnectorNode"
		if node is not None :
			# flag (new from QT 4.6...)
			#self.setFlag ( QtModule.QGraphicsItem.ItemSendsScenePositionChanges )
			self.setFlag ( QtModule.QGraphicsItem.ItemSendsGeometryChanges )

			# qt graphics stuff
			self.setFlag ( QtModule.QGraphicsItem.ItemIsMovable )
			self.setFlag ( QtModule.QGraphicsItem.ItemIsSelectable )
			self.setZValue ( 1 )
			( x, y ) = self.node.offset
			self.setPos ( x, y )
		#
		# setup connector color
		#
		paramTypeStr = self.getInputParam ().encodedTypeStr ()
		if paramTypeStr in self.paramsBrushes.keys () :
			self.brush = self.paramsBrushes [ paramTypeStr ]

		# self.startNodeLink.connect ( self.onStartNodeLinkTest )
	#
	# type
	#
	def type ( self ) : return GfxNodeConnector.Type
	#
	# boundingRect
	#
	def boundingRect ( self ) : return self.rect
	#
	# shape
	#
	def shape ( self ) :
		#
		shape = QtGui.QPainterPath ()
		shape_rect = QtCore.QRectF ( self.rect )
		shape.addEllipse ( shape_rect )
		return shape
	#
	# paint
	#
	def paint ( self, painter, option, widget ) :
		#
		pen = self.PenBorderNormal
		if self.isNodeSelected : #  isSelected()
			pen =  self.PenBorderSelected
			# brush = self.BrushNodeSelected

		painter.setPen ( pen )
		painter.setBrush ( self.brush )
		painter.drawEllipse ( self.rect )
		# print ( ">> GfxNodeConnector.paint" )
	#
	# getCenterPoint
	#
	def getCenterPoint ( self ) : return self.mapToScene ( self.rect.center () )
	#
	# addLink (GfxLink)
	#
	def addGfxLink ( self, link ) : self.links.append ( link )
	#
	# getFirstGfxLink
	#
	def getFirstGfxLink ( self ) : return self.links [ 0 ] ##copy.copy( self.links[0] )
	#
	# getFirstInputParam
	#
	def getFirstInputParam ( self ) : return self.getNode ().inputParams [ 0 ]
	#
	# getInputParam
	#
	def getInputParam ( self ) :
		#
		param = self.param
		if self.isNode () :
			param = self.node.inputParams [ 0 ]
		return param
	#
	# getFirstOutputParam
	#
	def getFirstOutputParam ( self ) : return self.getNode ().outputParams [ 0 ]
	#
	# getOutputParam
	#
	def getOutputParam ( self ) :
		#
		param = self.param
		if self.isNode () :
			param = self.node.outputParams [ 0 ]
		return param
	#
	# removeGfxLink
	#
	def removeGfxLink ( self, gfxLink ) :
		#
		if DEBUG_MODE : print '>> GfxNodeConnector::removeGfxLink'
		if gfxLink in self.links : self.links.remove ( gfxLink )
	#
	# removeAllLinks
	#
	def removeAllLinks ( self ) :
		#
		if DEBUG_MODE : print '>> GfxNodeConnector::removeAllLinks (count = %d)' % len ( self.links )
		for gfxLink in list ( self.links ) : gfxLink.remove () 
	#
	# removeInputGfxLinks
	#
	def removeInputGfxLinks ( self ) : 
		#
		for gfxLink in self.getInputGfxLinks () : gfxLink.remove ()
	#
	#
	def remove ( self ) :
		#
		if DEBUG_MODE : print ( '>> GfxNodeConnector.remove' )
		if self.isNode () :
			inputGfxLinks = self.getInputGfxLinks ()
			outputGfxLinks = self.getOutputGfxLinks ()
			#
			# check if node is connected
			#
			if len ( inputGfxLinks ) > 0 and len ( outputGfxLinks ) > 0 :
				#
				# and try to preserve existing links
				#
				inputLink = inputGfxLinks [0] # it's supposed that only 1 input connecion allowed
				srcConnector = inputLink.srcConnector
				( srcNode, srcParam ) = inputLink.link.getSrc ()
				#
				# inputLink and corresponding node link will be removed from nodeNet
				#
				if usePyQt4 :
					self.scene().emit ( QtCore.SIGNAL ( 'onGfxLinkRemoved' ), inputLink )
				else :
					self.scene().onGfxLinkRemoved.emit ( inputLink )
					
				for gfxLink in outputGfxLinks :
					gfxLink.setSrcConnector ( srcConnector )
					srcNode.attachOutputParamToLink ( srcParam, gfxLink.link )
					gfxLink.link.setSrc ( srcNode, srcParam )

					gfxLink.link.dstNode.addChild ( srcNode )
					gfxLink.link.dstNode.removeChild ( self.getNode () )

				srcConnector.adjustLinks ()
			else :
				self.removeAllLinks ()
			if usePyQt4 :
				self.scene().emit ( QtCore.SIGNAL ( 'onGfxNodeRemoved' ), self )
			else :
				self.scene().onGfxNodeRemoved.emit ( self )
		else :
			self.removeAllLinks ()
	#
	# isInput
	#
	def isInput ( self ) : return self.param.isInput
	#
	# isOutput
	#
	def isOutput ( self ) : return not self.isInput ()
	#
	# isConnectedToInput
	#
	def isConnectedToInput ( self ) :
		#
		result = False
		if self.isNode () :
			#if DEBUG_MODE : print ( '* isConnectedToInput isNode' )
			outputGfxLinks = self.getOutputGfxLinks ()
			for gfxLink in outputGfxLinks :
				dstConnector = gfxLink.dstConnector
				if dstConnector is not None :
					result = dstConnector.isConnectedToInput ()
				if result is True :
					break
		else :
			result = self.isInput ()
		return result
	#
	# isConnectedToOutput
	#
	def isConnectedToOutput ( self ) :
		#
		result = False
		if self.isNode () :
			#if DEBUG_MODE : print '* isConnectedToOutput isNode'
			inputGfxLinks = self.getInputGfxLinks ()
			for gfxLink in inputGfxLinks :
				srcConnector = gfxLink.srcConnector
				if srcConnector is not None :
					result = srcConnector.isConnectedToOutput ()
				if result is True :
					break
		else :
			result = self.isOutput ()
		return result
	#
	# isNode
	#
	def isNode ( self ) : return ( self.node is not None )
	#
	# getNode
	#
	def getNode ( self ) : return self.getGfxNode ().node
	#
	# getGfxNode
	#
	def getGfxNode ( self ) :
		#
		node = self
		if not self.isNode () :
			node = self.parentItem ()
		return node
	#
	# isLinked
	#
	def isLinked ( self ) :
		#
		isLinked = False
		if len ( self.links ) > 0 : isLinked = True
		return isLinked
	#
	# hasThisLink
	#
	def hasThisLink ( self, tstLink ) :
		#
		hasLink = False
		cpyLink = copy.copy ( tstLink )
		cpyLink.dstConnector = self

		for link in self.links :
			if link.isEqual ( cpyLink ) :
				hasLink = True
				break
		return hasLink
	#
	# getInputLinks
	#
	def getInputLinks ( self ) : return self.getNode ().getInputLinks ()
	#
	# getOutputLinks
	#
	def getOutputLinks ( self ) : return self.getNode ().getOutputLinks ()
	#
	# getInputGfxLinks
	#
	def getInputGfxLinks ( self ) :
		#
		inputGfxLinks = []
		for gfxLink in self.links :
			if gfxLink.dstConnector == self :
				inputGfxLinks.append ( gfxLink )
		return inputGfxLinks
	#
	# getOutputGfxLinks
	#
	def getOutputGfxLinks ( self ) :
		#
		outputGfxLinks = []
		for gfxLink in self.links :
			if gfxLink.srcConnector == self :
				outputGfxLinks.append ( gfxLink )
		return outputGfxLinks
	#
	# adjustLinks
	#
	def adjustLinks ( self ) :
		#
		for link in self.links : link.adjust ()
	#
	# getScene
	#
	def getScene ( self ) :
		#
		scene = self.scene ()
		if not self.isNode () :
			scene = self.parentItem ().scene ()
		return scene
	#
	# itemChange
	#
	def itemChange ( self, change, value ) :
		#if DEBUG_MODE : print ">> itemChanged "
		if change == QtModule.QGraphicsItem.ItemSelectedHasChanged :
			#if DEBUG_MODE : print "* selection "
			self.isNodeSelected = ( value == 1 ) #value.toBool ()
			#if self.isNodeSelected :
			#  node = self.parentItem ().node
			#  if node is not None :
			#    if DEBUG_MODE : print ">> selected conector for node %s (id = %d)" % ( node.label, node.id )
		elif change == QtModule.QGraphicsItem.ItemPositionHasChanged :
			#if DEBUG_MODE : print "* position "
			if self.isNode () :
				#if DEBUG_MODE : print ">> ItemPositionHasChanged conector for node %s ( %d, %d )" % ( self.node.label, self.x(), self.y() )
				from meShaderEd import getDefaultValue
				grid_snap = getDefaultValue ( app_settings, 'WorkArea', 'grid_snap' )
				grid_size = int ( getDefaultValue ( app_settings, 'WorkArea', 'grid_size' )  )

				x = self.x()
				y = self.y()
				if grid_snap :
					#if DEBUG_MODE : print '* snap to grid  (size = %d)' % grid_size
					x -= ( x % grid_size )
					y -= ( y % grid_size )
					self.setPos ( x, y )

				#if DEBUG_MODE : print '* GfxNode.itemChange = ItemPositionHasChanged (%f, %f)' % ( x, y )
				self.node.offset = ( x, y )
				self.adjustLinks ()
				#return QtCore.QPointF ( x, y )

		return QtModule.QGraphicsItem.itemChange ( self, change, value )
	#
	# hilite
	#
	def hilite ( self, state ) :
		#
		self.isNodeSelected = state
		self.update()
	#
	#  onStartNodeLinkTest
	#
	def onStartNodeLinkTest ( self, connector ) :
		#
		if DEBUG_MODE : print '>> onStartNodeLinkTest'
		#if DEBUG_MODE : print msg
		if DEBUG_MODE : print connector	
		if DEBUG_MODE : print self
	#
	# mousePressEvent
	#
	def mousePressEvent ( self, event ) :
		#if DEBUG_MODE : print ">> mousePressEvent"
		#if DEBUG_MODE : print self
		self.hilite( True )
		if event.modifiers () == QtCore.Qt.ControlModifier :
			# start new ConnectorNode
			self.state = 'traceNodeConnector'
			if  usePyQt4 :
				self.getScene ().emit ( QtCore.SIGNAL ( 'startNodeConnector' ), self, event.scenePos () )
			else :
				self.getScene ().startNodeConnector.emit ( self, event.scenePos () )
		else :
			if not self.isNode () :
				# start new link
				self.state = 'traceNodeLink'
				if  usePyQt4 :
					self.getScene ().emit ( QtCore.SIGNAL ( 'startNodeLink' ), self  )
				else :
					#if DEBUG_MODE : print '* startNodeLink.emit '
					#if DEBUG_MODE : print self
					self.getScene ().startNodeLink.emit ( self )
		if self.state != 'idle' :
			self.grabMouse ()
			event.accept ()
		else :
			QtModule.QGraphicsItem.mousePressEvent ( self, event )
	#
	# mouseMoveEvent
	#
	def mouseMoveEvent ( self, event ) :
		#print ">> mouseMoveEvent at %d %d" % ( event.scenePos().x(), event.scenePos().y() )
		if self.state == 'traceNodeLink' :
			if  usePyQt4 :
				self.getScene ().emit ( QtCore.SIGNAL ( 'traceNodeLink' ), self, event.scenePos () )
			else :
				self.getScene ().traceNodeLink.emit ( self, event.scenePos () )
		elif self.state == 'traceNodeConnector' :
			if  usePyQt4 :
				self.getScene ().emit ( QtCore.SIGNAL ( 'traceNodeConnector' ), self, event.scenePos () )
			else :
				self.getScene ().traceNodeConnector.emit (  self, event.scenePos () )
		if self.state != 'idle' :
			event.accept()
		else :
			QtModule.QGraphicsItem.mouseMoveEvent ( self, event )
	#
	# mouseReleaseEvent
	#
	def mouseReleaseEvent ( self, event ) :
		#print ">> mouseReleaseEvent"
		if self.state == 'traceNodeLink' :
			if  usePyQt4 :
				self.getScene ().emit ( QtCore.SIGNAL ( 'endNodeLink' ), self, event.scenePos () )
			else :
				self.getScene ().endNodeLink.emit ( self, event.scenePos () )
		elif self.state == 'traceNodeConnector' :
			if  usePyQt4 :
				self.getScene ().emit ( QtCore.SIGNAL ( 'endNodeConnector' ), self, event.scenePos () )
			else :
				self.getScene ().endNodeConnector.emit ( self, event.scenePos () )
		if self.state != 'idle' :
			self.hilite ( False )
			self.state = 'idle'
			self.ungrabMouse ()
			event.accept ()
		else :
			QtModule.QGraphicsItem.mouseReleaseEvent ( self, event )

