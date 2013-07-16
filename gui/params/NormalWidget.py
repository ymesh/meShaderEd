"""

 NormalWidget.py

"""
from PyQt4 import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget 
#
# NormalWidget
#
class NormalWidget ( ParamWidget ) :
  #
  # buildGui
  #      
  def buildGui ( self ) :
    #
    self.ui = Ui_NormalWidget_field () 
    self.ui.setupUi ( self )
#
# Ui_NormalWidget_field
#          
class Ui_NormalWidget_field ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, NormalWidget ) :
    #
    hl = QtGui.QHBoxLayout ()
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
    
    self.selector = QtGui.QComboBox ( NormalWidget )
    self.selector.setEditable ( False )
    #self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
    
    for label in [ "current", "shader", "object", "camera", "world", "raster", "NDC", "screen" ] :
      self.selector.addItem ( label )
    if self.widget.param.space != None :
      self.selector.setCurrentIndex( self.selector.findText ( self.widget.param.space ) )
    
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    hl.addWidget ( self.floatEdit0 )
    hl.addWidget ( self.floatEdit1 )
    hl.addWidget ( self.floatEdit2 )
    hl.addWidget ( self.selector )
    hl.addItem ( spacer )
    
    self.widget.param_vl.addLayout ( hl )
    
    QtCore.QMetaObject.connectSlotsByName ( NormalWidget )
    self.connectSignals ( NormalWidget )
  #
  # connectSignals
  #
  def connectSignals ( self, NormalWidget ) :
    #
    NormalWidget.connect ( self.floatEdit0, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.connect ( self.floatEdit1, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.connect ( self.floatEdit2, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged ) 
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, NormalWidget ) :
    #
    NormalWidget.disconnect ( self.floatEdit0, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.disconnect ( self.floatEdit1, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.disconnect ( self.floatEdit2, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    NormalWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged ) 
  #
  # onFloatEditEditingFinished
  #
  def onFloatEditEditingFinished ( self ) :
    #
    floatStr0 = self.floatEdit0.text ()
    floatStr1 = self.floatEdit1.text ()
    floatStr2 = self.floatEdit2.text ()
    f0 = floatStr0.toFloat ()[0]
    f1 = floatStr1.toFloat ()[0] 
    f2 = floatStr2.toFloat ()[0]
    
    self.widget.param.setValue ( [ f0, f1, f2 ] )
  #
  # onCurrentIndexChanged
  #
  def onCurrentIndexChanged ( self, idx ) :
    #
    space = str ( self.selector.currentText () ) 
    if space == 'current' : space = None
    self.widget.param.space = space
  #
  # updateGui
  #      
  def updateGui ( self, value ) :
    # 
    self.floatEdit0.setText ( QtCore.QString.number ( value [0], 'f', 3 ) )
    self.floatEdit1.setText ( QtCore.QString.number ( value [1], 'f', 3 ) )
    self.floatEdit2.setText ( QtCore.QString.number ( value [2], 'f', 3 ) )
