#===============================================================================
# gfxNodeConnector.py
#
# 
#
#===============================================================================
import os, sys, copy
from PyQt4 import QtCore, QtGui 
#
# GfxNodeConnector
#      
class GfxNodeConnector ( QtGui.QGraphicsItem ):
  Type = QtGui.QGraphicsItem.UserType + 5
  isRound = True
  #
  #  
  def __init__ ( self, param = None, radius=2, isRound=True ):
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
    
    #self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
  #
  #    
  def type ( self ): return GfxNodeConnector.Type
  #
  #
  def boundingRect ( self ): return self.rect  
  #
  #
  def getCenterPoint ( self ): return self.mapToScene( self.rect.center() ) 
  #
  #
  def addLink ( self, link ): self.links.append ( link )
  #
  #
  def getFirstLink ( self ): 
    return self.links[0] ##copy.copy( self.links[0] )   
  #
  #
  def removeLink ( self, link ): 
    print ">> GfxNodeConnector removeLink" 
    if link in self.links :
      self.links.remove ( link )
  #
  #
  def removeAllLinks ( self ): 
    print ">> GfxNodeConnector removeAllLinks (%d)" % len ( self.links )   
    for link in list( self.links ) :
      link.remove () # link will be removed from list 
      #self.links.remove ( link )      
      #self.scene().removeItem ( link )        
          
  #
  #
  def isInput ( self ): return self.param.isInput  
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
    for link in self.links :
      link.adjust ()
  #
  #
  def itemChange ( self, change, value ) :
    if change == QtGui.QGraphicsItem.ItemSelectedHasChanged :
      print ">> value = %s" % value.toBool() 
      self.isNodeSelected = value.toBool()
      if self.isNodeSelected :
        node = self.parentItem().node
        print ">> selected conector for node %s (id = %d)" % ( node.label, node.id )
    elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
      pass
      #print ">> ItemPositionHasChanged conector for node %s (param = %d)" % ( node.label, self.param.label )

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
    self.parentItem().scene().emit ( QtCore.SIGNAL( "startNodeLink" ), self )  
    self.grabMouse()
    #if not self.parentItem().isSelected() :
    #  self.parentItem().setSelected( True )  
    event.accept()
  #
  #
  def mouseMoveEvent ( self, event ) :
    #print ">> mouseMoveEvent at %d %d" % ( event.scenePos().x(), event.scenePos().y() )
    self.parentItem().scene().emit ( QtCore.SIGNAL( "traceNodeLink" ), self, event.scenePos() )  
    event.accept()
  #
  #
  def mouseReleaseEvent ( self, event ) :
    #print ">> mouseReleaseEvent" 
    self.parentItem().scene().emit ( QtCore.SIGNAL( "endNodeLink" ), self, event.scenePos() ) 
    self.ungrabMouse()
    self.hilite( False )
    event.accept()
