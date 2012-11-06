#===============================================================================
# PointWidget.py
#
# 
#
#===============================================================================

from PyQt4 import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget 

#
# PointWidget
#
class PointWidget ( ParamWidget ):
  #
  #                 
  def buildGui ( self ):
    
    self.ui = Ui_PointWidget_field() 
    self.ui.setupUi ( self )
#
# Ui_PointWidget_field
#          
class Ui_PointWidget_field ( object ):
  #
  #
  def setupUi ( self, PointWidget ):

    self.widget = PointWidget
    
    self.floatEdit0 = QtGui.QLineEdit( PointWidget )
    self.floatEdit1 = QtGui.QLineEdit( PointWidget )
    self.floatEdit2 = QtGui.QLineEdit( PointWidget )
    
    self.floatEdit0.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.floatEdit1.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit2.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.floatEdit0.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit1.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit2.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.selector = QtGui.QComboBox ( PointWidget )
    self.selector.setEditable ( False )
    #self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
    
    for label in [ "current", "shader", "object", "camera", "world", "raster", "NDC", "screen" ] :
      self.selector.addItem ( label )
    if self.widget.param.space != None :
      self.selector.setCurrentIndex( self.selector.findText ( self.widget.param.space ) )  
    
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.floatEdit0 )
    self.widget.hl.addWidget ( self.floatEdit1 )
    self.widget.hl.addWidget ( self.floatEdit2 )
    self.widget.hl.addWidget ( self.selector )
    
    self.widget.hl.addItem ( spacer )
    
    QtCore.QMetaObject.connectSlotsByName ( PointWidget )
    self.connectSignals ( PointWidget )
  #
  #
  def connectSignals ( self, PointWidget ):
    PointWidget.connect ( self.floatEdit0, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    PointWidget.connect ( self.floatEdit1, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    PointWidget.connect ( self.floatEdit2, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    PointWidget.connect ( self.selector, QtCore.SIGNAL( 'activated(int)' ), self.onCurrentIndexChanged ) 
  #
  #
  def disconnectSignals ( self, PointWidget ):
    PointWidget.disconnect ( self.floatEdit0, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    PointWidget.disconnect ( self.floatEdit1, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    PointWidget.disconnect ( self.floatEdit2, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    PointWidget.disconnect ( self.selector, QtCore.SIGNAL( 'activated(int)' ), self.onCurrentIndexChanged ) 
  #
  #                      
  def onFloatEditEditingFinished ( self ):
    floatStr0 = self.floatEdit0.text()
    floatStr1 = self.floatEdit1.text()
    floatStr2 = self.floatEdit2.text()
    f0 = floatStr0.toFloat()[0]
    f1 = floatStr1.toFloat()[0] 
    f2 = floatStr2.toFloat()[0]
    
    self.widget.param.setValue ( [ f0, f1, f2 ] )
  #
  #                      
  def onCurrentIndexChanged ( self, idx ):
    space = str ( self.selector.currentText () ) 
    if space == 'current' : space = None
    self.widget.param.space = space

  #
  #
  #      
  def updateGui ( self, value ): 
    self.floatEdit0.setText ( QtCore.QString.number( value[0], 'f', 3 ) )
    self.floatEdit1.setText ( QtCore.QString.number( value[1], 'f', 3 ) )
    self.floatEdit2.setText ( QtCore.QString.number( value[2], 'f', 3 ) )
