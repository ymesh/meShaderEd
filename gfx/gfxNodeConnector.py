#===============================================================================
# gfxNodeConnector.py
#
#
#
#===============================================================================
import os, sys, copy
from PyQt4 import QtCore, QtGui

from meShaderEd import app_settings
from global_vars import DEBUG_MODE
#
# GfxNodeConnector
#
class GfxNodeConnector ( QtGui.QGraphicsItem ):
  Type = QtGui.QGraphicsItem.UserType + 5
  isRound = True
  #
  #
  def __init__ ( self, param = None, radius=2, isRound=True, node=None ):
    QtGui.QGraphicsItem.__init__ ( self )
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
      if DEBUG_MODE : print ">> GfxNodeConnector is movable ..."
      # flag (new from QT 4.6...)
      self.setFlag ( QtGui.QGraphicsItem.ItemSendsScenePositionChanges )
      self.setFlag ( QtGui.QGraphicsItem.ItemSendsGeometryChanges )

      # qt graphics stuff
      self.setFlag ( QtGui.QGraphicsItem.ItemIsMovable )
      self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
      self.setZValue ( 1 )

    #self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
  #
  #
  def type ( self ): return GfxNodeConnector.Type
  #
  #
  def boundingRect ( self ): return self.rect
  #
  #
  def getCenterPoint ( self ): return self.mapToScene ( self.rect.center () )
  #
  #
  def addLink ( self, link ): self.links.append ( link )
  #
  #
  def getFirstLink ( self ): return self.links[0] ##copy.copy( self.links[0] )
  #
  #
  def removeLink ( self, link ):
    print '>> GfxNodeConnector removeLink'
    if link in self.links : self.links.remove ( link )
  #
  #
  def removeAllLinks ( self ):
    print '>> GfxNodeConnector removeAllLinks (%d)' % len ( self.links )
    for link in list( self.links ) :
      link.remove () # link will be removed from list
      #self.links.remove ( link )
      #self.scene().removeItem ( link )
  #
  #
  def remove ( self ) :
    if DEBUG_MODE : print '>> GfxNodeConnector remove gfxNode (temp)'
    #for connect in self.inputConnectors : connect.removeAllLinks ()
    #for connect in self.outputConnectors : connect.removeAllLinks ()
    self.scene().emit ( QtCore.SIGNAL ( 'onGfxNodeRemoved' ), self )
  #
  #
  def isInput ( self ): return self.param.isInput
  #
  #
  def isNode ( self ): return ( self.node is not None)
  #
  #
  def isLinked ( self ):
    isLinked = False
    if len ( self.links ) > 0 : isLinked = True
    return isLinked
  #
  #
  def hasThisLink ( self, tstLink ):
    hasLink = False
    cpyLink = copy.copy( tstLink )
    cpyLink.dstConnector = self

    for link in self.links :
      if link.isEqual ( cpyLink ) :
        hasLink = True
        break
    return hasLink
  #
  #
  def shape ( self ) :
    shape = QtGui.QPainterPath ()
    shape_rect = QtCore.QRectF ( self.rect )
    shape.addEllipse ( shape_rect )
    return shape
  #
  #
  def paint ( self, painter, option, widget ) :
    pen = self.PenBorderNormal
    if self.isNodeSelected : #  isSelected()
      pen =  self.PenBorderSelected
      # brush = self.BrushNodeSelected

    painter.setPen ( pen )
    painter.setBrush ( self.brush )
    painter.drawEllipse ( self.rect )
    # print ( ">> GfxNodeConnector.paint" )
  #
  #
  def adjustLinks ( self ) :
    # print ">> Connected links = %d" % len ( self.links )
    for link in self.links : link.adjust ()
  #
  #
  def getScene ( self ) :
    scene = self.scene ()
    if not self.isNode () :
      scene = self.parentItem ().scene ()
    return scene
  #
  #
  def itemChange ( self, change, value ) :
    if change == QtGui.QGraphicsItem.ItemSelectedHasChanged :
      self.isNodeSelected = value.toBool ()
      #if self.isNodeSelected :
      #  node = self.parentItem ().node
      #  if node is not None :
      #    if DEBUG_MODE : print ">> selected conector for node %s (id = %d)" % ( node.label, node.id )
    elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
      #print ">> ItemPositionHasChanged conector for node %s (param = %d)" % ( node.label, self.param.label )
      if self.isNode () :
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

    return QtGui.QGraphicsItem.itemChange ( self, change, value )
  #
  #
  def hilite ( self, state ) :
    self.isNodeSelected = state
    self.update()
  #
  #
  def mousePressEvent ( self, event ) :
    #print ">> mousePressEvent"
    self.hilite( True )
    if event.modifiers () == QtCore.Qt.ControlModifier :
      # start new ConnectorNode
      self.state = 'traceNodeConnector'
      self.getScene ().emit ( QtCore.SIGNAL ( 'startNodeConnector' ), self, event.scenePos () )
    else :
      if not self.isNode () :
        # start new link
        self.state = 'traceNodeLink'
        self.getScene ().emit ( QtCore.SIGNAL ( 'startNodeLink' ), self  )

    if self.state != 'idle' :
      self.grabMouse ()
      event.accept ()
    else :
      QtGui.QGraphicsItem.mousePressEvent ( self, event )

  #
  #
  def mouseMoveEvent ( self, event ) :
    #print ">> mouseMoveEvent at %d %d" % ( event.scenePos().x(), event.scenePos().y() )
    if self.state == 'traceNodeLink' :
      self.getScene ().emit ( QtCore.SIGNAL ( 'traceNodeLink' ), self, event.scenePos () )
    elif self.state == 'traceNodeConnector' :
      self.getScene ().emit ( QtCore.SIGNAL ( 'traceNodeConnector' ), self, event.scenePos () )
    if self.state != 'idle' :
      event.accept()
    else :
      QtGui.QGraphicsItem.mouseMoveEvent ( self, event )

  #
  #
  def mouseReleaseEvent ( self, event ) :
    #print ">> mouseReleaseEvent"
    if self.state == 'traceNodeLink' :
      self.getScene ().emit ( QtCore.SIGNAL ( 'endNodeLink' ), self, event.scenePos () )
    elif self.state == 'traceNodeConnector' :
      self.getScene ().emit ( QtCore.SIGNAL ( 'endNodeConnector' ), self, event.scenePos () )



    if self.state != 'idle' :
      self.hilite ( False )
      self.state = 'idle'
      self.ungrabMouse ()
      event.accept ()
    else :
      QtGui.QGraphicsItem.mouseReleaseEvent ( self, event )

