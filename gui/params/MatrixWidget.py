#===============================================================================
# MatrixWidget.py
#
# 
#
#===============================================================================

from PyQt4 import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget 

#
# MatrixWidget
#
class MatrixWidget ( ParamWidget ):
  #
  #                 
  def buildGui ( self ):
    
    self.ui = Ui_MatrixWidget_field() 
    self.ui.setupUi ( self )
#
# Ui_MatrixWidget_field
#          
class Ui_MatrixWidget_field ( object ):
  #
  #
  def setupUi ( self, MatrixWidget ):

    self.widget = MatrixWidget
    
    self.floatEdit0 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit1 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit2 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit3 = QtGui.QLineEdit( MatrixWidget )
    
    self.floatEdit4 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit5 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit6 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit7 = QtGui.QLineEdit( MatrixWidget )
    
    self.floatEdit8 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit9 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit10 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit11 = QtGui.QLineEdit( MatrixWidget )
    
    self.floatEdit12 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit13 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit14 = QtGui.QLineEdit( MatrixWidget )
    self.floatEdit15 = QtGui.QLineEdit( MatrixWidget )
    
    
    self.floatEdit0.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
    self.floatEdit1.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit2.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit3.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.floatEdit4.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
    self.floatEdit5.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit6.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit7.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.floatEdit8.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
    self.floatEdit9.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit10.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit11.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.floatEdit12.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
    self.floatEdit13.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit14.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit15.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    
    self.floatEdit0.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit1.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit2.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit3.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.floatEdit4.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit5.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit6.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit7.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.floatEdit8.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit9.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit10.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit11.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.floatEdit12.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit13.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit14.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit15.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.selector = QtGui.QComboBox ( MatrixWidget )
    self.selector.setEditable ( False )
    #self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
    
    for label in [ "current", "shader", "object", "camera", "world", "raster", "NDC", "screen" ] :
      self.selector.addItem ( label )
    if self.widget.param.space != None :
      self.selector.setCurrentIndex( self.selector.findText ( self.widget.param.space ) )
    
        
    #spacer1 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    #spacer2 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    #spacer3 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    #spacer4 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.raw1 = QtGui.QWidget(  MatrixWidget )
    
    self.hl1 = QtGui.QHBoxLayout ( self.raw1 )
    self.hl1.setSpacing ( UI.SPACING )
    self.hl1.setMargin ( 0 )
    lt_space1 = QtGui.QSpacerItem ( UI.LT_SPACE, UI.HEIGHT, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum )
    self.hl1.addItem ( lt_space1 )    
    self.hl1.addWidget ( self.floatEdit0 )
    self.hl1.addWidget ( self.floatEdit1 )
    self.hl1.addWidget ( self.floatEdit2 )
    self.hl1.addWidget ( self.floatEdit3 )
    self.widget.hl.addWidget ( self.selector )
    
    spacer1 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    self.hl1.addItem ( spacer1 )
    
    self.raw2 = QtGui.QWidget(  MatrixWidget )
    
    self.hl2 = QtGui.QHBoxLayout ( self.raw2 )
    self.hl2.setSpacing ( UI.SPACING )
    self.hl2.setMargin ( 0 )
    lt_space2 = QtGui.QSpacerItem ( UI.LT_SPACE, UI.HEIGHT, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum )
    self.hl2.addItem ( lt_space2 )    
    self.hl2.addWidget ( self.floatEdit4 )
    self.hl2.addWidget ( self.floatEdit5 )
    self.hl2.addWidget ( self.floatEdit6 )
    self.hl2.addWidget ( self.floatEdit7 )
    spacer2 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    self.hl2.addItem ( spacer2 )
    
    self.raw3 = QtGui.QWidget(  MatrixWidget )
    
    self.hl3 = QtGui.QHBoxLayout ( self.raw3 )
    self.hl3.setSpacing ( UI.SPACING )
    self.hl3.setMargin ( 0 )
    lt_space3 = QtGui.QSpacerItem ( UI.LT_SPACE, UI.HEIGHT, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum )
    self.hl3.addItem ( lt_space3 )    
    self.hl3.addWidget ( self.floatEdit8 )
    self.hl3.addWidget ( self.floatEdit9 )
    self.hl3.addWidget ( self.floatEdit10 )
    self.hl3.addWidget ( self.floatEdit11 )
    spacer3 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    self.hl3.addItem ( spacer3 )
    
    self.raw4 = QtGui.QWidget(  MatrixWidget )
    
    self.hl4 = QtGui.QHBoxLayout ( self.raw4 )
    self.hl4.setSpacing ( UI.SPACING )
    self.hl4.setMargin ( 0 )
    lt_space4 = QtGui.QSpacerItem ( UI.LT_SPACE, UI.HEIGHT, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum )
    self.hl4.addItem ( lt_space4 )    
    self.hl4.addWidget ( self.floatEdit12 )
    self.hl4.addWidget ( self.floatEdit13 )
    self.hl4.addWidget ( self.floatEdit14 )
    self.hl4.addWidget ( self.floatEdit15 )
    spacer4 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    self.hl4.addItem ( spacer4 )
    
    spacer5 = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    self.widget.hl.addItem ( spacer5 )
        
    self.widget.vl.addWidget ( self.raw1 )
    self.widget.vl.addWidget ( self.raw2 )
    self.widget.vl.addWidget ( self.raw3 )
    self.widget.vl.addWidget ( self.raw4 )
    
    
    #self.widget.hl.addItem ( spacer )
    
    #self.widget.addItem ( self.vl )
    
    QtCore.QMetaObject.connectSlotsByName ( MatrixWidget )
    self.connectSignals ( MatrixWidget )
  #
  #
  def connectSignals ( self, MatrixWidget ):
    MatrixWidget.connect ( self.floatEdit0, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit1, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit2, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit3, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
    MatrixWidget.connect ( self.floatEdit4, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit5, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit6, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit7, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
    MatrixWidget.connect ( self.floatEdit8, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit9, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit10, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit11, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
    MatrixWidget.connect ( self.floatEdit12, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit13, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit14, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.connect ( self.floatEdit15, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
    MatrixWidget.connect ( self.selector, QtCore.SIGNAL( 'activated(int)' ), self.onCurrentIndexChanged ) 
  #
  #
  def disconnectSignals ( self, MatrixWidget ):
    MatrixWidget.disconnect ( self.floatEdit0, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit1, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit2, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit3, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
    MatrixWidget.disconnect ( self.floatEdit4, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit5, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit6, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit7, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
    MatrixWidget.disconnect ( self.floatEdit8, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit9, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit10, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit11, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
    MatrixWidget.disconnect ( self.floatEdit12, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit13, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit14, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    MatrixWidget.disconnect ( self.floatEdit15, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
    MatrixWidget.disconnect ( self.selector, QtCore.SIGNAL( 'activated(int)' ), self.onCurrentIndexChanged ) 
  #
  #                      
  def onFloatEditEditingFinished ( self ):
    floatStr0 = self.floatEdit0.text()
    floatStr1 = self.floatEdit1.text()
    floatStr2 = self.floatEdit2.text()
    floatStr3 = self.floatEdit3.text()
    f0 = floatStr0.toFloat()[0]
    f1 = floatStr1.toFloat()[0] 
    f2 = floatStr2.toFloat()[0]
    f3 = floatStr3.toFloat()[0]
    
    #self.widget.param.value[ 0 ] = [ f0, f1, f2, f3 ]
    
    floatStr0 = self.floatEdit4.text()
    floatStr1 = self.floatEdit5.text()
    floatStr2 = self.floatEdit6.text()
    floatStr3 = self.floatEdit7.text()
    f4 = floatStr0.toFloat()[0]
    f5 = floatStr1.toFloat()[0] 
    f6 = floatStr2.toFloat()[0]
    f7 = floatStr3.toFloat()[0]
    
    #self.widget.param.value[ 1 ] = [ f4, f5, f6, f7 ]
    
    floatStr0 = self.floatEdit8.text()
    floatStr1 = self.floatEdit9.text()
    floatStr2 = self.floatEdit10.text()
    floatStr3 = self.floatEdit11.text()
    f8 = floatStr0.toFloat()[0]
    f9 = floatStr1.toFloat()[0] 
    f10 = floatStr2.toFloat()[0]
    f11 = floatStr3.toFloat()[0]
    
    #self.widget.param.value[ 2 ] = [ f8, f9, f10, f11 ]
    
    floatStr0 = self.floatEdit12.text()
    floatStr1 = self.floatEdit13.text()
    floatStr2 = self.floatEdit14.text()
    floatStr3 = self.floatEdit15.text()
    f12 = floatStr0.toFloat()[0]
    f13 = floatStr1.toFloat()[0] 
    f14 = floatStr2.toFloat()[0]
    f15 = floatStr3.toFloat()[0]
    
    #self.widget.param.value[ 3 ] = [ f12, f13, f14, f15 ]
    
    self.widget.param.setValue ( [ [ f0, f1, f2, f3 ], [ f4, f5, f6, f7 ], [ f8, f9, f10, f11 ],[ f12, f13, f14, f15 ] ] )
  #
  #                      
  def onCurrentIndexChanged ( self, idx ):
    space = str ( self.selector.currentText () ) 
    if space == 'current' : space = None
    self.widget.param.space = space
  #
  # value  = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]   
  #      
  def updateGui ( self, value ): 
    self.floatEdit0.setText ( QtCore.QString.number( value[0][0], 'f', 3 ) )
    self.floatEdit1.setText ( QtCore.QString.number( value[0][1], 'f', 3 ) )
    self.floatEdit2.setText ( QtCore.QString.number( value[0][2], 'f', 3 ) )
    self.floatEdit3.setText ( QtCore.QString.number( value[0][3], 'f', 3 ) )
    
    self.floatEdit4.setText ( QtCore.QString.number( value[1][0], 'f', 3 ) )
    self.floatEdit5.setText ( QtCore.QString.number( value[1][1], 'f', 3 ) )
    self.floatEdit6.setText ( QtCore.QString.number( value[1][2], 'f', 3 ) )
    self.floatEdit7.setText ( QtCore.QString.number( value[1][3], 'f', 3 ) )
    
    self.floatEdit8.setText ( QtCore.QString.number( value[2][0], 'f', 3 ) )
    self.floatEdit9.setText ( QtCore.QString.number( value[2][1], 'f', 3 ) )
    self.floatEdit10.setText ( QtCore.QString.number( value[2][2], 'f', 3 ) )
    self.floatEdit11.setText ( QtCore.QString.number( value[2][3], 'f', 3 ) )
    
    self.floatEdit12.setText ( QtCore.QString.number( value[3][0], 'f', 3 ) )
    self.floatEdit13.setText ( QtCore.QString.number( value[3][1], 'f', 3 ) )
    self.floatEdit14.setText ( QtCore.QString.number( value[3][2], 'f', 3 ) )
    self.floatEdit15.setText ( QtCore.QString.number( value[3][3], 'f', 3 ) )
