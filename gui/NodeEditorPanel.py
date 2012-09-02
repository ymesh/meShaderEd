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
from global_vars import app_global_vars

import gui.ui_settings as UI

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
  def __init__ ( self, parent ):
    QtGui.QDialog.__init__(self)

    self.editNode = None
          
    #self.debugPrint()
    self.buildGui ()
    self.updateGui ()
  #
  #
  def setEditNode ( self, editNode ): 
    print '>> NodeEditorPanel: setEditNode'
    self.editNode = editNode 
    
    item = QtGui.QListWidgetItem( editNode.name )
    self.ui.nodes_listWidget.addItem( item )
    
    self.updateGui ()
    
  #
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_NodeEditorPanel ( )
    self.ui.setupUi ( self )
    
    

  #
  #
  def updateGui ( self ):
    #  
    toolBoxIdx = self.ui.toolBox.currentIndex()
    
    print '>> NodeEditorPanel: toolBoxIdx = %d' % toolBoxIdx
    
    currentWidget = self.ui.side_stackedWidget.currentWidget ()
    self.ui.side_stackedWidget.removeWidget ( currentWidget )
    
    #frame = QtGui.QFrame()
        
    #frameLayout = QtGui.QVBoxLayout ()
    #frameLayout.setSpacing ( UI.SPACING )
    #frameLayout.setMargin ( UI.SPACING )
    #frameLayout.setAlignment ( QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft )
    
    #frame.setLayout( frameLayout )
    #frameLayout.addItem ( nodeEditor )
    
    # Node
    if toolBoxIdx == 0 :  
      nodeEditor = NodeEditor( self, self.editNode )
      self.ui.side_stackedWidget.addWidget ( nodeEditor )
    # Input, Output Parameters
    elif toolBoxIdx == 1 or toolBoxIdx == 2 : # Input Parameters
      nodeParamEditor = NodeParamEditor( self )
      self.ui.side_stackedWidget.addWidget ( nodeParamEditor )
    # Includes, Local Names   
    elif toolBoxIdx == 3 or toolBoxIdx == 4 : # Includes
      nodeNamesEditor = NodeNamesEditor( self )
      self.ui.side_stackedWidget.addWidget ( nodeNamesEditor )
    elif toolBoxIdx == 5 : # Code
      currentCodeItem = self.ui.code_listWidget.currentItem()
      editNode = None
      codeType = None
      if currentCodeItem is not None :
        editNode = self.editNode
        codeType = currentCodeItem.text ()
        # print 'currentCodeItem = ' + str( codeType )
      nodeCodeEditor = NodeCodeEditor( self, editNode, str( codeType ) )
      self.ui.side_stackedWidget.addWidget ( nodeCodeEditor )
    
    
  #
  #
  def onToolBoxIndexChanged ( self, idx ) :
    #print '>> NodeEditorPanel: onToolBoxIndexChanged idx = %d' % idx
    
    if idx != -1 : self.updateGui ()
    