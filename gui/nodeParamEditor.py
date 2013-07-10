"""
 nodeParamEditor.py

 ver. 1.0.0
 
 Author: Yuri Meshalkin (aka mesh) (mesh@kpp.kiev.ua)

 Dialog for managing node

"""
import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars, DEBUG_MODE, VALID_PARAM_TYPES
from core.nodeParam import *

import gui.ui_settings as UI
from gui.params.StringWidget import StringWidget
from gui.params.FloatWidget import FloatWidget
from gui.params.IntWidget import IntWidget
from gui.params.ColorWidget import ColorWidget
from gui.params.NormalWidget import NormalWidget
from gui.params.PointWidget import PointWidget
from gui.params.VectorWidget import VectorWidget
from gui.params.MatrixWidget import MatrixWidget
from gui.params.TextWidget import TextWidget
from gui.params.ControlWidget import ControlWidget

from ui_nodeParamEditor import Ui_NodeParamEditor
#
# NodeParamEditor
#
class NodeParamEditor ( QtGui.QWidget ) :
  #
  # __init__
  #
  def __init__ ( self, parent ) :
    #
    QtGui.QDialog.__init__ ( self )
    self.param = None
    self.param_default = None
    self.paramWidgets = {  'string'       : StringWidget
                          ,'image'        : StringWidget
                          ,'rib'          : StringWidget
                          ,'surface'      : StringWidget
                          ,'displacement' : StringWidget
                          ,'light'        : StringWidget
                          ,'volume'       : StringWidget
                          ,'float'        : FloatWidget
                          ,'int'          : IntWidget
                          ,'color'        : ColorWidget
                          ,'normal'       : NormalWidget
                          ,'transform'    : PointWidget
                          ,'point'        : PointWidget
                          ,'vector'       : VectorWidget
                          ,'matrix'       : MatrixWidget
                          ,'text'         : TextWidget
                          ,'control'      : ControlWidget
                          ,'shader'       : StringWidget
                          ,'geom'         : StringWidget
                        }

    self.buildGui()
  #
  #
  def __delete__ ( self, obj ) :
    #
    print '* NodeParamEditor closed... %s' % str( obj )
  #
  # buildGui
  #
  def buildGui ( self ) :
    # build the gui created with QtDesigner
    self.ui = Ui_NodeParamEditor ( )
    self.ui.setupUi ( self )

    # correct UI sizes for some controls
    self.ui.check_enabled.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    self.ui.check_enabled.setMaximumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    
    self.ui.check_display.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    self.ui.check_display.setMaximumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )

    self.ui.check_shader.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    self.ui.check_shader.setMaximumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )

    for label in VALID_PARAM_TYPES : self.ui.type_comboBox.addItem ( label )
    
    self.ui.type_comboBox.setCurrentIndex ( -1 )
    self.ui.type_comboBox.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.ui.type_comboBox.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )

    # temporary disabled, until "how to do it gracefully" will be clear ...
    self.ui.type_comboBox.setEnabled ( False )

    for label in [ 'None', 'uniform', 'varying', ]  :
      self.ui.detail_comboBox.addItem ( label )
    self.ui.detail_comboBox.setCurrentIndex ( -1 )
    self.ui.detail_comboBox.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.ui.detail_comboBox.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )

    for label in [ 'None', 'internal', 'external', 'primitive', 'attribute' ]  :
      self.ui.provider_comboBox.addItem ( label )
    self.ui.provider_comboBox.setCurrentIndex ( -1 )
    self.ui.provider_comboBox.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.ui.provider_comboBox.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )

    for label in [ 'None', 'slider', 'switch', 'selector', 'file', 'button' ]  :
      self.ui.subtype_comboBox.addItem ( label )
    self.ui.subtype_comboBox.setCurrentIndex ( -1 )
    self.ui.subtype_comboBox.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.ui.subtype_comboBox.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
  #
  # As paramWidet is monitoring a change of param.value only,
  # we need to cynchronize changing of param_default.value with param.default
  #
  def onParamDefValueChanged ( self, param ) :
    #
    if DEBUG_MODE : print '* onParamDefValueChanged'
    self.param.default = self.param_default.value
  #
  # onParamValueChanged
  #
  def onParamValueChanged ( self, param ) :
    #
    if DEBUG_MODE : print '* onParamValueChanged'
    self.param.value = param.value
  #
  # connectSignals
  #
  def connectSignals ( self ) :
    #
    self.connect ( self.param_default, QtCore.SIGNAL ( 'paramChanged(QObject)' ), self.onParamDefValueChanged )
    self.connect ( self.ui.name_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditParamName )
    self.connect ( self.ui.label_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditParamLabel )
    self.connect ( self.ui.check_enabled, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onEditParamEnabled )
    self.connect ( self.ui.check_display, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onEditParamDisplay )
    self.connect ( self.ui.check_shader, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onEditParamShader )
    self.connect ( self.ui.type_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditParamType )
    self.connect ( self.ui.detail_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditParamDetail )
    self.connect ( self.ui.provider_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditParamProvider )
    self.connect ( self.ui.subtype_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditParamSubtype )
    self.connect ( self.ui.range_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditParamRange )
    self.connect ( self.ui.descr_plainTextEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditParamHelp )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self ) :
    #
    if self.param_default is not None :
      self.disconnect ( self.param_default, QtCore.SIGNAL ( 'paramChanged(QObject)' ), self.onParamDefValueChanged )
    if self.param is not None :
      self.disconnect ( self.ui.name_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditParamName )
      self.disconnect ( self.ui.label_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditParamLabel )
      self.disconnect ( self.ui.check_enabled, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onEditParamEnabled )
      self.disconnect ( self.ui.check_display, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onEditParamDisplay )
      self.disconnect ( self.ui.check_shader, QtCore.SIGNAL ( 'stateChanged(int)' ), self.onEditParamShader )
      self.disconnect ( self.ui.type_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditParamType )
      self.disconnect ( self.ui.detail_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditParamDetail )
      self.disconnect ( self.ui.provider_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditParamProvider )
      self.disconnect ( self.ui.subtype_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditParamSubtype )
      self.disconnect ( self.ui.descr_plainTextEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditParamHelp )
  #
  # reset
  #
  def reset ( self ) :
    #
    self.ui.name_lineEdit.setText ( '' )
    self.ui.label_lineEdit.setText ( '' )
    
    self.ui.check_enabled.setChecked ( True )
    self.ui.check_display.setChecked ( True )
    self.ui.check_shader.setChecked ( False )

    self.ui.type_comboBox.setCurrentIndex( -1 )
    self.ui.detail_comboBox.setCurrentIndex ( -1 )
    self.ui.provider_comboBox.setCurrentIndex ( -1 )
    self.ui.subtype_comboBox.setCurrentIndex ( -1 )
    self.ui.range_lineEdit.setText ( '' )

    doc = QtGui.QTextDocument ()
    doc.setPlainText ( '' )
    layout = QtGui.QPlainTextDocumentLayout ( doc )
    doc.setDocumentLayout ( layout )
    self.ui.descr_plainTextEdit.setDocument ( doc )
  #
  # Remove stackedWidget's layout every time,
  # when current parameter (or it's type) is changing
  #
  def removeValueWidget ( self ) :
    #
    while True :
      currentWidget = self.ui.value_stackedWidget.currentWidget ()
      if currentWidget is not None :
        #print '> removeWidget: %s' % str( currentWidget )
        self.ui.value_stackedWidget.removeWidget ( currentWidget )
      else :
        break
  #
  # setParam
  #
  def setParam ( self, param ) :
    #
    self.removeValueWidget()
    self.disconnectSignals()
    self.param = param
    
    if self.param is not None :
      #import copy
      self.param_default = self.param.copy() # duplicate param for default value editing
      self.param_default.value = param.default

      self.ui.name_lineEdit.setText ( self.param.name )
      self.ui.label_lineEdit.setText ( self.param.label )
      
      self.ui.check_enabled.setChecked ( self.param.enabled )
      self.ui.check_display.setChecked ( self.param.display )
      self.ui.check_shader.setChecked ( self.param.shaderParam )

      self.ui.type_comboBox.setCurrentIndex ( self.ui.type_comboBox.findText ( self.param.type ) )
      self.ui.detail_comboBox.setCurrentIndex ( self.ui.detail_comboBox.findText ( self.param.detail ) )
      self.ui.provider_comboBox.setCurrentIndex ( self.ui.provider_comboBox.findText ( self.param.provider ) )
      self.ui.subtype_comboBox.setCurrentIndex ( self.ui.subtype_comboBox.findText ( self.param.subtype ) )
      self.ui.range_lineEdit.setText ( self.param.range )

      doc = QtGui.QTextDocument ()
      help_text = ''
      if self.param.help != None : help_text = self.param.help

      doc.setPlainText ( help_text )
      layout = QtGui.QPlainTextDocumentLayout ( doc )
      doc.setDocumentLayout( layout )

      self.ui.descr_plainTextEdit.setDocument ( doc )

      frame = QtGui.QFrame()

      frameLayout = QtGui.QVBoxLayout ()
      frameLayout.setSpacing ( UI.SPACING )
      frameLayout.setMargin ( 0 ) # UI.SPACING )
      frameLayout.setAlignment ( QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft )

      frame.setLayout( frameLayout )

      if self.param.type in self.paramWidgets.keys () :
        print '>> Create %s param widget' % self.param.type

        # create paramWidget without GfxNode and ignoreSubtype = True
        self.ui.value_widget = apply ( self.paramWidgets [ self.param.type ], [ self.param, None, True ] )
        self.ui.value_widget.label.setText ( 'Current Value' )

        frameLayout.addWidget ( self.ui.value_widget )
        
        self.ui.def_value_widget = apply ( self.paramWidgets [ self.param_default.type ], [ self.param_default, None, True ] )
        self.ui.def_value_widget.label.setText ( 'Default Value' )

        frameLayout.addWidget ( self.ui.def_value_widget )

      self.ui.value_stackedWidget.addWidget ( frame )
      self.connectSignals ()
    else :
      self.reset ()
  #
  # onEditParamName
  #
  def onEditParamName ( self ) :
    #
    # !!! ListWidget item for param also should be changed
    #
    newName = str ( self.ui.name_lineEdit.text () ).strip ()
    if newName == '' :
      newName = self.param.name
      self.ui.name_lineEdit.setText ( self.param.name )
    if newName != self.param.name :
      self.emit( QtCore.SIGNAL ( 'changeParamName' ), self.param.name, newName )
  #
  # onEditParamLabel
  #
  def onEditParamLabel ( self ) :
    #
    newName  = str ( self.ui.label_lineEdit.text () ).strip ()
    if newName == '' :
      newName = self.param.label
      self.ui.label_lineEdit.setText ( self.param.label )
    if newName != self.param.label :
      self.emit( QtCore.SIGNAL ( 'changeParamLabel' ), self.param.label, newName )
  #
  #
  #
  def onEditParamEnabled ( self, value ) : self.param.enabled = self.ui.check_enabled.isChecked ()
  def onEditParamDisplay ( self, value ) : self.param.display = self.ui.check_display.isChecked ()
  def onEditParamShader ( self, value )  : self.param.shaderParam = self.ui.check_shader.isChecked ()
  def onEditParamType ( self, idx ) :
    #
    # !!! UI for param.value and param.default also should be changed
    #
    self.param.type = str ( self.ui.type_comboBox.itemText ( idx ) )

  def onEditParamDetail ( self, idx )   : self.param.detail = str ( self.ui.detail_comboBox.itemText ( idx ) )
  def onEditParamProvider ( self, idx ) : self.param.provider = str ( self.ui.provider_comboBox.itemText ( idx ) )
  def onEditParamSubtype ( self, idx )  : self.param.subtype = str ( self.ui.subtype_comboBox.itemText ( idx ) )
  def onEditParamRange ( self )         : self.param.range = str ( self.ui.range_lineEdit.text () )
  def onEditParamHelp ( self )          : self.param.help = str ( self.ui.descr_plainTextEdit.toPlainText () )
