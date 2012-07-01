#===============================================================================
# FloatWidget.py
#
# 
#
#===============================================================================
import math
from decimal import *

from PyQt4 import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget 

#
# FloatWidget
#
class FloatWidget ( ParamWidget ):
  #
  #                 
  def buildGui ( self ):
    
    if self.param.subtype == 'selector': 
      self.ui = Ui_FloatWidget_selector()
    elif self.param.subtype == 'switch': 
      self.ui = Ui_FloatWidget_switch()
    elif self.param.subtype == 'slider' or self.param.subtype == 'vslider' : 
      self.ui = Ui_FloatWidget_slider()
    else:
      self.ui = Ui_FloatWidget_field() 
       
    self.ui.setupUi ( self )
#
# Ui_FloatWidget_field
#          
class Ui_FloatWidget_field ( object ):
  #
  #
  def setupUi ( self, FloatWidget ):

    self.widget = FloatWidget
    
    self.floatEdit = QtGui.QLineEdit( FloatWidget )
    
    self.floatEdit.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.floatEdit.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.floatEdit )
    self.widget.hl.addItem ( spacer )
    #self.widget.hl.setStretch ( 1, 1 )
    
    QtCore.QMetaObject.connectSlotsByName ( FloatWidget )
    self.connectSignals ( FloatWidget )
  #
  #
  def connectSignals ( self, FloatWidget ):
    FloatWidget.connect ( self.floatEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
  #
  #
  def disconnectSignals ( self, FloatWidget ):
    FloatWidget.disconnect ( self.floatEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
  #
  #                      
  def onFloatEditEditingFinished ( self ):
    floatStr = self.floatEdit.text()
    floatValue = floatStr.toFloat()[0] 
    self.widget.param.value = floatValue       
    #self.controler.editProperty( floatValue )  #
  #
  #      
  def updateGui ( self, value ): self.floatEdit.setText ( QtCore.QString.number(value, 'f', 3) )
#
# Ui_FloatWidget_switch
#          
class Ui_FloatWidget_switch ( object ):
  #
  #
  def setupUi ( self, FloatWidget ):

    self.widget = FloatWidget
    
    self.checkBox = QtGui.QCheckBox( FloatWidget )
    
    self.checkBox.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.checkBox.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.checkBox )
    self.widget.hl.addItem ( spacer )
    #self.widget.hl.setStretch ( 1, 1 )
    
    QtCore.QMetaObject.connectSlotsByName ( FloatWidget )
    self.connectSignals ( FloatWidget )
  #
  #
  def connectSignals ( self, FloatWidget ):
    FloatWidget.connect( self.checkBox, QtCore.SIGNAL('stateChanged(int)'), self.onStateChanged )
  #
  #
  def disconnectSignals ( self, FloatWidget ):
    FloatWidget.disconnect( self.checkBox, QtCore.SIGNAL('stateChanged(int)'), self.onStateChanged )  #
  # 
  #                     
  def onStateChanged ( self, value ):
    floatValue = self.checkBox.isChecked()    
    # print "CALL: onStateChanged value = %d  floatValue = %d" % ( value, floatValue )
    self.widget.param.value = floatValue
  #
  #      
  def updateGui ( self, value ): self.checkBox.setChecked( value != 0 )  
#
# Ui_FloatWidget_selector
#          
class Ui_FloatWidget_selector ( object ):
  #
  #
  def setupUi ( self, FloatWidget ):
    
    self.widget = FloatWidget
    
    self.selector = QtGui.QComboBox ( FloatWidget )
    self.selector.setEditable ( False )
    self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
    
    rangeList = self.widget.param.getRangeValues ()
    for ( label, value ) in rangeList :
      #print "label = %s value = %s" % ( label, value )
      self.selector.addItem ( label, float( value ) )
    
    spacer = QtGui.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.selector )
    self.widget.hl.addItem ( spacer )
    
    QtCore.QMetaObject.connectSlotsByName ( FloatWidget )
    self.connectSignals ( FloatWidget )
  #
  #
  def connectSignals ( self, FloatWidget ):
    FloatWidget.connect ( self.selector, QtCore.SIGNAL( 'activated(int)' ), self.onCurrentIndexChanged ) #currentIndexChanged
  #
  #
  def disconnectSignals ( self, FloatWidget ):
    FloatWidget.disconnect ( self.selector, QtCore.SIGNAL( 'activated(int)' ), self.onCurrentIndexChanged )
  #
  #                      
  def onCurrentIndexChanged ( self, idx ):
    ( floatValue, ok ) = self.selector.itemData ( idx ).toFloat()
    print ">> Ui_FloatWidget_selector setValue = " # %d" % floatValue
    print floatValue
    self.widget.param.value = float( floatValue )
    self.widget.param.paramChanged ()
    #self.controler.editProperty( stringValue )
  #
  #      
  def updateGui ( self, setValue ): 
    currentIdx = -1
    i = 0
    print ">> Ui_FloatWidget_selector setValue = %s" % setValue
    rangeList = self.widget.param.getRangeValues ()
    for ( label, value ) in rangeList :
      print ( "label = %s : value = %s" ) % ( label, value )
      if setValue == value : 
        currentIdx = i
        break
      i += 1
    self.selector.setCurrentIndex( currentIdx )
    
