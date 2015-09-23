"""

 StringWidget.py

"""
from core.mePyQt import QtGui, QtCore

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI 
from paramWidget import ParamWidget 
#
# StringWidget
#
class StringWidget ( ParamWidget ) :
  #
  # buildGui
  #                 
  def buildGui ( self ) :
    #
    if not self.ignoreSubtype :
      if self.param.subtype == 'selector': 
        self.ui = Ui_StringWidget_selector ()
      elif self.param.subtype == 'file':
        self.ui = Ui_StringWidget_file () 
      else:
        self.ui = Ui_StringWidget_field () 
    else :
      self.ui = Ui_StringWidget_field ()    
    self.ui.setupUi ( self )
#
# Ui_StringWidget_field
#
class Ui_StringWidget_field ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, StringWidget ) :
    #
    hl = QtGui.QHBoxLayout ()
    hl.setStretch ( 1, 1 )
    
    self.widget = StringWidget
    
    self.stringEdit = QtGui.QLineEdit ( StringWidget )
    
    self.stringEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.stringEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
    
    hl.addWidget ( self.stringEdit )
    self.widget.param_vl.addLayout ( hl )
    
    QtCore.QMetaObject.connectSlotsByName ( StringWidget )
    self.connectSignals ( StringWidget )
  #
  # connectSignals
  #
  def connectSignals ( self, StringWidget ) :
    #
    StringWidget.connect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, StringWidget ) :
    #
    StringWidget.disconnect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
  #
  # onStringEditEditingFinished
  #
  def onStringEditEditingFinished ( self ) :
    #
    stringValue = self.stringEdit.text ()
    self.widget.param.setValue ( str ( stringValue ) )
  #
  # updateGui
  #
  def updateGui ( self, value ) :
    # 
    self.stringEdit.setText ( value )
#
# Ui_StringWidget_selector
#          
class Ui_StringWidget_selector ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, StringWidget ) :
    #
    hl = QtGui.QHBoxLayout ()
    self.widget = StringWidget
    
    self.selector = QtGui.QComboBox ( StringWidget )
    self.selector.setEditable ( False )
    self.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
    
    rangeList = self.widget.param.getRangeValues ()
    
    for ( label, value ) in rangeList :
      #print "label = %s value = %s" % ( label, value )
      self.selector.addItem ( label, value )
    
    spacer = QtGui.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
    
    hl.addWidget ( self.selector )
    hl.addItem ( spacer )
    self.widget.param_vl.addLayout ( hl )
    
    QtCore.QMetaObject.connectSlotsByName ( StringWidget )
    self.connectSignals ( StringWidget )
  #
  # connectSignals
  #
  def connectSignals ( self, StringWidget ) :
    #
    StringWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, StringWidget ) :
    #
    StringWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
  #
  # onCurrentIndexChanged
  #
  def onCurrentIndexChanged ( self, idx ) :
    pass
    stringValue = self.selector.itemData ( idx ).toString ()
    #print ">> Ui_StringWidget_selector idx = %d setValue = %s" % ( idx, stringValue )
    self.widget.param.setValue ( str ( stringValue ) )
  #
  # updateGui
  #
  def updateGui ( self, setValue ) :
    #
    currentIdx = -1
    i = 0
    rangeList = self.widget.param.getRangeValues ()
    for ( label, value ) in rangeList :
      if setValue == value : 
        currentIdx = i
        break
      i += 1
    self.selector.setCurrentIndex ( currentIdx )
#
# Ui_StringWidget_file
#
class Ui_StringWidget_file ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, StringWidget ) :
    #
    hl = QtGui.QHBoxLayout ()
    hl.setStretch ( 1, 1 )
    
    self.widget = StringWidget
    
    self.stringEdit = QtGui.QLineEdit ( StringWidget )
    
    self.stringEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.stringEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
    
    self.btnBrowseDir = QtGui.QToolButton ( StringWidget )
    self.btnBrowseDir.setText ( '...' )
    self.btnBrowseDir.setMinimumSize ( QtCore.QSize ( UI.BROWSE_WIDTH, UI.HEIGHT ) )
    self.btnBrowseDir.setMaximumSize ( QtCore.QSize ( UI.BROWSE_WIDTH, UI.HEIGHT ) )
    
    hl.addWidget ( self.stringEdit )
    hl.addWidget ( self.btnBrowseDir )
    self.widget.param_vl.addLayout ( hl )
    
    
    #QtCore.QMetaObject.connectSlotsByName ( StringWidget )
   
    self.connectSignals ( StringWidget )
  #
  # connectSignals
  #
  def connectSignals ( self, StringWidget ) :
    #
    StringWidget.connect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
    StringWidget.connect ( self.btnBrowseDir, QtCore.SIGNAL ( 'clicked()' ), self.onBrowseFile )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, StringWidget ) :
    #
    StringWidget.disconnect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
    StringWidget.disconnect ( self.btnBrowseDir, QtCore.SIGNAL ( 'clicked()' ), self.onBrowseFile )
  #
  # onStringEditEditingFinished
  #
  def onStringEditEditingFinished ( self ) :
    #
    stringValue = self.stringEdit.text ()
    self.widget.param.value = str ( stringValue )
    #self.widget.param.paramChanged ()
  #
  # onBrowseFile
  #
  def onBrowseFile ( self ) :
    #
    if DEBUG_MODE : print '>> Ui_StringWidget_file onBrowseFile'
    typeFilter = ''
    rangeList = self.widget.param.getRangeValues ()
    
    for ( label, value ) in rangeList :
      if DEBUG_MODE : print "label = %s value = %s" % ( label, value )
      typeFilter += ( label + ' ' + value + ';;' )
      #self.selector.addItem ( label, value )
    #print '>> Ui_StringWidget_file typeFilter = %s' % typeFilter   
    
    curDir = app_global_vars [ 'ProjectPath' ]
    
    filename = QtGui.QFileDialog.getOpenFileName ( self.widget, 'Select file', curDir, typeFilter )
    
    if filename != '' : 
      self.widget.param.setValue ( str ( filename ) )
      self.updateGui ( self.widget.param.value )
  #
  # updateGui
  #
  def updateGui ( self, value ) :
    # 
    self.stringEdit.setText ( value )    
