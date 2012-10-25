#===============================================================================
# NodeEditorPanel.py
#
# ver. 1.0.0
# Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
# 
# Dialog for managing node code and parameters
# 
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI

from core.nodeNetwork import *

from nodeEditor import NodeEditor
from nodeNamesEditor import NodeNamesEditor
from nodeParamEditor import NodeParamEditor
from nodeCodeEditor import NodeCodeEditor

from ui_nodeEditorPanel import Ui_NodeEditorPanel
#
#
#
class NodeEditorPanel ( QtGui.QDialog ):
  #
  #
  def __init__ ( self, xml_node = None ):
    QtGui.QDialog.__init__ ( self )

    self.editNode = createNodeFromXML ( xml_node ) 
    
    self.nodeEditor = None
    self.nodeParamEditor = None

    self.nodeCodeEditor = None
    self.paramCodeEditor = None
          
    #self.debugPrint()
    self.buildGui ()
    self.setEditNode ( self.editNode )
    self.updateGui ()
  #
  #
  def connectSignals ( self ) :
    QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL( "selectionChanged" ), self.updateGui ) # onInputParamSelectionChanged )
    QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL( "selectionChanged" ), self.updateGui ) # onOutputParamSelectionChanged  )
    QtCore.QObject.connect ( self.ui.tabs_param_list, QtCore.SIGNAL( "currentChanged(int)" ), self.updateGui )
  # 
  #
  def setEditNode ( self, editNode ): 
    if DEBUG_MODE : print '>> NodeEditorPanel: setEditNode'
    self.editNode = editNode 
    
    for name in editNode.internals :
      item = QtGui.QListWidgetItem( name )  
      self.ui.internals_list.ui.listWidget.addItem( item )
      
    for name in editNode.includes :
      item = QtGui.QListWidgetItem( name )  
      self.ui.includes_list.ui.listWidget.addItem( item )
      
    for param in editNode.inputParams :
      item = QtGui.QListWidgetItem( param.name )  
      self.ui.input_list.ui.listWidget.addItem( param.name )
      
    for param in editNode.outputParams :
      item = QtGui.QListWidgetItem( param.name )  
      self.ui.output_list.ui.listWidget.addItem( param.name )
      
    item = QtGui.QListWidgetItem( editNode.name )
    self.ui.nodes_listWidget.addItem( item )
    
    self.connectSignals()
    
    #self.updateGui ()
    self.ui.toolBox.setCurrentIndex( 0 )
  #
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_NodeEditorPanel ( )
    self.ui.setupUi ( self )
    self.ui.code_tabs = QtGui.QTabWidget( self.ui.side_stackedWidget )
    self.ui.code_tabs.setVisible ( False )
  #
  #
  def updateGui ( self ):
    #  
    if self.editNode is not None :
      idx = self.ui.toolBox.currentIndex()
      
      if idx == 1 :  # Parameters
        tab_idx = self.ui.tabs_param_list.currentIndex()
        param = None
        if tab_idx == 0 : #input parameters
          list_item = self.ui.input_list.ui.listWidget.currentItem()
          if list_item is not None :
            param = self.editNode.getInputParamByName( str( list_item.text() ) )
        elif tab_idx == 1 : # output parametrs
          list_item = self.ui.output_list.ui.listWidget.currentItem()
          if list_item is not None :
            param = self.editNode.getOutputParamByName( str( list_item.text() ) )
        self.nodeParamEditor.setParam ( param )
      elif idx == 2 : # Code
        self.ui.code_tabs.setVisible ( True )
  #
  #
  def onToolBoxIndexChanged ( self, idx ) :
    print 'onToolBoxIndexChanged (idx = %d)' % idx
    #    
    if idx != -1 :
      currentWidget = self.ui.side_stackedWidget.currentWidget ()
      self.ui.side_stackedWidget.removeWidget ( currentWidget )
      # Node
      if idx == 0 :  
        if self.nodeEditor is None :
          self.nodeEditor = NodeEditor( self )
        self.nodeEditor.setNode( self.editNode )
        self.ui.side_stackedWidget.addWidget ( self.nodeEditor )
      # Input, Output Parameters
      elif idx == 1  : # Parameters
        if self.nodeParamEditor is None :
          self.nodeParamEditor = NodeParamEditor( self )
        self.ui.side_stackedWidget.addWidget ( self.nodeParamEditor )
      # Includes, Local Names   
      elif idx == 2 : # Code
        if self.nodeCodeEditor is None :
          self.nodeCodeEditor = NodeCodeEditor( self )
        if self.paramCodeEditor is None :
          self.paramCodeEditor = NodeCodeEditor( self )
        
        self.nodeCodeEditor.setNodeCode ( self.editNode.code, 'SL' )
        self.paramCodeEditor.setNodeCode ( self.editNode.param_code, 'python' )
        
        self.ui.tab_code = self.ui.code_tabs.addTab ( self.nodeCodeEditor, 'Code' )
        self.ui.tab_code = self.ui.code_tabs.addTab ( self.paramCodeEditor, 'Control Code' )
        
        self.ui.code_tabs.setCurrentIndex ( 0 ) 
        self.ui.side_stackedWidget.addWidget ( self.ui.code_tabs )
       
      self.updateGui ()
  #
  #
  def onInputParamSelectionChanged ( self, paramName ) :
    if DEBUG_MODE : print '>> NodeEditorPanel: onInputParamSelectionChanged (%s)' % paramName
    param = self.editNode.getInputParamByName( str( paramName ) ) 
    self.nodeParamEditor.setParam ( param )
  #
  #
  def onOutputParamSelectionChanged ( self, paramName ) :
    if DEBUG_MODE : print '>> NodeEditorPanel: onOutputParamSelectionChanged (%s)' % paramName
    param = self.editNode.getOutputParamByName( str( paramName ) ) 
    self.nodeParamEditor.setParam ( param )  
  #
  #
  def onCodeListIndexChanged ( self, idx ) :
    # if DEBUG_MODE : print '>> NodeEditorPanel: onCodeListIndexChanged idx = %d' % idx
    self.updateGui ()
    #if idx != -1 : 
    #  currentCodeItem = self.ui.code_listWidget.currentItem()
    #  codeType = str( currentCodeItem.text () )
    #  if codeType == 'param_code' :
    #    self.nodeCodeEditor.setNodeCode ( self.editNode.param_code, 'python' )
    #  elif codeType == 'code' :
    #    self.nodeCodeEditor.setNodeCode ( self.editNode.code, 'SL' )
  #
  #  
  def accept ( self ) :
    print '>> NodeEditorPanel: accept'  
    self.done ( QtGui.QDialog.Accepted )
