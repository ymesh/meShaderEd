#===============================================================================
# WorkArea.py
#
#
#
#===============================================================================
import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *

from core.nodeLink import NodeLink
from core.connectorNode import ConnectorNode

from gfx.gfxNode import GfxNode
from gfx.gfxNodeConnector import GfxNodeConnector
from gfx.gfxLink import GfxLink
from gfx.gfxNote import GfxNote

from meShaderEd import app_settings
from global_vars import DEBUG_MODE

#from ui_workArea import Ui_workArea
#
# WorkArea
#
class WorkArea ( QtGui.QGraphicsView ) :
  #
  #
  #
  def __init__ ( self ):
    QtGui.QGraphicsView.__init__ ( self )

    self.drawGrid = True
    self.gridSnap = False
    self.straightLinks = False
    self.reverseFlow = False

    self.gridSize = 10
    self.minGap = 120
    self.current_Z = 1

    self.state = 'idle'
    self.panStartPos = None

    self.lastConnectCandidate = None
    self.currentGfxLink = None

    self.inspectedNode = None
    self.nodeNet = None

    self.selectedNodes = []
    self.selectedLinks = []

    # set scene
    scene = QtGui.QGraphicsScene ( self )

    scene.setSceneRect ( -10000, -10000, 20000, 20000 )
    #scene.setItemIndexMethod ( QtGui.QGraphicsScene.NoIndex )
    self.setScene ( scene )

    # qt graphics stuff
    self.setCacheMode ( QtGui.QGraphicsView.CacheBackground )
    self.setRenderHint ( QtGui.QPainter.Antialiasing )

    self.setTransformationAnchor ( QtGui.QGraphicsView.AnchorUnderMouse )
    self.setResizeAnchor ( QtGui.QGraphicsView.AnchorViewCenter )
    self.setDragMode ( QtGui.QGraphicsView.RubberBandDrag )

    self.setMouseTracking ( False )
    self.setAcceptDrops ( True )
    """
    viewport = self.viewport()
    if viewport is not None :
      print ">> WorkArea viewport.setAcceptTouchEvents"
      #proxy = QtGui.QGraphicsProxyWidget ()
      proxy = viewport.graphicsProxyWidget ()
      if proxy is not None :
        proxy.setAcceptTouchEvents ( True )

      #self.setAttribute ( QtGui.AcceptTouchEvents, True )
      #viewport()->setAttribute(Qt::WA_AcceptTouchEvents);
      #setDragMode(ScrollHandDrag);
      #Qt::WA_AcceptTouchEvents
    """
    self.viewBrush = QtGui.QBrush ( QtGui.QColor ( 148, 148, 148 ) )
    self.setBackgroundBrush ( self.viewBrush )

    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'selectionChanged()' ), self.onSelectionChanged )

    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'startNodeLink' ), self.onStartNodeLink )
    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'traceNodeLink' ), self.onTraceNodeLink )
    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'endNodeLink' ), self.onEndNodeLink )

    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'startNodeConnector' ), self.onStartNodeConnector )
    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'traceNodeConnector' ), self.onTraceNodeConnector )
    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'endNodeConnector' ), self.onEndNodeConnector )

    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'onGfxNodeRemoved' ), self.onRemoveNode )
    QtCore.QObject.connect ( self.scene (), QtCore.SIGNAL ( 'onGfxLinkRemoved' ), self.onRemoveLink )

    if DEBUG_MODE : print ">> WorkArea:: __init__"
  #
  # drawBackground
  #
  def drawBackground ( self, painter, rect ) :
    sc_rect = self.sceneRect ()
    bbrush = QtGui.QBrush( QtGui.QColor ( 148, 148, 148 ) ) ## painter.background()
    painter.fillRect ( rect, bbrush )

    if self.drawGrid :
    #  print( "grid size = %d" % self.gridSize )
      gr_pen = QtGui.QPen ( QtGui.QColor ( 180, 180, 180 ) )
      gr_pen.setWidth ( 0 )
      painter.setPen ( gr_pen )
      for x in range ( int ( sc_rect.x () ), int ( sc_rect.right () ), self.gridSize ):
        painter.drawLine ( x, sc_rect.y (), x, sc_rect.bottom () )
      for y in range ( int ( sc_rect.y () ), int ( sc_rect.bottom () ), self.gridSize ):
        painter.drawLine ( sc_rect.x (), y, sc_rect.right (), y )

  #
  # Returns a list of GfxNodes in the scene for given type
  # or all nodes if type == None
  #
  def getGfxNodesByType ( self, type = None ) :
    resultList = []
    for item in self.scene ().items () :
      if ( isinstance ( item, GfxNode ) or
           ( isinstance ( item, GfxNodeConnector ) and item.isNode () ) ) :
        if type is None or item.node.type == type :
          print '>> item.node.type = %s' % item.node.type
          resultList.append ( item )
    return resultList
  #
  # Returns GfxNodes for given Node
  #
  def getGfxNodesByNode ( self, node = None ) :
    gfxNode = None
    for item in self.scene ().items () :
      if ( isinstance ( item, GfxNode ) or ( isinstance ( item, GfxNodeConnector ) and item.isNode () ) ) :
        if item.node == node :
          gfxNode = item
          break
    return gfxNode
  #
  # selectAllNodes
  #
  def selectAllNodes ( self ) :
    for item in self.getGfxNodesByType ( None ) :
      item.setSelected ( True )
  #
  # selectAbove
  #
  def selectAbove ( self, upperGfxNode ) :
    #
    if DEBUG_MODE : print '>> WorkArea::selectAbove upperGfxNode.node (%s) links:' % upperGfxNode.node.label
    for link_list in upperGfxNode.node.outputLinks.values () :
      for link in link_list :
        link.printInfo ()
        gfxNode = self.getGfxNodesByNode ( link.dstNode )
        gfxNode.setSelected ( True )
        self.selectAbove ( gfxNode )
  #
  # selectBelow
  #
  def selectBelow ( self, upperGfxNode ) :
    #
    if DEBUG_MODE : print '>> WorkArea::selectBelow upperGfxNode.node (%s) children:' % upperGfxNode.node.label
    for node in upperGfxNode.node.childs :
      if DEBUG_MODE : print '* %s' % node.label
      gfxNode = self.getGfxNodesByNode ( node )
      gfxNode.setSelected ( True )
      self.selectBelow ( gfxNode )
  #
  # setNodeNetwork
  #
  def setNodeNetwork ( self, nodeNet ) : self.nodeNet = nodeNet
  #
  #
  def clear ( self ):
    if DEBUG_MODE : print '>> WorkArea:: clearing nodes ...'
    for item in self.scene ().items () : self.scene ().removeItem ( item )
    self.nodeNet.clear ()
    self.state = 'idle'
    self.panStartPos = None
    self.lastConnectCandidate = None
    self.currentGfxLink = None
    self.inspectedNode = None
  #
  # addGfxLink
  #
  def addGfxLink ( self, link ) :
    #
    if DEBUG_MODE : print '>> WorkArea::addGfxLink (id=%d)' % link.id
    gfxLink = GfxLink ( link )
    srcNode = link.srcNode
    dstNode = link.dstNode
    srcParam = link.srcParam
    dstParam = link.dstParam
    srcConnector = None
    dstConnector = None
    for item in self.scene ().items ():
      if isinstance ( item, GfxNode ) :
        if item.node == srcNode :
          srcConnector = item.getOutputConnectorByParam ( srcParam )
        elif item.node == dstNode :
          dstConnector = item.getInputConnectorByParam ( dstParam )
      elif isinstance ( item, GfxNodeConnector ) and item.isNode () :
        if item.node == srcNode :
          srcConnector = item
        elif item.node == dstNode :
          dstConnector = item
      if ( srcConnector != None and dstConnector != None ) :
        break
    gfxLink.setSrcConnector ( srcConnector )
    gfxLink.setDstConnector ( dstConnector )
    gfxLink.adjust ()
    self.scene ().addItem ( gfxLink )
  #
  # Node already in NodeNet, so add new GfxNode to scene
  #
  def addGfxNode ( self, node, pos = None ) :
    #
    #print ( ">> WorkArea: addGfxNode %s" % node.label )
    if node.type == 'connector' :
      gfxNode = GfxNodeConnector ( node.inputParams [ 0 ], node = node )
    elif node.type == 'note' :
      gfxNode = GfxNote ( node )
    else :
      gfxNode = GfxNode ( node )
    scene = self.scene ()
    if pos != None : gfxNode.moveBy ( pos.x(), pos.y() )
    #for item in scene.selectedItems (): item.setSelected ( False )
    scene.addItem ( gfxNode )
    gfxNode.setSelected ( True )
    self.emit ( QtCore.SIGNAL ( 'gfxNodeAdded' ), gfxNode )
  #
  # adjustLinks
  #
  def adjustLinks ( self ) :
    for item in self.scene ().items () :
      if isinstance ( item, GfxLink ): item.adjust ()
  #
  # onSelectionChanged
  #
  def onSelectionChanged ( self ) :
    #
    #print ">> WorkArea: onSelectionChanged "
    self.selectedNodes = []
    self.selectedLinks = []
    selected = self.scene ().selectedItems ()

    for item in selected:
      if   isinstance ( item, GfxNode ): self.selectedNodes.append ( item )
      elif isinstance ( item, GfxNote ): self.selectedNodes.append ( item )
      elif isinstance ( item, GfxNodeConnector ): self.selectedNodes.append ( item )
      elif isinstance ( item, GfxLink ): self.selectedLinks.append ( item )

    self.emit ( QtCore.SIGNAL ( 'selectNodes' ), self.selectedNodes, self.selectedLinks )
  #
  # lastConnectCandidateReset
  #
  def lastConnectCandidateReset ( self ) :
    #
    if self.lastConnectCandidate is not None :
      self.lastConnectCandidate.hilite( False )
    self.lastConnectCandidate = None
  #
  # isLinkAcceptable
  #
  def isLinkAcceptable ( self, connector, connectCandidate ) :
    #
    isAcceptable = False
    if isinstance ( connectCandidate, GfxNodeConnector ):
      # do not connect to itself
      if connectCandidate != connector :
        # do not connect to the same node
        if connectCandidate.parentItem () != connector.parentItem () :
          # do not connect the same link to connector twice
          if not connectCandidate.hasThisLink ( self.currentGfxLink ) :
            # connect only to similar type
            if connector.param.encodedTypeStr() == connectCandidate.param.encodedTypeStr () :
              if not connectCandidate.isNode () :
                # connect only input with output and vice versa
                if connector.param.isInput != connectCandidate.param.isInput :
                    isAcceptable = True
              else :
                # we have nodeConnector
                isAcceptable = True

    return isAcceptable
  #
  # onStartNodeLink
  #
  def onStartNodeLink ( self, connector ):
    #
    srcNode = connector.getNode ()
    srcParam = connector.param
    if DEBUG_MODE : print '>> WorkArea::onStartNodeLink from %s (%s)' % ( srcNode.label, srcParam.label )

    srcConnector = connector
    self.state = 'traceNodeLink'
    self.lastConnectCandidate = None

    if connector.isInput () and connector.isLinked () :
      oldLink = connector.getFirstGfxLink ()
      srcConnector = oldLink.srcConnector
      oldLink.remove ()

    gfxLink = GfxLink ( None, srcConnector )
    self.scene ().addItem ( gfxLink )
    self.currentGfxLink = gfxLink
    self.currentGfxLink.isLinkSelected = True
  #
  # onTraceNodeLink
  #
  def onTraceNodeLink ( self, connector, scenePos ) :
    # node = connector.parentItem().node
    # print ">> WorkArea: onDrawNodeLink from %s (%d %d)" % ( node.label, scenePos.x(), scenePos.y() )
    connectCandidate = self.scene ().itemAt ( scenePos )
    srcConnector = self.currentGfxLink.srcConnector
    swappedLink = False
    if srcConnector is None : # link has swapped connectors
      srcConnector = self.currentGfxLink.dstConnector
      swappedLink = True

    if self.isLinkAcceptable ( srcConnector, connectCandidate ) :
      if connectCandidate != self.lastConnectCandidate :
        self.lastConnectCandidateReset ()
        connectCandidate.hilite ( True )
        self.lastConnectCandidate = connectCandidate
        # link_node = connectCandidate.parentItem().node
        # print ">> WorkArea: onDrawNodeLink to %s" % link_node.label
      else :
        scenePos = self.lastConnectCandidate.getCenterPoint () # snap to last position
        pass
        # self.lastConnectCandidateReset()
    else :
      self.lastConnectCandidateReset ()

    #if self.currentGfxLink is not None :
    if swappedLink :
      self.currentGfxLink.setSrcPoint ( scenePos )
    else :
      self.currentGfxLink.setDstPoint ( scenePos )
  #
  # onEndNodeLink
  #
  def onEndNodeLink ( self, connector, scenePos ) :
    #
    srcConnector = self.currentGfxLink.srcConnector
    dstConnector = self.currentGfxLink.dstConnector
    swappedLink = False
    if srcConnector is None : # link has swapped connectors
      swappedLink = True

    if self.lastConnectCandidate is None :
      self.currentGfxLink.remove ()
      #self.emit( QtCore.SIGNAL( 'nodeParamChanged' ), srcConnector.parentItem(), srcConnector.param )
      #self.emit( QtCore.SIGNAL( 'nodeParamChanged' ), dstConnector.parentItem(), dstConnector.param )
    else :
      if self.lastConnectCandidate.isNode () :
        # if connection was made to ConnectorNode
        if dstConnector is None :
          self.lastConnectCandidate.removeInputGfxLinks ()
      else :
        # remove old link first if it exists
        if self.lastConnectCandidate.isInput () and self.lastConnectCandidate.isLinked () :
          #oldLink = self.lastConnectCandidate.getFirstLink ()
          #oldLink.remove ()
          self.lastConnectCandidate.removeInputGfxLinks ()

      self.currentGfxLink.isLinkSelected = False
      self.currentGfxLink.update ()

      srcNode = dstNode = None
      srcParam = dstParam = None

      if swappedLink :
        srcNode = self.lastConnectCandidate.getNode ()
        srcParam = self.lastConnectCandidate.param
        if self.lastConnectCandidate.isNode () :
          srcParam = self.lastConnectCandidate.getFirstOutputParam ()
        dstNode = dstConnector.getNode ()
        dstParam = dstConnector.param
        self.currentGfxLink.setSrcConnector ( self.lastConnectCandidate )
      else :
        srcNode = srcConnector.getNode ()
        srcParam = srcConnector.param
        dstNode = self.lastConnectCandidate.getNode ()
        dstParam = self.lastConnectCandidate.param
        if self.lastConnectCandidate.isNode () :
          dstParam = self.lastConnectCandidate.getFirstInputParam ()
        self.currentGfxLink.setDstConnector ( self.lastConnectCandidate )

      link = NodeLink.build ( srcNode, dstNode, srcParam, dstParam )

      #if not dstParam.isInput :
        # swap source and destination
      #  self.currentGfxLink.swapConnectors ()
      #  link.swapNodes ()

      self.currentGfxLink.link = link
      self.nodeNet.addLink ( link )
      #self.emit ( QtCore.SIGNAL ( 'nodeConnectionChanged' ), self.currentGfxLink.srcConnector.getGfxNode (), self.currentGfxLink.srcConnector.param )
      self.emit ( QtCore.SIGNAL ( 'nodeConnectionChanged' ), self.currentGfxLink.dstConnector.getGfxNode (), self.currentGfxLink.dstConnector.param )

    self.lastConnectCandidateReset ()
    self.currentGfxLink = None
    self.state = 'idle'
  #
  # onStartNodeConnector
  #
  def onStartNodeConnector ( self, connector, scenePos  ) :
    #
    if DEBUG_MODE : print '>> WorkArea::onStartNodeConnector'
    self.state = 'traceNodeConnector'

    newNode = ConnectorNode ()
    self.nodeNet.addNode ( newNode )

    newParam = connector.param.copy ()
    newParam.isInput = False
    newInParam = newParam.copy ()
    newOutParam = newParam.copy ()

    newNode.addInputParam ( newInParam )
    newNode.addOutputParam ( newOutParam )

    newConnector = GfxNodeConnector ( newParam, connector.radius, node = newNode )
    newConnector.brush = connector.brush
    newConnector.setPos ( scenePos )
    newConnector.moveBy ( -connector.radius, -connector.radius )

    self.lastConnectCandidate = newConnector
    self.scene ().addItem ( newConnector )
    newConnector.hilite ( True )

    srcNode = connector.getNode ()
    srcParam = connector.getOutputParam ()
    dstNode = newConnector.getNode ()
    dstParam = newConnector.getInputParam ()

    #
    # swap link direction only for connectors
    # in open chain connected to input node parameter
    #
    swappedLink = False
    if connector.isConnectedToInput () and not connector.isConnectedToOutput () :
      if DEBUG_MODE : print '*** swap link direction ***'
      swappedLink = True
      srcNode = newConnector.getNode ()
      srcParam = newConnector.getOutputParam ()
      dstNode = connector.getNode ()
      dstParam = connector.getInputParam ()

    link = NodeLink.build ( srcNode, dstNode, srcParam, dstParam )
    # if swappedLink : link.swapNodes ()
    self.nodeNet.addLink ( link )

    #if DEBUG_MODE : self.nodeNet.printInfo ()

    # preserve existing links for parameter connectors
    if connector.isLinked () and not connector.isNode () :
      if connector.isInput () :
        #print '*** preserve input ***'
        # TODO!!!
        # This is very rough code -- needs to be wrapped in functions
        gfxLinks = connector.getInputGfxLinks ()
        for gfxLink in gfxLinks :
          gfxLink.setDstConnector ( newConnector )

          # remove gfxLink from previouse connector
          connector.removeLink ( gfxLink )

          # adjust destination for node link
          newConnector.getNode ().attachInputParamToLink ( newConnector.getInputParam (), gfxLink.link )
          newConnector.getNode ().childs.add ( gfxLink.link.srcNode )
          connector.getNode ().childs.remove ( gfxLink.link.srcNode )

          gfxLink.link.dstNode = newConnector.getNode ()
          gfxLink.link.dstParam = newConnector.getInputParam ()
      else :
        #print '*** preserve output ***'
        gfxLinks = connector.getOutputGfxLinks ()
        for gfxLink in gfxLinks :
          gfxLink.setSrcConnector ( newConnector )

          # remove gfxLink from previouse connector
          connector.removeLink ( gfxLink )

          # adjust source for node link
          connector.getNode ().detachOutputParamFromLink ( gfxLink.link.srcParam, gfxLink.link )
          newConnector.getNode ().attachOutputParamToLink ( newConnector.getOutputParam (), gfxLink.link )
          #newConnector.getNode ().childs.add ( connector.getNode () )
          gfxLink.link.dstNode.childs.add ( newConnector.getNode () )
          gfxLink.link.dstNode.childs.remove ( connector.getNode () )

          gfxLink.link.srcNode = newConnector.getNode ()
          gfxLink.link.srcParam = newConnector.getOutputParam ()

      #if DEBUG_MODE : self.nodeNet.printInfo ()

    gfxLink = GfxLink ( link, connector, newConnector  )
    self.scene ().addItem ( gfxLink )


  #
  # onTraceNodeConnector
  #
  def onTraceNodeConnector ( self, connector, scenePos ) :
    #
    #if DEBUG_MODE : print '>> WorkArea::onTraceNodeConnector'
    if self.lastConnectCandidate is not None :
      self.lastConnectCandidate.setPos ( scenePos )
      self.lastConnectCandidate.moveBy ( -connector.radius, -connector.radius )
   #
  # onEndNodeConnector
  #
  def onEndNodeConnector ( self, connector, scenePos ) :
    #
    if DEBUG_MODE : print '>> WorkArea::onEndNodeConnector'
    print '>> lastConnectCandidate.node.type = %s' % self.lastConnectCandidate.node.type
    self.lastConnectCandidateReset ()
    self.state = 'idle'
  #
  # onRemoveNode
  #
  def onRemoveNode ( self, gfxNode ) :
    print ">> WorkArea: onRemoveNode"
    self.emit ( QtCore.SIGNAL ( 'gfxNodeRemoved' ), gfxNode )
    self.scene ().removeItem ( gfxNode )
    self.nodeNet.removeNode ( gfxNode.node )
  #
  # onRemoveLink
  #
  def onRemoveLink ( self, gfxLink ) :
    #print ">> WorkArea: onRemoveLink"
    self.scene ().removeItem ( gfxLink )
    if gfxLink.link is not None :
      srcConnector = gfxLink.srcConnector
      dstConnector = gfxLink.dstConnector
      self.nodeNet.removeLink ( gfxLink.link )
      if srcConnector is not None :
        if DEBUG_MODE : print 'srcConnector.parentItem().node.label = %s ' % srcConnector.getNode ().label
        #self.emit( QtCore.SIGNAL( 'nodeConnectionChanged' ), srcConnector.parentItem(), srcConnector.param )
      if dstConnector is not None :
        if DEBUG_MODE : print 'dstConnector.parentItem().node.label = %s ' % dstConnector.getNode ().label
        self.emit ( QtCore.SIGNAL ( 'nodeConnectionChanged' ), dstConnector.getGfxNode (), dstConnector.param )
  #
  # removeSelected
  #
  def removeSelected ( self ):
    if DEBUG_MODE : print '>> WorkArea::removeSelected: (before) nodes = %d links = %d' % ( len (  self.nodeNet.nodes.values () ), len ( self.nodeNet.links.values () ) )
    selected = self.scene().selectedItems()

    for item in selected:
      if ( isinstance ( item, GfxLink ) or
           isinstance ( item, GfxNode ) or
           isinstance ( item, GfxNote ) or
         ( isinstance ( item, GfxNodeConnector ) and item.isNode () ) ) : item.remove ()

    if DEBUG_MODE : print '>> WorkArea::removeSelected (after) nodes = %d links = %d' % ( len ( self.nodeNet.nodes.values ()), len ( self.nodeNet.links.values ()) )
  #
  # dragEnterEvent
  #
  def dragEnterEvent ( self, event ):
    print '>> WorkArea::onDragEnterEvent'
    #for form_str in event.mimeData().formats():
    #  print str ( form_str )
    #  if form_str == 'text/uri-list' :
    #    print event.mimeData().data( 'text/uri-list' )
    mimedata = event.mimeData ()

    if mimedata.hasFormat ( 'application/x-text' ) or mimedata.hasFormat ( 'text/uri-list' ):
      event.accept ()
    else:
      event.ignore ()
  #
  # dragMoveEvent
  #
  def dragMoveEvent ( self, event ):
    #print ">> WorkArea: onDragMoveEvent"
    mimedata = event.mimeData ()
    if mimedata.hasFormat ( 'application/x-text' ) or mimedata.hasFormat ( 'text/uri-list' ):
      event.setDropAction ( QtCore.Qt.CopyAction )
      event.accept ()
    else:
      event.ignore ()
  #
  # dropEvent
  #
  def dropEvent ( self, event ):
    if DEBUG_MODE : print ">> WorkArea: onDropEvent"
    file_list = []
    mimedata = event.mimeData ()

    if mimedata.hasFormat ( 'application/x-text' ) :
      # decode drop stuff
      data = mimedata.data ( 'application/x-text' )
      stream = QtCore.QDataStream ( data, QtCore.QIODevice.ReadOnly )
      filename = QtCore.QString ()
      stream >> filename

      if DEBUG_MODE : print 'itemFilename = %s' % ( filename )

      file_list.append ( filename )
      event.setDropAction ( QtCore.Qt.CopyAction )
      event.accept ()
    elif mimedata.hasFormat ( 'text/uri-list' ) :
      data = str ( mimedata.data( 'text/uri-list' ).data() )
      #print data
      for item in data.split () :
        filename = str ( QtCore.QUrl( item ).toLocalFile () )

        ( name, ext ) = os.path.splitext( os.path.basename( filename ) )
        if DEBUG_MODE : print ':: %s (%s)' % ( filename, ext )
        if ext == '.xml' :
          file_list.append ( filename )
    else:
      event.ignore ()

    for file_name in file_list : self.insertNodeNet ( file_name, self.mapToScene( event.pos () ) )
  #
  # keyPressEvent
  #
  def keyPressEvent ( self, event ) :
    #print ">> WorkArea: keyPressEvent"
    QtGui.QGraphicsView.keyPressEvent ( self, event)
  #
  # wheelEvent
  #
  def wheelEvent ( self, event ):
    #print ">> WorkArea: wheelEvent"
    # QtGui.QGraphicsView.wheelEvent( self, event)
    scale = -1.0
    if 'linux' in sys.platform: scale = 1.0
    import math
    scaleFactor = math.pow( 2.0, scale * event.delta() / 600.0 )
    factor = self.matrix().scale( scaleFactor, scaleFactor ).mapRect( QtCore.QRectF( -1, -1, 2, 2 ) ).width ()
    if factor < 0.07 or factor > 100: return
    self.scale ( scaleFactor, scaleFactor )
  #
  # mousePressEvent
  #
  def mousePressEvent ( self, event ):
    #print ">> WorkArea: mousePressEvent"
    if ( event.button () == QtCore.Qt.MidButton or
      ( event.button () == QtCore.Qt.LeftButton and event.modifiers () == QtCore.Qt.ShiftModifier ) ) :
      if self.state == 'idle':
        self.panStartPos = self.mapToScene ( event.pos () )
        self.state = 'pan'
        return
    if ( event.button () == QtCore.Qt.RightButton and event.modifiers () == QtCore.Qt.ShiftModifier ) :
      if self.state == 'idle':
        self.state = 'zoom'
        self.panStartPos = self.mapToScene ( event.pos () )
      return
    QtGui.QGraphicsView.mousePressEvent ( self, event )
  #
  # mouseDoubleClickEvent
  #
  def mouseDoubleClickEvent ( self, event ):
    #print ">> WorkArea: mouseDoubleClickEvent"
    selected = self.scene ().selectedItems ()

    for item in selected:
      if isinstance ( item, GfxNode ):
        print '>> Edit node %s' % item.node.label
        self.emit ( QtCore.SIGNAL ( "editGfxNode" ), item )

    QtGui.QGraphicsView.mouseDoubleClickEvent ( self, event )
  #
  # mouseMoveEvent
  #
  def mouseMoveEvent ( self, event ):
    #print ">> WorkArea: mouseMoveEvent"
    if self.state == 'pan' :
      panCurrentPos = self.mapToScene( event.pos() )
      panDeltaPos = panCurrentPos - self.panStartPos
      # update view matrix
      self.setInteractive ( False )
      self.translate ( panDeltaPos.x(), panDeltaPos.y() )
      self.setInteractive ( True )
    elif self.state == 'zoom' :
      panCurrentPos = self.mapToScene( event.pos() )
      panDeltaPos = panCurrentPos - self.panStartPos

      scale = -1.0
      if 'linux' in sys.platform: scale = 1.0
      import math
      scaleFactor = math.pow( 2.0, scale * max( panDeltaPos.x(), panDeltaPos.y() ) / 200.0  ) #
      factor = self.matrix().scale( scaleFactor, scaleFactor ).mapRect( QtCore.QRectF( -1, -1, 2, 2 ) ).width()

      if factor < 0.07 or factor > 100: return
      # update view matrix
      self.setInteractive ( False )
      self.scale ( scaleFactor, scaleFactor )
      self.translate ( -panDeltaPos.x() * scaleFactor, -panDeltaPos.y() * scaleFactor )
      self.setInteractive ( True )
    else :
      QtGui.QGraphicsView.mouseMoveEvent ( self, event )
  #
  # mouseReleaseEvent
  #
  def mouseReleaseEvent ( self, event ):
    #print ">> WorkArea: mouseReleaseEvent"
    if self.state == 'pan' or self.state == 'zoom':
      self.state = 'idle'
      self.panStartPos = None
    QtGui.QGraphicsView.mouseReleaseEvent ( self, event )
  #
  # resetZoom
  #
  def resetZoom ( self ) :
    if DEBUG_MODE : print ">> WorkArea: resetZoom"
    self.setInteractive ( False )
    self.resetTransform()
    self.setInteractive ( True )
  #
  # viewportEvent
  #
  def viewportEvent ( self, event ):
    #case QEvent::TouchBegin:
    # case QEvent::TouchUpdate:
    # case QEvent::TouchEnd:
    if event.type() == QtCore.QEvent.TouchBegin :
      if DEBUG_MODE : print ">> WorkArea: QEvent.TouchBegin"
    return QtGui.QGraphicsView.viewportEvent ( self, event )
  #
  # deselectAllNodes
  #
  def deselectAllNodes ( self ) :
    selected = self.scene().selectedItems()
    for item in selected : item.setSelected ( False )
  #
  # openNodeNet
  #
  def openNodeNet ( self, filename, pos = None ) :
    #
    ( nodes, links ) = self.nodeNet.open ( normPath ( filename ) )
    for node in nodes : self.addGfxNode ( node )
    for link in links : self.addGfxLink ( link )
  #
  # insertNodeNet
  #
  def insertNodeNet ( self, filename, pos = None ) :
    #
    if DEBUG_MODE : print "::insertNodeNet (before insert) nodes = %d links = %d" % ( len(self.nodeNet.nodes.values()), len(self.nodeNet.links.values()) )

    ( nodes, links ) = self.nodeNet.insert ( normPath ( filename ) )

    if pos == None :
      # on dblclk -- insert node at left border of sceneBound
      sceneBound = self.scene().itemsBoundingRect ()
      if not sceneBound.isNull () :
        x_offset = sceneBound.x() - self.minGap
        pos = QtCore.QPointF ( x_offset, 0 )

    self.deselectAllNodes ()

    for node in nodes : self.addGfxNode ( node, pos )
    for link in links : self.addGfxLink ( link )

    if DEBUG_MODE : print '::insertNodeNet (after insert) nodes = %d links = %d' % ( len ( self.nodeNet.nodes.values ()), len ( self.nodeNet.links.values () ) )
