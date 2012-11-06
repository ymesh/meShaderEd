#===============================================================================
# gfxNode.py
#
# 
#
#===============================================================================
import os, sys
from PyQt4 import QtCore, QtGui 

from gfx.gfxNodeConnector import GfxNodeConnector
from gfx.gfxLink import GfxLink

from global_vars import DEBUG_MODE
#
# GfxNode
# 	 
class GfxNode ( QtGui.QGraphicsItem ):
  Type = QtGui.QGraphicsItem.UserType + 1
  #
  #  
  def __init__ ( self, node ):
    QtGui.QGraphicsItem.__init__ ( self )  
    
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
    self.radius = 10
    self.swatchSize = 48
    self.hasSwatch = False
    
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
                                                                 
    self.PenNodeShaderParam = QtGui.QPen( QtGui.QColor( 250, 250, 250 ) )
                                   
    self.BrushNodeNormal = QtGui.QBrush ( QtGui.QColor( 128, 128, 128 ) )  
    self.BrushNodeSelected = QtGui.QBrush ( QtGui.QColor( 140, 140, 140 ) )

    
    self.paramsBrushes = {   'c' : QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)) 
                            ,'f' : QtGui.QBrush(QtGui.QColor(QtCore.Qt.lightGray))
                            ,'m' : QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkYellow)) 
                            ,'p' : QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkCyan)) 
                            ,'s' : QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkGreen)) 
                            ,'v' : QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkMagenta))
                            ,'n' : QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkBlue)) 
                            ,'R' : QtGui.QBrush(QtGui.QColor('orange')) 
                         }
                               
        
    # flag (new from QT 4.6...)
    self.setFlag ( QtGui.QGraphicsItem.ItemSendsScenePositionChanges ) 
    self.setFlag ( QtGui.QGraphicsItem.ItemSendsGeometryChanges )
    #self.setFlag ( QtGui.QGraphicsItem.ItemIsFocusable )
    
    # qt graphics stuff
    self.setFlag ( QtGui.QGraphicsItem.ItemIsMovable )
    self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
    self.setZValue ( 1 )   
    
    #self.gfxNodeBuilder = GfxNodeBuilder(self.node)
    #self.isNodeSelected = False
    
    self.setupHeader()
    self.setupParams( self.node.outputParams, self.outputParamLabels, self.outputConnectors )
    self.setupParams( self.node.inputParams, self.inputParamLabels, self.inputConnectors )
    
    ( x, y ) = self.node.offset
    self.setPos ( x, y )
    self.setupGeometry ()
    
    #for param in self.node.inputParams :
    #  self.node.connect( param, QtCore.SIGNAL( 'paramChanged(QObject)' ), self.node.onParamChanged )
  #
  #    
  def type ( self ):
    return GfxNode.Type
  #
  #  
  def getInputConnectorByParam ( self, param ) :
    connector = None
    for cnt in self.inputConnectors :
      if cnt.param == param :
        connector = cnt
        break       
    return connector
  #
  #  
  def getOutputConnectorByParam ( self, param ) :
    connector = None
    for cnt in self.outputConnectors :
      if cnt.param == param :
        connector = cnt
        break       
    return connector
  #
  #
  def remove ( self ) :
    if DEBUG_MODE : print ">> GfxNode remove gfxNode (temp)"
    for connect in self.inputConnectors :
      connect.removeAllLinks ()

    for connect in self.outputConnectors :
      connect.removeAllLinks ()
    
    self.scene().emit ( QtCore.SIGNAL( "onGfxNodeRemoved" ), self )  
  
  #
  #  
  def updateNodeLabel ( self ) :
    self.header['label'].label = self.node.label
    self.setupGeometry () 
    self.update ()  
    self.adjustLinks ()
  #
  #  
  def updateInputParams ( self ):
    i = 0
    for param in self.node.inputParams : # for i in range( len( self.node.inputParams )) :
      if param.provider != 'attribute' :
        label = self.inputParamLabels[ i ]
        label.brush = self.BrushNodeNormal
        label.PenNormal = self.PenBorderNormal
        if param.shaderParam :
          if not self.node.isInputParamLinked ( param ) :
            label.PenNormal = self.PenNodeShaderParam
        label.update()
        i += 1
  #
  #
  def setupGeometry ( self ): 
    ( wi_header, hi_header ) = self.getHeaderSize()
    ( wi_output, hi_output ) = self.getParamsSize( self.outputParamLabels )
    ( wi_input, hi_input ) = self.getParamsSize( self.inputParamLabels )

    wi_max = max( wi_header, wi_output, wi_input ) + 2 * self.x_offset 
    hi_max = hi_header + hi_output + hi_input + 3 * self.y_offset

    self.rect = QtCore.QRectF ( 0, 0, wi_max, hi_max )  ## self.gfxNodeBuilder.rect.united(self.gfxNodeBuilder.shadowRect)
    self.setupHeaderGeometry( self.x_offset, self.y_offset ) 
    self.setupOutputParamsGeometry( wi_max - self.x_offset, hi_header + 2 * self.y_offset )
    self.setupInputParamsGeometry( self.x_offset, hi_header + 2 * self.y_offset + hi_output )  
  #
  #
  def boundingRect ( self ): 
    #print ( "GfxNode.boundingRect" )        
    bound_rect = QtCore.QRectF ( self.rect )
    bound_rect.adjust( -6, 0, 6, 0 ) 
    return bound_rect
  #
  #
  def shape ( self ):
    shape = QtGui.QPainterPath ()               
    shape.addRect ( self.boundingRect() )
    #shape += self.header['input'].shape() 
    #shape += self.header['output'].shape()
    return shape  
  #
  # 
  def setupHeader ( self ) :
    if self.node.type != 'variable' :    
      self.header['name'] = GfxNodeLabel( self.node.name ) 
      
      self.header['name'].brush = self.BrushNodeNormal
      self.header['name'].pen = self.PenBorderNormal
      #self.header['name'].font = self.headerFont
      self.header['name'].font.setItalic( True )
      
      self.header['label'] = GfxNodeLabel( self.node.label ) 
        
      self.header['label'].brush = self.BrushNodeNormal
      self.header['label'].pen = self.PenBorderNormal
      #self.header['label'].font = self.headerFont
      self.header['label'].font.setBold( True )
      
      if self.hasSwatch :      
        self.header['swatch'] = GfxNodeSwatch ( self.swatchSize ) 
      
      #self.header['input'] = GfxNodeConnector( 6 ) 
      #self.header['output'] = GfxNodeConnector( 6 ) 
  #
  #
  def getHeaderSize ( self ) :
    wi = 80 # minimal node width
    hi = 0
    if self.node.type != 'variable' : 
      (wi_label, hi_label) = self.header['label'].getLabelSize()
      (wi_name, hi_name) = self.header['name'].getLabelSize()
      hi = ( hi_label + hi_name )        
      wi = max ( wi, (self.x_offset + max ( wi_label, wi_name ) ) )
      if self.hasSwatch :      
        hi = max ( self.swatchSize, hi )
        wi += self.swatchSize
    return ( wi, hi )
  #
  #
  def setupHeaderGeometry ( self, x, y ) :
    if self.node.type != 'variable' : 
      wi_header = self.rect.width()
      if self.hasSwatch :
        self.header['swatch'].rect.moveTo( x, y )
        #self.header['input'].rect.moveTo( x - self.x_offset - self.header['input'].radius,
        #                                  y + self.swatchSize / 2 - self.header['input'].radius )
        #self.header['output'].rect.moveTo( wi_header - self.header['output'].radius,
        #                                  y + self.swatchSize / 2 - self.header['output'].radius )
        x += self.header['swatch'].rect.width () + self.x_offset

      (wi, hi) = self.header['label'].getLabelSize()
      self.header['label'].rect = QtCore.QRectF ( x, y, wi, hi ) 
      y += hi
      (wi, hi) = self.header['name'].getLabelSize()
      self.header['name'].rect = QtCore.QRectF ( x, y, wi, hi )  
      
      # parent controls from header
      for ctrl in self.header.keys() : 
        self.header[ ctrl ].setParentItem( self )        
  #
  #
  def setupOutputParamsGeometry ( self, xs, ys ) : 
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
  #
  def setupInputParamsGeometry ( self, xs, ys ) : 
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
  #
  def getParamsSize ( self, paramLabels ) :
    wi = 0
    hi = 0
    for label in paramLabels :
      ( wi_label, hi_label ) = label.getLabelSize()
      hi += hi_label
      wi = max ( wi, wi_label )
    return ( wi, hi )          
  #
  #
  def setupParams ( self, params, labels, connectors ):
    for param in params :
      # ignore attributes
      if param.provider != 'attribute' :
        
        label = GfxNodeLabel ( param.label )
        label.brush = self.BrushNodeNormal
        label.PenNormal = self.PenBorderNormal
        
        if not param.isInput :
          label.font.setBold( True )
        
        if param.shaderParam :
          #label.font.setBold( True ) 
          label.PenNormal = self.PenNodeShaderParam
        
        labels.append( label )
        
        connector = GfxNodeConnector ( param, 5 )
        
        if not param.isInput:
          connector.singleLinkOnly = False 
        if param.encodedTypeStr() in self.paramsBrushes.keys() :
          connector.brush = self.paramsBrushes[ param.encodedTypeStr() ]
        
        connectors.append ( connector )
  #
  #    
  def adjustLinks ( self ) :
    # invalidate all the links attached
    for connect in self.inputConnectors :
      connect.adjustLinks ()

    for connect in self.outputConnectors :
      connect.adjustLinks ()  
  #
  #    
  def itemChange ( self, change, value ):
    if change == QtGui.QGraphicsItem.ItemSelectedHasChanged : #ItemSelectedChange:
      #self.isNodeSelected = not self.isNodeSelected
      if self.node.type != 'variable' :       
        # variable node has not header 
        self.header['label'].isNodeSelected = value.toBool()
        #self.header['swatch'].isNodeSelected = self.isNodeSelected
      
      if value.toBool() :
        items = self.scene().items()
        for i in range( len ( items ) - 1, -1, -1 ) :
          if items[ i ].parentItem() is None :
            if items[ i ] != self : 
              items[ i ].stackBefore ( self )
        #scene.setFocusItem ( self )
    elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
      # print '>> GfxNode.itemChange = ItemPositionHasChanged (%f, %f)' % ( self.x(), self.y() )
      self.node.offset = ( self.x(), self.y() )
      self.adjustLinks ()  
    
    return QtGui.QGraphicsItem.itemChange ( self, change, value )
  #
  #        
  def paint ( self, painter, option, widget ):        
    # print ( ">> GfxNode.paint" ) 
    self.paintFrame ( painter ) 
  #
  #  
  def paintFrame ( self, painter ):
    #print ( ">> GfxNode.paintWindowFrame" ) 
    painter.setRenderHint ( QtGui.QPainter.Antialiasing )
    painter.setRenderHint ( QtGui.QPainter.SmoothPixmapTransform )
    
    pen = self.PenBorderNormal
    brush = self.BrushNodeNormal
    if self.isSelected() :
      pen =  self.PenBorderSelected
      # brush = self.BrushNodeSelected 
    
    painter.setPen ( pen )
    painter.setBrush ( brush )
        
    # painter.drawRect ( self.rect )
    painter.drawRoundedRect ( self.rect, self.radius, self.radius, QtCore.Qt.AbsoluteSize ) # Qt::SizeMode mode = Qt::AbsoluteSize Qt.RelativeSize
