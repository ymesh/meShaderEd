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

from gfx.gfxNode import GfxNode
from gfx.gfxNodeConnector import GfxNodeConnector
from gfx.gfxLink import GfxLink

from meShaderEd import app_settings
from global_vars import DEBUG_MODE

#from ui_workArea import Ui_workArea
#
#
# 
class WorkArea ( QtGui.QGraphicsView ):
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
    
    QtCore.QObject.connect( self.scene(), QtCore.SIGNAL( "selectionChanged()" ), self.onSelectionChanged )
    QtCore.QObject.connect( self.scene(), QtCore.SIGNAL( "startNodeLink" ), self.onStartNodeLink )
    QtCore.QObject.connect( self.scene(), QtCore.SIGNAL( "traceNodeLink" ), self.onTraceNodeLink )
    QtCore.QObject.connect( self.scene(), QtCore.SIGNAL( "endNodeLink" ), self.onEndNodeLink )

    QtCore.QObject.connect( self.scene(), QtCore.SIGNAL( "onGfxNodeRemoved" ), self.onRemoveNode )
    QtCore.QObject.connect( self.scene(), QtCore.SIGNAL( "onGfxLinkRemoved" ), self.onRemoveLink )
    
    if DEBUG_MODE : print ">> WorkArea: __init__"
  #    
  #
  #
  def drawBackground ( self, painter, rect ):
    sc_rect = self.sceneRect()
    bbrush = QtGui.QBrush( QtGui.QColor( 148, 148, 148 ) ) ## painter.background()
    painter.fillRect( rect, bbrush )
    
    if self.drawGrid :
    #  print( "grid size = %d" % self.gridSize )
      gr_pen = QtGui.QPen( QtGui.QColor( 180, 180, 180 ) ) 
      gr_pen.setWidth( 0 )
      painter.setPen( gr_pen )
      for x in range( int( sc_rect.x() ), int( sc_rect.right() ), self.gridSize ):
        painter.drawLine( x, sc_rect.y(), x, sc_rect.bottom() ) 
      for y in range( int( sc_rect.y() ), int( sc_rect.bottom() ), self.gridSize ):
        painter.drawLine( sc_rect.x(), y, sc_rect.right(), y )
    #else:
    #  print( "no grid" )
    #print( "rect: x = %d y = %d wi = %d hi = %d" % (rect.x(), rect.y(), rect.width(), rect.height() ) )
    #print( "rect: x = %d y = %d wi = %d hi = %d" % (sc_rect.x(), sc_rect.y(), sc_rect.width(), sc_rect.height() ) )
    
    #self.viewBrush = QtGui.QBrush( QtGui.QColor( 148, 148, 148 ) )  
    #self.setBackgroundBrush( self.viewBrush )
    
  #
  # Returns a list of GfxNodes in the scene for given type 
  #
  def getGfxNodesByType ( self, type  ) :
    resultList = []
    for item in self.scene().items() :
      if isinstance ( item, GfxNode ):  
        if item.node.type == type :
          resultList.append ( item )  
    return resultList
  #
  #    
  def setNodeNetwork ( self, nodeNet ):
    self.nodeNet = nodeNet
  #
  #    
  def clear ( self ):
    if DEBUG_MODE : print ">> WorkArea: clearing nodes ..."
    
    for item in self.scene().items() :
      self.scene().removeItem ( item )
      
    self.nodeNet.clear ()
    
    self.state = 'idle'
    self.panStartPos = None
    
    self.lastConnectCandidate = None
    self.currentGfxLink = None
    
    self.inspectedNode = None
  #
  #
  #
  def addGfxLink ( self, link ) :
    #
    #print '>> WorkArea: addGfxLink'
    gfxLink = GfxLink( link )
    
    srcNode = link.srcNode
    dstNode = link.dstNode
    
    srcParam = link.srcParam
    dstParam = link.dstParam
    
    srcConnector = None
    dstConnector = None
    
    for item in self.scene().items():
      if isinstance ( item, GfxNode ):
        if item.node == srcNode :
          srcConnector = item.getOutputConnectorByParam ( srcParam ) 
        elif item.node == dstNode :  
          dstConnector = item.getInputConnectorByParam ( dstParam ) 
      if ( srcConnector != None and dstConnector != None ) :
        break 
    
    gfxLink.setSrcConnector ( srcConnector )
    gfxLink.setDstConnector ( dstConnector )
    
    gfxLink.adjust ()
    
    self.scene().addItem ( gfxLink )
  #
  # Node already in NodeNet, so add new GfxNode to scene 
  #   
  def addGfxNode ( self, node, pos = None ):
    #
    #print ( ">> WorkArea: addGfxNode %s" % node.label ) 
    gfxNode = GfxNode ( node )
    scene = self.scene ()
    
    if pos != None : gfxNode.moveBy ( pos.x(), pos.y() )
    
    #for item in scene.selectedItems (): item.setSelected ( False )
      
    scene.addItem ( gfxNode )
    gfxNode.setSelected ( True )
    
    self.emit ( QtCore.SIGNAL( "gfxNodeAdded" ), gfxNode ) 
  #
  #
  #
  def adjustLinks ( self ) :
    for item in self.scene().items() :
      if isinstance ( item, GfxLink ): item.adjust ()   
  #    
  #
  #
  def onSelectionChanged ( self ) :
    #
    #print ">> WorkArea: onSelectionChanged " 
    selectedNodes = [] 
    selectedLinks = []
    selected = self.scene().selectedItems()
    
    for item in selected:
      if isinstance ( item, GfxNode ): selectedNodes.append ( item ) 
      if isinstance ( item, GfxLink ): selectedLinks.append ( item ) 
    
    self.emit( QtCore.SIGNAL( "selectNodes" ), selectedNodes, selectedLinks ) 
  #
  #
  def lastConnectCandidateReset ( self ) :
    #
    if self.lastConnectCandidate is not None :
      self.lastConnectCandidate.hilite( False )  
    self.lastConnectCandidate = None
  #
  #
  def isLinkAcceptable ( self, connector, connectCandidate ) :
    #
    isAcceptable = False
    if isinstance ( connectCandidate, GfxNodeConnector ):     
      # do not connect to itself   
      if connectCandidate != connector :
        # do not connect to the same node            
        if connectCandidate.parentItem() != connector.parentItem() :  
          # do not connect the same link to connector twice      
          if not connectCandidate.hasThisLink ( self.currentGfxLink ) :
            # connectors must have a valid parameter ???          
            # if connector.param is not None and connectCandidate.param is not None :
            # connect only input with output and vice versa
            if connector.param.isInput != connectCandidate.param.isInput :
              # connect only to similar type              
              if connector.param.encodedTypeStr() == connectCandidate.param.encodedTypeStr() :
                isAcceptable = True
    return isAcceptable
  #
  #
  def onStartNodeLink ( self, connector ):
    #
    srcNode = connector.parentItem().node
    srcParam = connector.param
    if DEBUG_MODE : print ">> WorkArea: onCreateNodeLink from %s (%s)" % ( srcNode.label, srcParam.label )  
    
    srcConnector = connector  
    self.state = 'traceNodeLink'
    self.lastConnectCandidate = None    
    
    if connector.isInput() and connector.isLinked() :
      oldLink = connector.getFirstLink() 
      srcConnector = oldLink.srcConnector
      oldLink.remove()   

    gfxLink = GfxLink( None, srcConnector )
    self.scene().addItem ( gfxLink )
    self.currentGfxLink = gfxLink
    self.currentGfxLink.isLinkSelected = True

  #
  #
  def onTraceNodeLink ( self, connector, scenePos ) :
    # node = connector.parentItem().node
    # print ">> WorkArea: onDrawNodeLink from %s (%d %d)" % ( node.label, scenePos.x(), scenePos.y() ) 

    connectCandidate = self.scene().itemAt( scenePos )
    srcConnector = self.currentGfxLink.srcConnector

    if self.isLinkAcceptable ( srcConnector, connectCandidate ) :
      if connectCandidate != self.lastConnectCandidate :
        self.lastConnectCandidateReset()
        connectCandidate.hilite( True )
        self.lastConnectCandidate = connectCandidate
        # link_node = connectCandidate.parentItem().node
        # print ">> WorkArea: onDrawNodeLink to %s" % link_node.label 
      else :
        scenePos = self.lastConnectCandidate.getCenterPoint() # snap to last position
        pass
        # self.lastConnectCandidateReset()
    else :
      self.lastConnectCandidateReset () 
    
    #if self.currentGfxLink is not None :
    self.currentGfxLink.setDstPoint ( scenePos )  
  #
  #
  def onEndNodeLink ( self, connector, scenePos ):
    srcConnector = self.currentGfxLink.srcConnector
    dstConnector = self.currentGfxLink.dstConnector
    
    if self.lastConnectCandidate is None :
      self.currentGfxLink.remove()
      #self.emit( QtCore.SIGNAL( 'nodeParamChanged' ), srcConnector.parentItem(), srcConnector.param )
      #self.emit( QtCore.SIGNAL( 'nodeParamChanged' ), dstConnector.parentItem(), dstConnector.param ) 
    else :
      # remove old link first if it exists      
      if self.lastConnectCandidate.isInput() and self.lastConnectCandidate.isLinked() :
        oldLink = self.lastConnectCandidate.getFirstLink() 
        oldLink.remove()  

      self.currentGfxLink.isLinkSelected = False
      self.currentGfxLink.update()
      
      srcNode = srcConnector.parentItem().node
      srcParam = srcConnector.param

      dstNode = self.lastConnectCandidate.parentItem().node
      dstParam = self.lastConnectCandidate.param
      
      self.currentGfxLink.setDstConnector ( self.lastConnectCandidate )
      link = NodeLink.build ( srcNode, dstNode, srcParam, dstParam )

      if dstParam.isInput is not True :
        # swap source and destination
        self.currentGfxLink.swapConnectors()
        link.swapNodes()

      self.currentGfxLink.link = link
      self.nodeNet.addLink ( link ) 
      #self.emit( QtCore.SIGNAL( 'nodeConnectionChanged' ), self.currentGfxLink.srcConnector.parentItem(), self.currentGfxLink.srcConnector.param )
      self.emit( QtCore.SIGNAL( 'nodeConnectionChanged' ), self.currentGfxLink.dstConnector.parentItem(), self.currentGfxLink.dstConnector.param ) 
    
    self.lastConnectCandidateReset ()
    self.currentGfxLink = None
    self.state = 'idle'
  #
  #
  #    
  def onRemoveNode ( self, gfxNode ):
    #print ">> WorkArea: onRemoveNode"
    self.emit ( QtCore.SIGNAL( "gfxNodeRemoved" ), gfxNode ) 
    self.scene().removeItem ( gfxNode )
    self.nodeNet.removeNode ( gfxNode.node )
  #
  #    
  def onRemoveLink ( self, gfxLink ):
    #print ">> WorkArea: onRemoveLink"
    self.scene().removeItem ( gfxLink )
    if gfxLink.link is not None : 
      srcConnector = gfxLink.srcConnector
      dstConnector = gfxLink.dstConnector  
      self.nodeNet.removeLink ( gfxLink.link )
      if srcConnector is not None :  
        print "srcConnector.parentItem().node.label = %s " % srcConnector.parentItem().node.label
        #self.emit( QtCore.SIGNAL( 'nodeConnectionChanged' ), srcConnector.parentItem(), srcConnector.param )
      if dstConnector is not None :
        print "dstConnector.parentItem().node.label = %s " % dstConnector.parentItem().node.label
        self.emit( QtCore.SIGNAL( 'nodeConnectionChanged' ), dstConnector.parentItem(), dstConnector.param ) 
  #
  #
  def removeSelected ( self ):
    if DEBUG_MODE : print ":: (before) nodes = %d links = %d" % ( len(self.nodeNet.nodes.values()), len(self.nodeNet.links.values()) )    
    selected = self.scene().selectedItems() 

    for item in selected:
      if isinstance ( item, GfxLink ): item.remove()
      if isinstance ( item, GfxNode ): item.remove()  

    print ":: (after) nodes = %d links = %d" % ( len( self.nodeNet.nodes.values()), len( self.nodeNet.links.values()) )        
  #
  #
  def dragEnterEvent(self, event):
    print ">> WorkArea: onDragEnterEvent"
    #for form_str in event.mimeData().formats():
    #  print str ( form_str )
    #  if form_str == 'text/uri-list' :
    #    print event.mimeData().data( 'text/uri-list' )  
    mimedata = event.mimeData()
    
    if mimedata.hasFormat( 'application/x-text' ) or mimedata.hasFormat( 'text/uri-list' ):
      event.accept()
    else:
      event.ignore()
  #
  #
  def dragMoveEvent ( self, event ):
    #print ">> WorkArea: onDragMoveEvent"
    mimedata = event.mimeData()
    if mimedata.hasFormat( 'application/x-text' ) or mimedata.hasFormat( 'text/uri-list' ):
      event.setDropAction ( QtCore.Qt.CopyAction )
      event.accept()
    else:
      event.ignore()
  #
  #        
  def dropEvent ( self, event ):
    if DEBUG_MODE : print ">> WorkArea: onDropEvent"
    file_list = []
    mimedata = event.mimeData()
    
    if mimedata.hasFormat ( 'application/x-text' ) :
      # decode drop stuff
      data = mimedata.data ( 'application/x-text' )       
      stream = QtCore.QDataStream ( data, QtCore.QIODevice.ReadOnly )
      filename = QtCore.QString()
      stream >> filename
      
      if DEBUG_MODE : print "itemFilename = %s" % ( filename )
      
      file_list.append ( filename )
      event.setDropAction ( QtCore.Qt.CopyAction )
      event.accept()
    elif mimedata.hasFormat ( 'text/uri-list' ) :  
      data = str ( mimedata.data( 'text/uri-list' ).data() )
      #print data
      for item in data.split() :
        filename = str ( QtCore.QUrl( item ).toLocalFile () )
        
        ( name, ext ) = os.path.splitext( os.path.basename( filename ) )
        if DEBUG_MODE : print ':: %s (%s)' % ( filename, ext )
        if ext == '.xml' :
          file_list.append ( filename )  
    else:
      event.ignore()    
    
    for file_name in file_list :
      self.insertNodeNet ( file_name, self.mapToScene( event.pos() ) )    
  #
  #
  def keyPressEvent ( self, event ) : 
    #print ">> WorkArea: keyPressEvent"
    QtGui.QGraphicsView.keyPressEvent ( self, event)
    #event.ignore()
    #event.accept()
  #
  #  
  def wheelEvent ( self, event ):
    #print ">> WorkArea: wheelEvent"
    # QtGui.QGraphicsView.wheelEvent( self, event)
    scale = -1.0
    if 'linux' in sys.platform: scale = 1.0     
    import math
    scaleFactor = math.pow( 2.0, scale * event.delta() / 600.0 )
    factor = self.matrix().scale( scaleFactor, scaleFactor ).mapRect( QtCore.QRectF( -1, -1, 2, 2 ) ).width()
    if factor < 0.07 or factor > 100: return
    self.scale ( scaleFactor, scaleFactor )      
  #
  #
  def mousePressEvent ( self, event ):
    #print ">> WorkArea: mousePressEvent"
    if ( event.button() == QtCore.Qt.MidButton or 
      ( event.button() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ShiftModifier ) ) :  
      if self.state == 'idle':
        self.panStartPos = self.mapToScene( event.pos() )
        self.state = 'pan'
        return
    if ( event.button() == QtCore.Qt.RightButton and event.modifiers() == QtCore.Qt.ShiftModifier ) :  
      if self.state == 'idle':
        self.state = 'zoom'
        self.panStartPos = self.mapToScene( event.pos() )
      return
    QtGui.QGraphicsView.mousePressEvent ( self, event )        
  #
  #
  def mouseDoubleClickEvent ( self, event ):
    #print ">> WorkArea: mouseDoubleClickEvent"
    selected = self.scene().selectedItems()
    
    for item in selected:
      if isinstance ( item, GfxNode ): 
        print '>> Edit node %s' % item.node.label 
        self.emit( QtCore.SIGNAL( "editGfxNode" ), item ) 
        
    QtGui.QGraphicsView.mouseDoubleClickEvent ( self, event )
  #
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
  #  
  def mouseReleaseEvent ( self, event ):        
    #print ">> WorkArea: mouseReleaseEvent"
    if self.state == 'pan' or self.state == 'zoom':
      self.state = 'idle'  
      self.panStartPos = None
    QtGui.QGraphicsView.mouseReleaseEvent ( self, event )   
    
  #
  #
  def resetZoom ( self ) :
    if DEBUG_MODE : print ">> WorkArea: resetZoom"
    self.setInteractive ( False )
    self.resetTransform() 
    self.setInteractive ( True )   
  #
  #
  def viewportEvent( self, event ):
    #case QEvent::TouchBegin:
    # case QEvent::TouchUpdate:
    # case QEvent::TouchEnd:
    if event.type() == QtCore.QEvent.TouchBegin :
      print ">> WorkArea: QEvent.TouchBegin"
    return QtGui.QGraphicsView.viewportEvent ( self, event )
  #
  #
  def deselectAllNodes ( self ) :
    selected = self.scene().selectedItems()
    
    for item in selected:
      item.setSelected ( False )
  #
  #
  #
  def openNodeNet ( self, filename, pos = None ) :
    #
    ( nodes, links ) = self.nodeNet.open ( normPath ( filename ) ) 
    for node in nodes : self.addGfxNode ( node )  
    for link in links : self.addGfxLink ( link ) 
  #
  #
  #
  def insertNodeNet ( self, filename, pos = None ) :
    #
    if DEBUG_MODE : print ":: (before insert) nodes = %d links = %d" % ( len(self.nodeNet.nodes.values()), len(self.nodeNet.links.values()) ) 
    
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
      
    if DEBUG_MODE : print ":: (after insert) nodes = %d links = %d" % ( len(self.nodeNet.nodes.values()), len(self.nodeNet.links.values()) )     