#
# Ui_FloatWidget_slider
#          
class Ui_FloatWidget_slider ( object ):
  #
  #
  def getRangeMultiplier ( self, floatStep ) :
    
    multiplier = 1.0
    value = float ( floatStep )
    while not value.is_integer() :
      value *= 10.0
      multiplier *= 10.0
    
    return multiplier
  #
  #
  def setupUi ( self, FloatWidget ):

    self.widget = FloatWidget
    
    self.floatEdit = QtGui.QLineEdit( FloatWidget )
    
    self.floatEdit.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.floatEdit.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.slider = QtGui.QSlider ( QtCore.Qt.Horizontal, FloatWidget )
    
    floatMinVal = 0
    floatMaxVal = 1
    floatStep = 0.1
    
    rangeList = self.widget.param.getRangeValues ()
    if len ( rangeList ) :
      floatMinVal = rangeList[ 0 ]
      floatMaxVal = rangeList[ 1 ]
      floatStep = rangeList[ 2 ]
    
    if floatStep == 0.0 : floatStep = 0.1

    multiplier = self.getRangeMultiplier ( floatStep )
    
    intMinVal = int ( floatMinVal * multiplier )
    intMaxVal = int ( floatMaxVal * multiplier )
    intStep = int ( floatStep * multiplier )
    
    print 'intMinVal = %d intMaxVal = %d' % ( intMinVal, intMaxVal )
    
    self.slider.setRange ( intMinVal, intMaxVal )
    self.slider.setSingleStep ( intStep )
    
    self.slider.setValue ( int( self.widget.param.value * multiplier ) )

    #setTickInterval
    #setPageStep
    
    self.widget.hl.addWidget ( self.floatEdit )
    self.widget.hl.addWidget ( self.slider )
    self.widget.hl.setStretch ( 1, 1 )
    
    QtCore.QMetaObject.connectSlotsByName ( FloatWidget )
    self.connectSignals ( FloatWidget )
  #
  #
  def connectSignals ( self, FloatWidget ):
    FloatWidget.connect ( self.floatEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    FloatWidget.connect ( self.slider, QtCore.SIGNAL( 'valueChanged(int)' ), self.onSliderValueChanged )
  #
  #
  def disconnectSignals ( self, FloatWidget ):
    FloatWidget.disconnect ( self.floatEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onFloatEditEditingFinished )
    FloatWidget.disconnect ( self.slider, QtCore.SIGNAL( 'valueChanged(int)' ), self.onSliderValueChanged )
  #
  #                      
  def onFloatEditEditingFinished ( self ) :
    floatStr = self.floatEdit.text()
    floatValue = floatStr.toFloat()[0] 
    self.widget.param.value = floatValue       
    #self.controler.editProperty( floatValue )  #
    
    floatMinVal = 0
    floatMaxVal = 1
    floatStep = 0.1
    
    rangeList = self.widget.param.getRangeValues ()
    if len ( rangeList ) :
      floatMinVal = rangeList[ 0 ]
      floatMaxVal = rangeList[ 1 ]
      floatStep = rangeList[ 2 ]
    
    if floatStep == 0.0 : floatStep = 0.1
    
    multiplier = self.getRangeMultiplier ( floatStep )
      
    intMinVal = int ( floatMinVal * multiplier )
    intMaxVal = int ( floatMaxVal * multiplier )
    intStep = int ( floatStep * multiplier )
    
    self.slider.setValue ( int( floatValue * multiplier ) )
    
  #
  #                      
  def onSliderValueChanged ( self, value ) :
    intValue = value #self.slider.value ()
    
    floatMinVal = 0
    floatMaxVal = 1
    floatStep = 0.1
    
    rangeList = self.widget.param.getRangeValues ()
    if len ( rangeList ) :
      floatMinVal = rangeList[ 0 ]
      floatMaxVal = rangeList[ 1 ]
      floatStep = rangeList[ 2 ]
    
    if floatStep == 0.0 : floatStep = 0.1
    
    multiplier = self.getRangeMultiplier ( floatStep ) 
    
    floatValue = float ( intValue ) / float ( multiplier )
    self.widget.param.value = floatValue
    self.updateGui ( floatValue ) 
    #self.widget.param.paramChanged ()
  #
  #      
  def updateGui ( self, value ): 
    #rangeList = self.widget.param.getRangeValues ()
    
    self.floatEdit.setText ( QtCore.QString.number(value, 'f', 3) )