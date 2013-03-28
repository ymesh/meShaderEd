#===============================================================================
# ColorWidget.py
#
# 
#
#===============================================================================

from PyQt4 import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget 

#
# FloatWidget
#
class ColorWidget ( ParamWidget ) :
  #
  #                 
  def buildGui ( self ) :
    self.ui = Ui_ColorWidget_field() 
    self.ui.setupUi ( self )
#
#
#
class ColorEditEventFilter ( QtCore.QObject ) :
  #
  # __init__
  #
  def __init__ ( self, ColorWidget ) :
    QtCore.QObject.__init__ ( self, None )
    self.ColorWidget = ColorWidget
    #print "eventFilter created..." 
  #
  # eventFilter
  #
  def eventFilter ( self, obj, event ) :
    # check for single click
    if event.type () == QtCore.QEvent.MouseButtonPress:
      #print "eventFilter = MouseButtonPress" 
      self.ColorWidget.emit ( QtCore.SIGNAL ( 'clicked()' ) )  
      return True
    else:
      return obj.eventFilter ( obj, event )    
#
# Ui_ColorWidget_field
#          
class Ui_ColorWidget_field ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, ColorWidget ) :
    #
    self.widget = ColorWidget
    self.colorEdit = QtGui.QLabel ( ColorWidget )
    
    self.colorEdit.setMinimumSize ( QtCore.QSize( UI.COLOR_WIDTH, UI.HEIGHT ) )
    self.colorEdit.setMaximumSize ( QtCore.QSize( UI.COLOR_WIDTH, UI.HEIGHT ) )

    self.colorEdit.setObjectName ( 'colorEdit' )
    
    self.selector = QtGui.QComboBox ( ColorWidget )
    self.selector.setEditable ( False )
    #self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
    
    for label in [ "rgb", "hsv", "hsl", "xyz", "XYZ", "YIQ" ] :
      self.selector.addItem ( label )
    if self.widget.param.space != None :
      self.selector.setCurrentIndex ( self.selector.findText ( self.widget.param.space ) )
      
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.colorEdit )
    self.widget.hl.addWidget ( self.selector )
    
    self.widget.hl.addItem ( spacer )
    
    QtCore.QMetaObject.connectSlotsByName ( ColorWidget )
    self.connectSignals ( ColorWidget )
    
    # install a custom filter in order to avoid subclassing
    self.colorEventFilter = ColorEditEventFilter ( ColorWidget )
    self.colorEdit.installEventFilter ( self.colorEventFilter )
    
  #
  # connectSignals
  #  
  def connectSignals ( self, ColorWidget ) :
    # register signal propertyChanged for updating the gui
    #self.connect( self.colorProperty, QtCore.SIGNAL('propertyChanged()'), self.onPropertyChanged )
    ColorWidget.connect ( ColorWidget, QtCore.SIGNAL ( 'clicked()' ), self.onClicked )
    ColorWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged ) 
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, ColorWidget ) :
    # register signal propertyChanged for updating the gui
    #self.disconnect( self.colorProperty, QtCore.SIGNAL('propertyChanged()'), self.onPropertyChanged )
    ColorWidget.disconnect ( ColorWidget, QtCore.SIGNAL ( 'clicked()' ), self.onClicked ) 
    ColorWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )      
  #
  # onClicked
  #
  def onClicked ( self ) : 
    #print( "ColorWidget = onClicked" )
    redValue = int ( self.widget.param.value [0] * 255 )
    greenValue = int ( self.widget.param.value [1] * 255 )
    blueValue = int ( self.widget.param.value [2] * 255 )
    colorSelected = QtGui.QColorDialog.getColor ( QtGui.QColor ( redValue, greenValue, blueValue ), self.widget )
    if colorSelected.isValid() :
      newValue = ( colorSelected.redF (),
                   colorSelected.greenF (),
                   colorSelected.blueF ())        
      self.widget.param.setValue ( newValue )
      #self.widget.param.paramChanged ()
      self.updateGui ( self.widget.param.value )
  #
  # onCurrentIndexChanged
  #
  def onCurrentIndexChanged ( self, idx ) :
    space = str ( self.selector.currentText () ) 
    if space == 'rgb' : space = None
    self.widget.param.space = space
  #
  # updateGui
  #
  def updateGui ( self, value ) :
    r = value [0] 
    g = value [1] 
    b = value [2] 
    
    pixmap = QtGui.QPixmap ( UI.COLOR_WIDTH, UI.HEIGHT )
    pixmap.fill ( QtCore.Qt.transparent )
    painter = QtGui.QPainter ()
    painter.begin ( pixmap )
    painter.setRenderHint ( QtGui.QPainter.Antialiasing, True )
    
    color = QtGui.QColor ( r * 255, g * 255, b * 255 )
    
    painter.setPen ( QtCore.Qt.NoPen )
    painter.setBrush ( color )  
    rect = QtCore.QRectF ( 0.0, 0.0, UI.COLOR_WIDTH, UI.HEIGHT )
    painter.drawRects ( rect  )
    painter.end ()
    
    self.colorEdit.setPixmap ( pixmap )


