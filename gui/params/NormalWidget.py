#===============================================================================
# NormalWidget.py
#
# 
#
#===============================================================================

from PyQt4 import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget 

#
# NormalWidget
#
class NormalWidget ( ParamWidget ):
  #
  #                 
  def buildGui ( self ):
    
    self.ui = Ui_NormalWidget_field() 
    self.ui.setupUi ( self )
#
# Ui_NormalWidget_field
#          
class Ui_NormalWidget_field ( object ):
  #
  #
  def setupUi ( self, NormalWidget ):

    self.widget = NormalWidget
    
    self.floatEdit0 = QtGui.QLineEdit( NormalWidget )
    self.floatEdit1 = QtGui.QLineEdit( NormalWidget )
    self.floatEdit2 = QtGui.QLineEdit( NormalWidget )
    
    self.floatEdit0.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.floatEdit1.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit2.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.floatEdit0.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit1.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    self.floatEdit2.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.floatEdit0 )
    self.widget.hl.addWidget ( self.floatEdit1 )
    self.widget.hl.addWidget ( self.floatEdit2 )
    
    self.widget.hl.addItem ( spacer )
    
    QtCore.QMetaObject.connectSlotsByName ( NormalWidget )
    self.connectSignals ( NormalWidget )
  #
  #
  def connectSignals ( self, NormalWidget ):
    NormalWidget.connect ( self.floatEdit0, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.connect ( self.floatEdit1, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.connect ( self.floatEdit2, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
  #
  #
  def disconnectSignals ( self, NormalWidget ):
    NormalWidget.disconnect ( self.floatEdit0, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.disconnect ( self.floatEdit1, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.disconnect ( self.floatEdit2, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
  #
  #                      
  def onFloatEditEditingFinished ( self ):
    floatStr0 = self.floatEdit0.text()
    floatStr1 = self.floatEdit1.text()
    floatStr2 = self.floatEdit2.text()
    f0 = floatStr0.toFloat()[0]
    f1 = floatStr1.toFloat()[0] 
    f2 = floatStr2.toFloat()[0]
    
    self.widget.param.value = [ f0, f1, f2 ]
    self.widget.param.paramChanged ()       
    #self.controler.editProperty( floatValue )  #
  #
  #
  #      
  def updateGui ( self, value ): 
    self.floatEdit0.setText ( QtCore.QString.number( value[0], 'f', 3 ) )
    self.floatEdit1.setText ( QtCore.QString.number( value[1], 'f', 3 ) )
    self.floatEdit2.setText ( QtCore.QString.number( value[2], 'f', 3 ) )
