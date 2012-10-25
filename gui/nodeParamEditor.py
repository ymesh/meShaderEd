#===============================================================================
# nodeParamEditor.py
#
# ver. 1.0.0
# Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
# 
# Dialog for managing node 
# 
#===============================================================================
import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars
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

from ui_nodeParamEditor import Ui_NodeParamEditor
#
#
#
class NodeParamEditor ( QtGui.QWidget ):
  #
  #
  def __init__ ( self, parent ):
    QtGui.QDialog.__init__ ( self )
    self.param = None
    self.param_default = None
    self.paramWidgets = { 'string' : StringWidget
                          ,'image' : StringWidget
                          ,'rib' : StringWidget
                          ,'surface' : StringWidget 
                          ,'displacement' : StringWidget 
                          ,'light' : StringWidget  
                          ,'volume' : StringWidget
                          ,'float' : FloatWidget
                          ,'int' : IntWidget
                          ,'color' : ColorWidget
                          ,'normal' : NormalWidget
                          ,'transform' : PointWidget
                          ,'point' : PointWidget
                          ,'vector' : VectorWidget
                          ,'matrix' : MatrixWidget
                        }
                        
    self.buildGui()
  #
  #
  def __delete__ ( self, obj ) :
    print '* NodeParamEditor closed... %s' % str( obj )

  #
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_NodeParamEditor ( )
    self.ui.setupUi ( self )
    
    # correct UI sizes for some controls
    self.ui.check_display.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    self.ui.check_display.setMaximumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    
    self.ui.check_shader.setMinimumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) )
    self.ui.check_shader.setMaximumSize ( QtCore.QSize ( UI.CHECK_WIDTH, UI.HEIGHT ) ) 
    
    for label in [ 'float', 'int', 'color', 'string', 'normal', 'point', 'vector', 'matrix', 
                   'surface', 'displacement', 'volume', 'light', 
                   'rib', 'text', 'transform','image'  ]  :
      self.ui.type_comboBox.addItem ( label )
    self.ui.type_comboBox.setCurrentIndex ( -1 )
    self.ui.type_comboBox.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.ui.type_comboBox.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
    
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
    
    for label in [ 'None', 'slider', 'switch', 'selector', 'file' ]  :
      self.ui.subtype_comboBox.addItem ( label )
    self.ui.subtype_comboBox.setCurrentIndex ( -1 )
    self.ui.subtype_comboBox.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    self.ui.subtype_comboBox.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
  #
  # As paramWidet is monitoring a change of param.value only,
  # we need to cynchronize changing of param_default.value with param.default  
  #
  def onParamDefValueChanged ( self, param ) :
    print '* onParamDefValueChanged'
    self.param.default = self.param_default.value
  #
  #
  def onParamValueChanged ( self, param ) :
    print '* onParamValueChanged'
    self.param.value = param.value
  #
  #
  def connectSignals ( self ) :
    #
    self.connect ( self.param_default, QtCore.SIGNAL( 'paramChanged(QObject)' ), self.onParamDefValueChanged )
    #
    self.connect ( self.ui.name_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrName  )
    self.connect ( self.ui.label_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrLabel  )
  #
  #
  def disconnectSignals ( self ) :
    if self.param_default is not None :
      self.disconnect ( self.param_default, QtCore.SIGNAL( 'paramChanged(QObject)' ), self.onParamDefValueChanged )
    if self.param is not None :
      self.disconnect ( self.ui.name_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrName )
      self.disconnect ( self.ui.label_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrLabel )
  #
  #
  def reset ( self ) :  
    self.ui.name_lineEdit.setText ( '' ) 
    self.ui.label_lineEdit.setText ( '' )
    self.ui.check_display.setChecked ( False )
    self.ui.check_shader.setChecked ( False )

    self.ui.type_comboBox.setCurrentIndex( -1 )
    self.ui.detail_comboBox.setCurrentIndex ( -1 )
    self.ui.provider_comboBox.setCurrentIndex ( -1 )
    self.ui.subtype_comboBox.setCurrentIndex ( -1 )
    self.ui.range_lineEdit.setText ( '' ) 
    
    doc = QtGui.QTextDocument ()
    doc.setPlainText ( '' )
    layout = QtGui.QPlainTextDocumentLayout( doc )
    doc.setDocumentLayout( layout )
    self.ui.descr_plainTextEdit.setDocument ( doc )  
  #
  # Remove stackedWidget's layout every time,
  # when current parameter (or it's type) is changing
  #
  def removeValueWidget ( self ) :
    while True :
      currentWidget = self.ui.value_stackedWidget.currentWidget ()
      if currentWidget is not None :
        #print '> removeWidget: %s' % str( currentWidget )
        self.ui.value_stackedWidget.removeWidget ( currentWidget )
      else :
        break
  #
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
      self.ui.check_display.setChecked ( self.param.display )
      self.ui.check_shader.setChecked ( self.param.shaderParam )

      self.ui.type_comboBox.setCurrentIndex( self.ui.type_comboBox.findText ( self.param.type ) )
      self.ui.detail_comboBox.setCurrentIndex( self.ui.detail_comboBox.findText ( self.param.detail ) )
      self.ui.provider_comboBox.setCurrentIndex( self.ui.provider_comboBox.findText ( self.param.provider ) )
      self.ui.subtype_comboBox.setCurrentIndex( self.ui.subtype_comboBox.findText ( self.param.subtype ) )
      self.ui.range_lineEdit.setText ( self.param.range ) 
      
      doc = QtGui.QTextDocument ()
      help_text = ''
      if self.param.help != None : 
        help_text = self.param.help  
      
      doc.setPlainText ( help_text )
      layout = QtGui.QPlainTextDocumentLayout( doc )
      doc.setDocumentLayout( layout )
        
      self.ui.descr_plainTextEdit.setDocument ( doc ) 
      
      frame = QtGui.QFrame()
        
      frameLayout = QtGui.QVBoxLayout ()
      frameLayout.setSpacing ( UI.SPACING )
      frameLayout.setMargin ( 0 ) # UI.SPACING )
      frameLayout.setAlignment ( QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft )
      
      frame.setLayout( frameLayout )
    
      if self.param.type in self.paramWidgets.keys() :
        print '>> Create %s param widget' % self.param.type
        
        # create paramWidget without GfxNode and ignoreSubtype = True
        self.ui.value_widget = apply ( self.paramWidgets [ self.param.type ], [ self.param, None, self, True ] )
        
        self.ui.value_widget.label.setText ( 'Current Value' ) 
        self.ui.value_widget.label.setMinimumSize ( QtCore.QSize ( 100, UI.HEIGHT ) )
        self.ui.value_widget.label.setMaximumSize ( QtCore.QSize ( 100, UI.HEIGHT ) )
    
        frameLayout.addWidget ( self.ui.value_widget ) 
        
        self.ui.def_value_widget = apply ( self.paramWidgets [ self.param_default.type ], [ self.param_default, None, self, True ] )
        
        self.ui.def_value_widget.label.setText ( 'Default Value' ) 
        self.ui.def_value_widget.label.setMinimumSize ( QtCore.QSize ( 100, UI.HEIGHT ) )
        self.ui.def_value_widget.label.setMaximumSize ( QtCore.QSize ( 100, UI.HEIGHT ) )
    
        frameLayout.addWidget ( self.ui.def_value_widget ) 
        
      self.ui.value_stackedWidget.addWidget ( frame )
      self.connectSignals()  
    else :
      self.reset ()
  #
  #
  def onEditNodeStrAttrName ( self ) : self.param.name = str ( self.ui.name_lineEdit.text () )
  def onEditNodeStrAttrLabel ( self ) : self.param.label = str ( self.ui.label_lineEdit.text () )