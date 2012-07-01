#===============================================================================
# IntWidget.py
#
# 
#
#===============================================================================

from PyQt4 import QtGui, QtCore

import gui.ui_settings as UI 
from paramWidget import ParamWidget 

#
# IntWidget
#
class IntWidget ( ParamWidget ):
  #
  #                 
  def buildGui ( self ):
    
    if self.param.subtype == 'selector': 
      self.ui = Ui_IntWidget_selector()
    elif self.param.subtype == 'switch': 
      self.ui = Ui_IntWidget_switch()
    elif self.param.subtype == 'slider' or self.param.subtype == 'vslider' : 
      self.ui = Ui_IntWidget_slider()
    else:
      self.ui = Ui_IntWidget_field() 
       
    self.ui.setupUi ( self )
#
# Ui_IntWidget_field
#          
class Ui_IntWidget_field ( object ):
  #
  #
  def setupUi ( self, IntWidget ):

    self.widget = IntWidget
    
    self.intEdit = QtGui.QLineEdit( IntWidget )
    
    self.intEdit.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.intEdit.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.intEdit )
    self.widget.hl.addItem ( spacer )
    #self.widget.hl.setStretch ( 1, 1 )
    
    QtCore.QMetaObject.connectSlotsByName ( IntWidget )
    self.connectSignals ( IntWidget )
  #
  #
  def connectSignals ( self, IntWidget ):
    IntWidget.connect ( self.intEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onIntEditEditingFinished )
  #
  #
  def disconnectSignals ( self, IntWidget ):
    IntWidget.disconnect ( self.intEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onIntEditEditingFinished )
  #
  #                      
  def onIntEditEditingFinished ( self ) :
    intStr = self.intEdit.text()
    intValue = intStr.toInt()[0] 
    self.widget.param.value = intValue       
    #self.controler.editProperty( floatValue )  #
  #
  #      
  def updateGui ( self, value ): self.intEdit.setText ( QtCore.QString.number( value ) )
#
# Ui_IntWidget_switch
#          
class Ui_IntWidget_switch ( object ):
  #
  #
  def setupUi ( self, IntWidget ):

    self.widget = IntWidget
    
    self.checkBox = QtGui.QCheckBox( IntWidget )
    
    self.checkBox.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.checkBox.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.checkBox )
    self.widget.hl.addItem ( spacer )
    #self.widget.hl.setStretch ( 1, 1 )
    
    QtCore.QMetaObject.connectSlotsByName ( IntWidget )
    self.connectSignals ( IntWidget )
  #
  #
  def connectSignals ( self, IntWidget ):
    IntWidget.connect( self.checkBox, QtCore.SIGNAL('stateChanged(int)'), self.onStateChanged )
  #
  #
  def disconnectSignals ( self, IntWidget ):
    IntWidget.disconnect( self.checkBox, QtCore.SIGNAL('stateChanged(int)'), self.onStateChanged )  #
  # 
  #                     
  def onStateChanged ( self, value ):
    intValue = self.checkBox.isChecked()    
    # print "CALL: onStateChanged value = %d  floatValue = %d" % ( value, floatValue )
    self.widget.param.value = intValue
  #
  #      
  def updateGui ( self, value ): self.checkBox.setChecked( value != 0 )  