#
# GfxNodeLabel
#      
class GfxNodeLabel ( QtGui.QGraphicsItem ):
  Type = QtGui.QGraphicsItem.UserType + 3
  #
  #
  def __init__ ( self, label ):
    QtGui.QGraphicsItem.__init__ ( self )  
    
    self.label = label
    
    self.PenNormal = QtGui.QPen ( QtGui.QColor ( 0, 0, 0 ) )
    self.PenSelected = QtGui.QPen ( QtGui.QColor ( 240, 240, 240 ) ) 
    
    self.font = QtGui.QFont ()  
    self.brush = QtGui.QBrush ( QtGui.QColor ( 140, 140, 140 ) ) # ( 128, 128, 128 ) ( 132, 132, 132 )
    
    
    self.isNodeSelected = False
    self.rect = QtCore.QRectF () 
  #
  #    
  def type ( self ): return GfxNodeLabel.Type
  #
  #
  def boundingRect ( self ): return self.rect
  #
  #
  def getLabelSize ( self ):
    
    labelFontMetric = QtGui.QFontMetricsF( self.font )
    height = labelFontMetric.height() + 1
    width = labelFontMetric.width( self.label ) + 1
    return ( width, height )
  #
  #    
  def paint ( self, painter, option, widget ):        
    # print ( ">> GfxNode.paint" ) 

    painter.fillRect ( self.rect, self.brush )
    
    painter.setFont ( self.font )
    pen = self.PenNormal
    
    if self.isNodeSelected : pen = self.PenSelected
      
    painter.setPen ( pen )
    painter.drawText ( self.rect, QtCore.Qt.AlignLeft, self.label )
