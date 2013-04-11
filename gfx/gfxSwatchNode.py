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

    self.brush = QtGui.QBrush ( QtGui.QColor ( 140, 140, 140 ) ) # ( 128, 128, 128 ) ( 132, 132, 132 )
    self.PenBorderNormal = QtGui.QPen ( QtGui.QColor ( 0, 0, 0 ) )
    self.PenBorderSelected = QtGui.QPen ( QtGui.QColor ( 240, 240, 240 ) )

    self.node = node
    self.inputConnectors = []
    
    self.isNodeSelected = False
    
    self.radius = UI.NODE_RADIUS
    self.swatchSize = UI.SWATCH_SIZE
    
    self.rect = QtCore.QRectF ( 0, 0, self.swatchSize, self.swatchSize )
    
    if self.node is not None :
      self.updateNode ()
      ( x, y ) = self.node.offset
      self.setPos ( x, y ) 
    
    # flag (new from QT 4.6...)
    self.setFlag ( QtGui.QGraphicsItem.ItemSendsScenePositionChanges )
    self.setFlag ( QtGui.QGraphicsItem.ItemSendsGeometryChanges )

    # qt graphics stuff
    self.setFlag ( QtGui.QGraphicsItem.ItemIsMovable )
    self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
    self.setZValue ( 1 )
  #
  # type
  #
  def type ( self ) : return GfxSwatchNode.Type
  #
  # updateNode
  #
  def updateNode ( self ) :
    # remove all GfxLinks
    for connect in self.inputConnectors : connect.removeAllLinks ()
    # remove all children
    for item in self.childItems () : self.scene().removeItem ( item )
    
    self.setupParams ()
    self.setupGeometry ()
  #
  # setupParams
  #
  def setupParams ( self ):
    self.inputConnectors = []
    for param in self.node.inputParams :
      # ignore attributes
      if param.provider != 'attribute' :
        connector = GfxNodeConnector ( param, UI.CONNECTOR_RADIUS, node = None )
        self.inputConnectors.append ( connector )
  #
  # setupGeometry
  #
  def setupGeometry ( self ):
    #
    x = 0
    y = 0
    hi = self.rect.height () / ( len ( self.inputConnectors) + 1 )
    
    for connector in self.inputConnectors :
      connector.rect.moveTo ( x - connector.radius, y + hi - connector.radius )
      y += hi
      connector.setParentItem ( self )
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
    shape.addRect ( self.rect )
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
  def itemChange ( self, change, value ):
    if change == QtGui.QGraphicsItem.ItemSelectedHasChanged : #ItemSelectedChange:
      if value.toBool () :
        items = self.scene ().items ()
        for i in range ( len ( items ) - 1, -1, -1 ) :
          if items [ i ].parentItem() is None :
            if items [ i ] != self :
              items [ i ].stackBefore ( self )
    elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
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
    pen = self.PenBorderNormal
    
    if self.isSelected () :
      pen =  self.PenBorderSelected
      # brush = self.BrushNodeSelected
    painter.setPen ( pen )
    painter.setBrush ( self.brush )
    painter.drawRoundedRect ( self.rect, self.radius, self.radius, QtCore.Qt.AbsoluteSize )
