#===============================================================================
#
# gfxNodeLabel.py
#
#
#
#===============================================================================
from PyQt4 import QtCore, QtGui

from global_vars import DEBUG_MODE, GFX_NODE_LABEL_TYPE
from meShaderEd import app_settings

#
# GfxNodeLabel
#
class GfxNodeLabel ( QtGui.QGraphicsItem ) :
  #
  Type = GFX_NODE_LABEL_TYPE
  #
  # __init__
  #
  def __init__ ( self, label, fill_BG = True ) :
    #
    QtGui.QGraphicsItem.__init__ ( self )

    self.label = label

    self.textColor = QtGui.QColor ( 0, 0, 0 )
    self.selectedColor = QtGui.QColor ( 240, 240, 240 )
    
    self.PenNormal = QtGui.QPen ( self.textColor )
    self.PenSelected = QtGui.QPen ( self.selectedColor )

    self.font = QtGui.QFont ()
    self.brush = QtGui.QBrush ( QtGui.QColor ( 140, 140, 140 ) )
    
    self.justify = QtCore.Qt.AlignLeft
    
    self.fill_BG = fill_BG
    self.isNodeSelected = False
    self.rect = QtCore.QRectF ()
  #
  # type
  #
  def type ( self ) : return GfxNodeLabel.Type
  #
  # boundingRect
  #
  def boundingRect ( self ) : return self.rect
  #
  # setTextColor
  #
  def setTextColor ( self, color ) : 
    self.textColor = color
    self.PenNormal = QtGui.QPen ( self.textColor ) 
  #
  # getLabelSize
  #
  def getLabelSize ( self ) :
    #
    labelFontMetric = QtGui.QFontMetricsF ( self.font )
    lines = self.label.split ( '\n' )
    height = 0
    width = 0
    for line in lines :
      height += labelFontMetric.height () + 1
      width = max ( width, labelFontMetric.width ( line ) ) + 1
    return ( width, height )
  #
  # paint
  #
  def paint ( self, painter, option, widget ) :
    #
    painter.setFont ( self.font )
    pen = self.PenNormal
    if self.isNodeSelected : pen = self.PenSelected
    if self.fill_BG : painter.fillRect ( self.rect, self.brush )
    painter.setPen ( pen )
    painter.drawText ( self.rect, self.justify, self.label )