#
# Ui_IntWidget_selector
#          
class Ui_IntWidget_selector ( object ):
  #
  #
  def setupUi ( self, IntWidget ):
    
    self.widget = IntWidget
    
    self.selector = QtGui.QComboBox ( IntWidget )
    self.selector.setEditable ( False )
    self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
    
    rangeList = self.widget.param.getRangeValues ()
    for ( label, value ) in rangeList :
      #print "label = %s value = %s" % ( label, value )
      self.selector.addItem ( label, int( value ) )
    
    spacer = QtGui.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    self.widget.hl.addWidget ( self.selector )
    self.widget.hl.addItem ( spacer )
    
    QtCore.QMetaObject.connectSlotsByName ( IntWidget )
    self.connectSignals ( IntWidget )
  #
  #
  def connectSignals ( self, IntWidget ):
    IntWidget.connect ( self.selector, QtCore.SIGNAL( 'activated(int)' ), self.onCurrentIndexChanged ) #currentIndexChanged
  #
  #
  def disconnectSignals ( self, IntWidget ):
    IntWidget.disconnect ( self.selector, QtCore.SIGNAL( 'activated(int)' ), self.onCurrentIndexChanged )
  #
  #                      
  def onCurrentIndexChanged ( self, idx ):
    ( intValue, ok ) = self.selector.itemData ( idx ).toInt()
    #print ">> Ui_IntWidget_selector setValue = " # %d" % intValue
    #print intValue
    self.widget.param.value = int( intValue )
    self.widget.param.paramChanged ()
    #self.controler.editProperty( stringValue )
  #
  #      
  def updateGui ( self, setValue ): 
    currentIdx = -1
    i = 0
    print ">> Ui_IntWidget_selector setValue = %s" % setValue
    rangeList = self.widget.param.getRangeValues ()
    for ( label, value ) in rangeList :
      print ( "label = %s : value = %s" ) % ( label, value )
      if setValue == value : 
        currentIdx = i
        break
      i += 1
    self.selector.setCurrentIndex( currentIdx )
    
#
# Ui_IntWidget_slider
#          
class Ui_IntWidget_slider ( object ):
  #
  #
  def setupUi ( self, IntWidget ):

    self.widget = IntWidget
    
    self.intEdit = QtGui.QLineEdit( IntWidget )
    
    self.intEdit.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.intEdit.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
    
    self.slider = QtGui.QSlider ( QtCore.Qt.Horizontal, IntWidget )
    
    intMinVal = 0
    intMaxVal = 10
    intStep = 1
    
    rangeList = self.widget.param.getRangeValues ()
    if len ( rangeList ) :
      intMinVal = rangeList[ 0 ]
      intMaxVal = rangeList[ 1 ]
      intStep = rangeList[ 2 ]
    
    if intStep == 0 : intStep = 1
    
    #print 'intMinVal = %d intMaxVal = %d' % ( intMinVal, intMaxVal )
    
    self.slider.setRange ( intMinVal, intMaxVal )
    self.slider.setSingleStep ( intStep )
    
    self.slider.setValue ( int( self.widget.param.value ) )

    #setTickInterval
    #setPageStep
    
    self.widget.hl.addWidget ( self.intEdit )
    self.widget.hl.addWidget ( self.slider )
    self.widget.hl.setStretch ( 1, 1 )
    
    QtCore.QMetaObject.connectSlotsByName ( IntWidget )
    self.connectSignals ( IntWidget )
  #
  #
  def connectSignals ( self, IntWidget ):
    IntWidget.connect ( self.intEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onIntEditEditingFinished )
    IntWidget.connect ( self.slider, QtCore.SIGNAL( 'valueChanged(int)' ), self.onSliderValueChanged )
  #
  #
  def disconnectSignals ( self, IntWidget ):
    IntWidget.disconnect ( self.intEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onIntEditEditingFinished )
    IntWidget.disconnect ( self.slider, QtCore.SIGNAL( 'valueChanged(int)' ), self.onSliderValueChanged )
  #
  #                      
  def onIntEditEditingFinished ( self ):
    intStr = self.intEdit.text()
    intValue = intStr.toInt()[0] 
    self.widget.param.value = intValue     
    self.slider.setValue ( intValue )
  #
  #                      
  def onSliderValueChanged ( self, value ) :
    self.widget.param.value = value
    self.updateGui ( value) 
    #self.widget.param.paramChanged ()
  #
  #      
  def updateGui ( self, value ): self.intEdit.setText ( QtCore.QString.number( value ) ) 