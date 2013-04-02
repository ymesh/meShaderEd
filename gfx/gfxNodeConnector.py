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
  # __init__
  #
  def __init__ ( self, param = None, radius=5, isRound=True, node=None ) :
    #
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
      ( x, y ) = self.node.offset
      self.setPos ( x, y )

    #self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
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
    shape = QtGui.QPainterPath ()
    shape_rect = QtCore.QRectF ( self.rect )
    shape.addEllipse ( shape_rect )
    return shape
  #
  # paint
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
  # getCenterPoint
  #
  def getCenterPoint ( self ) : return self.mapToScene ( self.rect.center () )
  #
  # addLink (GfxLink)
  #
  def addLink ( self, link ) : self.links.append ( link )
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
    param = self.param
    if self.isNode () :
      param = self.node.outputParams [ 0 ]
    return param
  #
  # removeLink
  #
  def removeLink ( self, gfxLink ) :
    print '>> GfxNodeConnector removeLink'
    if gfxLink in self.links : self.links.remove ( gfxLink )
  #
  # removeAllLinks
  #
  def removeAllLinks ( self ) :
    print '>> GfxNodeConnector removeAllLinks (%d)' % len ( self.links )
    for gfxLink in list ( self.links ) :
      gfxLink.remove () # link will be removed from list
  #
  # removeInputGfxLinks
  #
  def removeInputGfxLinks ( self ) :
    for gfxLink in self.getInputGfxLinks () :
      gfxLink.remove ()
  #
  #
  def remove ( self ) :
    if DEBUG_MODE : print '>> GfxNodeConnector remove gfxNode (temp)'
    if self.isNode () :
      # !!! temporary solution
      # TODO! check if node is connected
      # and replace existing links
      self.removeAllLinks ()
    self.scene().emit ( QtCore.SIGNAL ( 'onGfxNodeRemoved' ), self )
  #
  # isInput
  #
  def isInput ( self ): return self.param.isInput
  #
  # isOutput
  #
  def isOutput ( self ): return not self.isInput () 
  #
  # isConnectedToInput
  #
  def isConnectedToInput ( self ) : 
    result = False
    if self.isNode () :
      #if DEBUG_MODE : print '* isConnectedToInput isNode'
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
  def getNode ( self ) : 
    return self.getGfxNode ().node
  #
  # getGfxNode
  #
  def getGfxNode ( self ) :
    node = self
    if not self.isNode () :
      node = self.parentItem ()
    return node
  #
  # isLinked
  #
  def isLinked ( self ) :
    isLinked = False
    if len ( self.links ) > 0 : isLinked = True
    return isLinked
  #
  # hasThisLink
  #
  def hasThisLink ( self, tstLink ) :
    hasLink = False
    cpyLink = copy.copy( tstLink )
    cpyLink.dstConnector = self

    for link in self.links :
      if link.isEqual ( cpyLink ) :
        hasLink = True
        break
    return hasLink
  #
  # getInputLinks
  #
  def getInputLinks ( self ) :
    inputLinks = []
    nodeInputLinks = self.getNode ().inputLinks
    for link in nodeInputLinks.values () :
      inputLinks.append ( link )
    return inputLinks
  #
  # getOutputLinks
  #
  def getOutputLinks ( self ) :
    outputLinks = []
    nodeOutputLinks = self.getNode ().outputLinks
    for link_list in nodeOutputLinks.values () :
      for link in link_list :
        outputLinks.append ( link )
    return outputLinks
  #
  # getInputGfxLinks
  #
  def getInputGfxLinks ( self ) :
    inputGfxLinks = []
    for gfxLink in self.links :
      if gfxLink.dstConnector == self :
        inputGfxLinks.append ( gfxLink )
    return inputGfxLinks
  #
  # getOutputGfxLinks
  #
  def getOutputGfxLinks ( self ) :
    outputGfxLinks = []
    for gfxLink in self.links :
      if gfxLink.srcConnector == self :
        outputGfxLinks.append ( gfxLink )
    return outputGfxLinks
  #
  # adjustLinks
  #
  def adjustLinks ( self ) :
    # print ">> Connected links = %d" % len ( self.links )
    for link in self.links : link.adjust ()
  #
  # getScene
  #
  def getScene ( self ) :
    scene = self.scene ()
    if not self.isNode () :
      scene = self.parentItem ().scene ()
    return scene
  #
  # itemChange
  #
  def itemChange ( self, change, value ) :
    if change == QtGui.QGraphicsItem.ItemSelectedHasChanged :
      self.isNodeSelected = value.toBool ()
      #if self.isNodeSelected :
      #  node = self.parentItem ().node
      #  if node is not None :
      #    if DEBUG_MODE : print ">> selected conector for node %s (id = %d)" % ( node.label, node.id )
    elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
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

    return QtGui.QGraphicsItem.itemChange ( self, change, value )
  #
  # hilite
  #
  def hilite ( self, state ) :
    self.isNodeSelected = state
    self.update()
  #
  # mousePressEvent
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
  # mouseMoveEvent
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
  # mouseReleaseEvent
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

