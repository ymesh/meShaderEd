"""

	gfxLink.py

"""
from core.mePyQt import QtCore, QtGui

from global_vars import DEBUG_MODE, GFX_LINK_TYPE
from meShaderEd import app_settings

if QtCore.QT_VERSION < 50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# GfxLink
#
class GfxLink ( QtModule.QGraphicsItem ) :
	#
	Type = GFX_LINK_TYPE
	isStraight = True
	#
	# createFromPoints
	#
	@staticmethod
	def createFromPoints ( srcP, dstP ) :
		gfxLink = GfxLink ()
		gfxLink.srcPoint = gfxLink.mapToItem ( gfxLink, srcP )
		gfxLink.dstPoint = gfxLink.mapToItem ( gfxLink, dstP )
		gfxLink.adjust ()

		return gfxLink
	#
	# createFromLink
	#
	@staticmethod
	def createFromLink ( link ):
		gfxLink = GfxLink ()
		gfxLink.link = link
		gfxLink.path = QtGui.QPainterPath ()
		gfxLink.adjust ()

		return gfxLink
	#
	# __init__
	#
	def __init__ ( self, link = None, srcConnector = None, dstConnector = None ) :
		#
		QtModule.QGraphicsItem.__init__ ( self )

		from meShaderEd import getDefaultValue
		self.isStraight = getDefaultValue ( app_settings, 'WorkArea', 'straight_links' )

		# qt graphics stuff
		self.brushSelected = QtGui.QBrush ( QtGui.QColor ( 250, 250, 250 ) )
		self.brushNormal = QtGui.QBrush ( QtGui.QColor ( 20, 20, 20 ) )
		self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
		self.setZValue( 0 )

		self.link = link

		self.rect = QtCore.QRectF ()
		self.points = []
		self.path = None
		self.isLinkSelected = False
		self.srcPoint = self.dstPoint = None
		self.srcConnector = self.dstConnector = None

		self.setSrcConnector ( srcConnector )
		self.setDstConnector ( dstConnector)

		if srcConnector != None :
			if srcConnector.isConnectedToInput () and not srcConnector.isConnectedToOutput (): 
				self.swapConnectors ()
	#
	# remove
	#
	def remove ( self ) :
		if DEBUG_MODE : print ">> GfxLink::remove"

		if self.srcConnector is not None :
			self.srcConnector.removeGfxLink ( self )
			#self.srcConnector = None
		if self.dstConnector is not None :
			self.dstConnector.removeGfxLink ( self )
			#self.dstConnector = None
		#if self.link is not None :
		scene = self.scene ()
		if scene != None :
			if DEBUG_MODE : print ">> GfxLink::remove emit( onGfxLinkRemoved )"
			scene.emit ( QtCore.SIGNAL ( 'onGfxLinkRemoved' ), self )
	#
	# type
	#
	def type ( self ) : return GfxLink.Type
	#
	# boundingRect
	#
	def boundingRect ( self ) : return self.rect
	#
	# shape
	#
	def shape ( self ) : return self.path
	#
	# swapConnectors
	#
	def swapConnectors ( self ):
		# swap source and destination
		src = self.srcConnector
		self.srcConnector = self.dstConnector
		self.dstConnector = src
	#
	# isDstConnectedTo
	#
	def isDstConnectedTo ( self, connector ) :
		connected = False
		if connector == self.dstConnector :
			connected = True
		return connected
	#
	# isEqual
	#
	def isEqual ( self, link ) :
		equal = False
		if self.srcConnector == link.srcConnector and self.dstConnector == link.dstConnector :
			equal = True
		elif self.srcConnector == link.dstConnector and self.dstConnector == link.srcConnector :
			equal = True
		return equal
	#
	# setSrcConnector
	#
	def setSrcConnector ( self, srcConnector ) :
		if srcConnector is not None :
			self.srcPoint = srcConnector.getCenterPoint ()
			self.srcConnector = srcConnector
			self.srcConnector.addGfxLink ( self )
	#
	# setDstConnector
	#
	def setDstConnector ( self, dstConnector ) :
		if dstConnector is not None :
			self.dstPoint = dstConnector.getCenterPoint ()
			self.dstConnector = dstConnector
			self.dstConnector.addGfxLink ( self )
	#
	# itemChange
	#
	def itemChange ( self, change, value ) :
		if change == QtGui.QGraphicsItem.ItemSelectedChange :
			self.isLinkSelected = value.toBool ()
		return QtGui.QGraphicsItem.itemChange ( self, change, value )
	#
	# setPoints
	#
	def setPoints ( self, srcP, dstP ) :
		self.srcPoint = self.mapToItem ( self, srcP )
		self.dstPoint = self.mapToItem ( self, dstP )
		self.adjust ()
	#
	# setSrcPoint
	#
	def setSrcPoint ( self, p ) :
		self.srcPoint = self.mapToItem ( self, p )
		self.adjust ()
	#
	# setDstPoint
	#
	def setDstPoint ( self, p ) :
		self.dstPoint = self.mapToItem ( self, p )
		self.adjust ()
	#
	# adjust
	#
	def adjust ( self ) :
		from meShaderEd import getDefaultValue
		self.isStraight = getDefaultValue ( app_settings, 'WorkArea', 'straight_links' )

		if self.srcConnector is not None : self.srcPoint = self.srcConnector.getCenterPoint ()
		if self.dstConnector is not None : self.dstPoint = self.dstConnector.getCenterPoint ()

		self.prepareGeometryChange ()

		del self.points [ : ]  # clear bezier points
		self.path = None
		if self.srcPoint is not None and self.dstPoint is not None :
			self.path = QtGui.QPainterPath ()
			# first point
			self.points.append ( self.srcPoint )
			self.path.moveTo ( self.points [ 0 ] )

			# draw curved spline if isStraight is False
			if not self.isStraight :
				# hull spline
				hull = QtCore.QRectF ( self.srcPoint, self.dstPoint )
				centerX = hull.center ().x ()
				centerY = hull.center ().y ()
				# second point
				offsetVX = min ( abs ( hull.topRight ().x () - hull.topLeft ().x () ) * 0.1, 40 )
				offsetVY = 0.0

				p1 = self.srcPoint + QtCore.QPointF ( offsetVX, offsetVY )
				self.points.append ( p1 )
				# third point
				p2 =   QtCore.QPointF ( centerX, self.srcPoint.y() )
				self.points.append ( p2 )
				# fourth point
				p3 = QtCore.QPointF ( centerX, centerY )
				self.points.append ( p3 )
				# fifth point (bezier tangent)
				p4 = QtCore.QPointF ( centerX, centerY )
				self.points.append ( p4 )
				# sixth point
				p5 = QtCore.QPointF ( centerX, self.dstPoint.y() )
				self.points.append ( p5 )
				# seventh point
				p6 = self.dstPoint - QtCore.QPointF ( offsetVX, offsetVY )
				self.points.append ( p6 )
			# last point
			self.points.append ( self.dstPoint )
			if self.isStraight :
				#if DEBUG_MODE : print '* GfxLink: Straight mode'
				self.path.lineTo ( self.dstPoint )
			else:
				#if DEBUG_MODE : print '* GfxLink: Curved mode'
				#self.path.cubicTo ( self.points[1], self.points[2], self.points[3] )
				#self.path.cubicTo ( self.points[5], self.points[6], self.points[7] )
				self.path.cubicTo ( p1, p1, p3 )
				self.path.cubicTo ( p6, p6, self.dstPoint )
			self.rect = self.path.boundingRect ()
	#
	# paint
	#
	def paint ( self, painter, option, widget ) :
		#
		if self.path is not None :
			painter.setRenderHint ( QtGui.QPainter.Antialiasing )
			brush = self.brushNormal
			if self.isLinkSelected : brush = self.brushSelected
			painter.setPen( QtGui.QPen ( brush,
																	1.25,
																	QtCore.Qt.SolidLine,
																	QtCore.Qt.RoundCap,
																	QtCore.Qt.RoundJoin
																)
										)
			painter.drawPath ( self.path )