#
# GfxNodeSwatch
#      
class GfxNodeSwatch ( QtGui.QGraphicsItem ):
  Type = QtGui.QGraphicsItem.UserType + 4
  #
  #
  def __init__ ( self, swatchSize ):
    QtGui.QGraphicsItem.__init__ ( self ) 
 
    self.brush = QtGui.QBrush ( QtGui.QColor ( 140, 140, 140 ) ) # ( 128, 128, 128 ) ( 132, 132, 132 )
    self.PenBorderNormal = QtGui.QPen ( QtGui.QColor ( 0, 0, 0 ) )
    self.PenBorderSelected = QtGui.QPen ( QtGui.QColor ( 240, 240, 240 ) )    
    
    #self.isNodeSelected = False
    self.radius = 5
    self.swatchSize = swatchSize
    self.rect = QtCore.QRectF ( 0, 0, swatchSize, swatchSize ) 
  #
  #    
  def type ( self ): return GfxNodeSwatch.Type
  #
  #
  def boundingRect ( self ): return self.rect   
  #
  #
  def shape ( self ):
    shape = QtGui.QPainterPath ()               
    shape.addRect ( self.rect )
    return shape   
  #
  #    
  def paint ( self, painter, option, widget ):        
    # print ( ">> GfxNodeSwatch.paint" ) 
    painter.setRenderHint ( QtGui.QPainter.Antialiasing )
    painter.setRenderHint ( QtGui.QPainter.SmoothPixmapTransform )
    
    pen = self.PenBorderNormal
    if self.parentItem().isSelected():
      pen =  self.PenBorderSelected
      # brush = self.BrushNodeSelected 
    
    painter.setPen ( pen )
    painter.setBrush ( self.brush )
    painter.drawRoundedRect ( self.rect, self.radius, self.radius, QtCore.Qt.AbsoluteSize )
