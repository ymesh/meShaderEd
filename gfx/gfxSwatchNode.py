#===============================================================================
# gfxSwatchNode.py
#
#
#
#===============================================================================
import os, sys
from PyQt4 import QtCore, QtGui

from gfx.gfxNodeLabel import GfxNodeLabel
from gfx.gfxNodeConnector import GfxNodeConnector
from gfx.gfxLink import GfxLink

from global_vars import DEBUG_MODE, GFX_SWATCH_NODE_TYPE
from meShaderEd import app_settings
import gui.ui_settings as UI
#
# GfxNodeSwatch
#
class GfxSwatchNode ( QtGui.QGraphicsItem ) :
  #
  Type = GFX_SWATCH_NODE_TYPE
  #
  # __init__
  #
  def __init__ ( self, node = None, swatchSize = UI.SWATCH_SIZE ) :
    #
    QtGui.QGraphicsItem.__init__ ( self )

    self.brush = QtGui.QBrush ( QtGui.QColor( 128, 128, 128 ) )
    self.PenBorderNormal = QtGui.QPen( QtGui.QBrush( QtGui.QColor( 0, 0, 0 ) ),
                                   1.0,
                                   QtCore.Qt.SolidLine,
                                   QtCore.Qt.RoundCap,
                                   QtCore.Qt.RoundJoin )

    self.PenBorderSelected = QtGui.QPen( QtGui.QBrush( QtGui.QColor( 250, 250, 250 ) ),
                                   2.0,
                                   QtCore.Qt.SolidLine,
                                   QtCore.Qt.RoundCap,
                                   QtCore.Qt.RoundJoin )

    self.node = node
    self.inputConnectors = []

    self.isNodeSelected = False

    self.radius = UI.NODE_RADIUS
    self.swatchSize = UI.SWATCH_SIZE

    self.shadow_offset = UI.SHADOW_OFFSET
    self.shadow_opacity = UI.SHADOW_OPACITY

    shadowColor = QtGui.QColor( 0, 0, 0 )
    shadowColor.setAlphaF ( self.shadow_opacity )
    self.BrushShadow = QtGui.QBrush ( shadowColor )
    self.PenShadow = QtGui.QPen ( shadowColor )

    self.rect = QtCore.QRectF ( 0, 0, self.swatchSize, self.swatchSize )
    self.pixmap = None

    if self.node is not None :
      self.updateGfxNode ()
      ( x, y ) = self.node.offset
      self.setPos ( x, y )

    # flag (new from QT 4.6...)
    self.setFlag ( QtGui.QGraphicsItem.ItemSendsScenePositionChanges )
    self.setFlag ( QtGui.QGraphicsItem.ItemSendsGeometryChanges )

    # qt graphics stuff
    self.setFlag ( QtGui.QGraphicsItem.ItemIsMovable )
    self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
    self.setZValue ( 1 )

    #self.connectSignals ()
  #
  # connectSignals
  #
  def connectSignals ( self ) :
    #
    if  self.scene () is not None :
      QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'updateSwatch' ), self.updateSwatch )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self ) :
    #
    if  self.scene () is not None :
      QtCore.QObject.disconnect ( self.scene (), QtCore.SIGNAL ( 'updateSwatch' ), self.updateSwatch )
  #
  # type
  #
  def type ( self ) : return GfxSwatchNode.Type
  #
  # remove
  #
  def remove ( self ) :
    #
    if DEBUG_MODE : print '>> GfxSwatchNode.remove'
    for connect in self.inputConnectors : connect.removeAllLinks ()
    self.scene().emit ( QtCore.SIGNAL ( 'onGfxNodeRemoved' ), self )
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
  # updateGfxNode
  #
  def updateGfxNode ( self ) :
    # remove all GfxLinks
    for connect in self.inputConnectors : connect.removeAllLinks ()
    # remove all children
    for item in self.childItems () : self.scene ().removeItem ( item )

    #self.rect = QtCore.QRectF ( 0, 0, self.swatchSize, self.swatchSize )
    self.inputConnectors = []
    self.setupParams ()
    self.setupConnectors ()
    self.setupGeometry ()
  #
  # setupParams
  #
  def setupParams ( self ) :
    #
    # get known node parameters
    #
    for name in [ 'size' ] :
      param = self.node.getInputParamByName ( name )
      if param is not None :
        if name == 'size' :
          self.swatchSize = int ( param.value )
  #
  # setupConnectors
  #
  def setupConnectors ( self ) :
    #
    for param in self.node.inputParams :
      # ignore attributes
      if param.provider != 'attribute' :
        connector = GfxNodeConnector ( param, UI.CONNECTOR_RADIUS, node = None )
        self.inputConnectors.append ( connector )
  #
  # setupGeometry
  #
  def setupGeometry ( self ) :
    #
    self.rect = QtCore.QRectF ( 0, 0, self.swatchSize, self.swatchSize )
    ( x, y ) = ( 0, 0 )
    hi = self.rect.height () / ( len ( self.inputConnectors) + 1 )

    for connector in self.inputConnectors :
      connector.rect.moveTo ( x - connector.radius, y + hi - connector.radius )
      y += hi
      connector.setParentItem ( self )
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
  # adjustLinks
  #
  def adjustLinks ( self ) :
    # invalidate all the links attached
    for connect in self.inputConnectors : connect.adjustLinks ()
  #
  # itemChange
  #
  def itemChange ( self, change, value ) :
    #
    if change == QtGui.QGraphicsItem.ItemSelectedHasChanged : #ItemSelectedChange:
      if value.toBool () :
        items = self.scene ().items ()
        for i in range ( len ( items ) - 1, -1, -1 ) :
          if items [ i ].parentItem() is None :
            if items [ i ] != self :
              items [ i ].stackBefore ( self )
    elif change == QtGui.QGraphicsItem.ItemPositionHasChanged :
      from meShaderEd import getDefaultValue
      grid_snap = getDefaultValue ( app_settings, 'WorkArea', 'grid_snap' )
      grid_size = int ( getDefaultValue ( app_settings, 'WorkArea', 'grid_size' )  )
      x = self.x ()
      y = self.y ()
      if grid_snap :
        x -= ( x % grid_size )
        y -= ( y % grid_size )
        self.setPos ( x, y )
      self.node.offset = ( x, y )
      self.adjustLinks ()
    return QtGui.QGraphicsItem.itemChange ( self, change, value )
  #
  # paint
  #
  def paint ( self, painter, option, widget ) :
    # print ( ">> GfxSwatchNode.paint" )
    painter.setRenderHint ( QtGui.QPainter.Antialiasing )
    painter.setRenderHint ( QtGui.QPainter.SmoothPixmapTransform )

    self.paintShadow ( painter )

    pen = self.PenBorderNormal

    if self.isSelected () : pen =  self.PenBorderSelected

    painter.setPen ( QtCore.Qt.NoPen  )
    painter.setBrush ( self.brush ) # QtCore.Qt.NoBrush
    painter.drawRoundedRect ( self.rect, self.radius, self.radius, QtCore.Qt.AbsoluteSize )

    if self.pixmap is not None :
      if not self.pixmap.isNull () :
        #painter.drawPixmap ( 0, 0, self.pixmap.scaled ( self.swatchSize, self.swatchSize,  transformMode = QtCore.Qt.SmoothTransformation ) )
        imageBrush = QtGui.QBrush ( self.pixmap.scaled ( self.swatchSize, self.swatchSize,  transformMode = QtCore.Qt.SmoothTransformation ) )
        painter.setBrush ( imageBrush )

    painter.setPen ( pen )
    painter.drawRoundedRect ( self.rect, self.radius, self.radius, QtCore.Qt.AbsoluteSize )
  #
  # paintShadow
  #
  def paintShadow ( self, painter ) :
    #
    painter.setBrush ( self.BrushShadow )
    painter.setPen ( self.PenShadow )
    painter.drawRoundedRect ( self.shadowRect (), self.radius, self.radius, QtCore.Qt.AbsoluteSize )
  #
  # mouseDoubleClickEvent
  #
  def mouseDoubleClickEvent ( self, event ) :
    #
    print ">> GfxSwatchNode.mouseDoubleClickEvent"
    #QtCore.QObject.emit ( self.toGraphicsObject (), QtCore.SIGNAL ( 'updateSwatch' ) )
    #self.connectSignals ()
    #self.scene ().emit ( QtCore.SIGNAL ( 'updateSwatch' ) )
    self.updateSwatch ()
    #QtGui.QGraphicsView.mouseDoubleClickEvent ( self.scene (), event )
    event.accept()
  #
  # updateSwatch
  #
  def updateSwatch ( self ) :
    #
    print ">> GfxSwatchNode.updateSwatch"

    #self.disconnectSignals ()

    self.pixmap = None
    self.imageName = self.node.computeNode ()

    if self.imageName != '' :
      print ">> GfxSwatchNode.setImage name = %s" % self.imageName

      imageReader = QtGui.QImageReader ( self.imageName )
      self.pixmap = QtGui.QPixmap ()
      if imageReader.canRead () :
        image = imageReader.read ()
        if not self.pixmap.convertFromImage ( image ) :
          print "!! QPixmap can't convert %s" % self.imageName
      else:
        print "!! QImageReader can't read %s..." % self.imageName
        # print imageReader.supportedImageFormats ()
        print "!! Lets try PIL module ..."
        import Image
        image = Image.open ( self.imageName )
        # image.verify()

        import os
        from global_vars import app_global_vars

        tmpname = app_global_vars [ 'TempPath' ] + '/' + os.path.basename ( self.imageName + '.png' )
        print "** Save %s ..." % tmpname
        image.save ( tmpname )

        self.pixmap = QtGui.QPixmap ( tmpname )

      self.update ()
      #self.scene ().setSceneRect ( self.rect () )
      #self.scene ().update ( self.mapRectToParent ( self.rect () ) ) # self.mapRectToScene

    #self.connectSignals ()



