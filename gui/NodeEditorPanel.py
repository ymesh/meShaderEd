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
from PyQt4 import Qt, QtCore, QtGui, QtXml

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
  def __init__ ( self, node = None ):
    QtGui.QDialog.__init__ ( self )

    self.editNode = None
    
    self.nodeEditor = None
    self.nodeParamEditor = None

    self.nodeCodeEditor = None
    self.paramCodeEditor = None
          
    #self.debugPrint()
    self.buildGui ()
    self.setEditNode ( node )

    self.ui.btn_save.setDefault ( False )
    self.ui.btn_close.setDefault ( True )
    self.updateGui ()
  #
  #
  def connectSignals ( self ) :
    QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL( "selectionChanged" ), self.updateGui ) # onInputParamSelectionChanged )
    QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL( "selectionChanged" ), self.updateGui ) # onOutputParamSelectionChanged  )
    
    QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL( "addItem" ), self.onAddParam )
    QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL( "addItem" ), self.onAddParam )
    QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL( "renameItem" ), self.onRenameParam )
    QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL( "renameItem" ), self.onRenameParam )
    QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL( "removeItem" ), self.onRemoveParam )
    QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL( "removeItem" ), self.onRemoveParam )
    
    QtCore.QObject.connect ( self.ui.tabs_param_list, QtCore.SIGNAL( "currentChanged(int)" ), self.updateGui )
    
    if self.nodeParamEditor is not None :
      QtCore.QObject.connect ( self.nodeParamEditor, QtCore.SIGNAL( "changeParamName" ), self.onRenameParam )
      QtCore.QObject.connect ( self.nodeParamEditor, QtCore.SIGNAL( "changeParamLabel" ), self.onRenameParamLabel )
      
    if self.nodeCodeEditor is not None :
      QtCore.QObject.connect ( self.nodeCodeEditor.ui.textEdit, QtCore.SIGNAL( 'textChanged()' ), self.onEditCode )
    
    if self.paramCodeEditor is not None :
      QtCore.QObject.connect ( self.paramCodeEditor.ui.textEdit, QtCore.SIGNAL( 'textChanged()' ), self.onEditParamCode)
    
    QtCore.QObject.connect ( self.ui.internals_list, QtCore.SIGNAL( "addItem" ), self.onAddInternal )
    QtCore.QObject.connect ( self.ui.includes_list, QtCore.SIGNAL( "addItem" ), self.onAddInclude )
    
    QtCore.QObject.connect ( self.ui.internals_list, QtCore.SIGNAL( "renameItem" ), self.onRenameInternal )
    QtCore.QObject.connect ( self.ui.includes_list, QtCore.SIGNAL( "renameItem" ), self.onRenameInclude )
    
    QtCore.QObject.connect ( self.ui.internals_list, QtCore.SIGNAL( "removeItem" ), self.onRemoveInternal )
    QtCore.QObject.connect ( self.ui.includes_list, QtCore.SIGNAL( "removeItem" ), self.onRemoveInclude )
  
  def disconnectSignals ( self ) :
    QtCore.QObject.disconnect ( self.ui.input_list, QtCore.SIGNAL( "selectionChanged" ), self.updateGui ) # onInputParamSelectionChanged )
    QtCore.QObject.disconnect ( self.ui.output_list, QtCore.SIGNAL( "selectionChanged" ), self.updateGui ) # onOutputParamSelectionChanged  )
    QtCore.QObject.disconnect ( self.ui.input_list, QtCore.SIGNAL( "addItem" ), self.onAddParam )
    QtCore.QObject.disconnect ( self.ui.output_list, QtCore.SIGNAL( "addItem" ), self.onAddParam )
    QtCore.QObject.disconnect ( self.ui.input_list, QtCore.SIGNAL( "renameItem" ), self.onRenameParam )
    QtCore.QObject.disconnect ( self.ui.output_list, QtCore.SIGNAL( "renameItem" ), self.onRenameParam )
    QtCore.QObject.disconnect ( self.ui.input_list, QtCore.SIGNAL( "removeItem" ), self.onRemoveParam )
    QtCore.QObject.disconnect ( self.ui.output_list, QtCore.SIGNAL( "removeItem" ), self.onRemoveParam )

    QtCore.QObject.disconnect ( self.ui.tabs_param_list, QtCore.SIGNAL( "currentChanged(int)" ), self.updateGui )
    
    if self.nodeParamEditor is not None :
      QtCore.QObject.disconnect ( self.nodeParamEditor, QtCore.SIGNAL( "changeParamName" ), self.onRenameParam )
      QtCore.QObject.disconnect ( self.nodeParamEditor, QtCore.SIGNAL( "changeParamLabel" ), self.onRenameParamLabel )
      
    if self.nodeCodeEditor is not None :
      QtCore.QObject.disconnect ( self.nodeCodeEditor.ui.textEdit, QtCore.SIGNAL( 'textChanged()' ), self.onEditCode )
    
    if self.paramCodeEditor is not None :
      QtCore.QObject.disconnect ( self.paramCodeEditor.ui.textEdit, QtCore.SIGNAL( 'textChanged()' ), self.onEditParamCode)


    QtCore.QObject.disconnect ( self.ui.internals_list, QtCore.SIGNAL( "addItem" ), self.onAddInternal )
    QtCore.QObject.disconnect ( self.ui.includes_list, QtCore.SIGNAL( "addItem" ), self.onAddInclude )
    
    QtCore.QObject.disconnect ( self.ui.internals_list, QtCore.SIGNAL( "renameItem" ), self.onRenameInternal )
    QtCore.QObject.disconnect ( self.ui.includes_list, QtCore.SIGNAL( "renameItem" ), self.onRenameInclude )
    
    QtCore.QObject.disconnect ( self.ui.internals_list, QtCore.SIGNAL( "removeItem" ), self.onRemoveInternal )
    QtCore.QObject.disconnect ( self.ui.includes_list, QtCore.SIGNAL( "removeItem" ), self.onRemoveInclude )
  #
  #
  def setupInputParams () :
    pass    
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
    if DEBUG_MODE : print '>> NodeEditorPanel::onToolBoxIndexChanged (idx = %d)' % idx
    # 
    self.disconnectSignals ()   
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
        
        self.ui.tab_code = self.ui.code_tabs.addTab ( self.nodeCodeEditor, 'Node Code' )
        self.ui.tab_code = self.ui.code_tabs.addTab ( self.paramCodeEditor, 'Control Code' )
        
        self.ui.code_tabs.setCurrentIndex ( 0 ) 
        self.ui.side_stackedWidget.addWidget ( self.ui.code_tabs )
      
      self.connectSignals ()      
      self.updateGui ()
  #
  #
  def onInputParamSelectionChanged ( self, paramName ) :
    if DEBUG_MODE : print '>> NodeEditorPanel::onInputParamSelectionChanged (%s)' % paramName
    param = self.editNode.getInputParamByName( str( paramName ) ) 
    self.nodeParamEditor.setParam ( param )
  #
  #
  def onOutputParamSelectionChanged ( self, paramName ) :
    if DEBUG_MODE : print '>> NodeEditorPanel::onOutputParamSelectionChanged (%s)' % paramName
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
  #
  def onRemoveInternal ( self, internal ) :
    internalsListWidget = self.ui.internals_list.ui.listWidget
    self.editNode.internals.remove ( internal )
    item = internalsListWidget.currentItem()
    internalsListWidget.takeItem ( internalsListWidget.currentRow () )
    internalsListWidget.removeItemWidget ( item )
    internalsListWidget.clearSelection ()
    internalsListWidget.setCurrentItem ( None )
  #
  #
  #
  def onRemoveInclude ( self, include ) :
    includesListWidget = self.ui.includes_list.ui.listWidget
    self.editNode.includes.remove ( include )
    item = includesListWidget.currentItem()
    includesListWidget.takeItem ( includesListWidget.currentRow () )
    includesListWidget.removeItemWidget ( item )
    includesListWidget.clearSelection ()
    includesListWidget.setCurrentItem ( None )
  #
  #
  #
  def onRemoveParam ( self, paramName ) :
    isInputParam = False
    tab_idx = self.ui.tabs_param_list.currentIndex()
    if tab_idx == 0 : isInputParam = True
    param = None
    paramList = None
    if isInputParam :
      param = self.editNode.getInputParamByName ( paramName )
      paramList = self.ui.input_list
    else :
      param = self.editNode.getOutputParamByName ( paramName )
      paramList = self.ui.output_list
    
    self.editNode.removeParam ( param )
    
    item = paramList.ui.listWidget.currentItem()
    paramList.ui.listWidget.takeItem ( paramList.ui.listWidget.currentRow () )
    paramList.ui.listWidget.removeItemWidget ( item )
    paramList.ui.listWidget.clearSelection ()
    paramList.ui.listWidget.setCurrentItem ( None )
  #
  #
  #
  def onRenameInternal ( self, oldName, newName ) :
    internalsListWidget = self.ui.internals_list.ui.listWidget
    from core.meCommon import getUniqueName
    idx = self.editNode.internals.index ( oldName )
    newName = getUniqueName ( newName, self.editNode.internals ) 
    self.editNode.internals[ idx ] = newName
    
    item = internalsListWidget.findItems( oldName, QtCore.Qt.MatchExactly )[0]
    item.setText ( newName )
    self.ui.internals_list.setName ( newName )
    internalsListWidget.clearSelection ()
    internalsListWidget.setCurrentItem ( item ) 
  #
  #
  #
  def onRenameInclude ( self, oldName, newName ) :
    includesListWidget = self.ui.includes_list.ui.listWidget
    from core.meCommon import getUniqueName
    idx = self.editNode.includes.index ( oldName )
    newName = getUniqueName ( newName, self.editNode.includes ) 
    self.editNode.includes[ idx ] = newName
    
    item = includesListWidget.findItems( oldName, QtCore.Qt.MatchExactly )[0]
    item.setText ( newName )
    self.ui.includes_list.setName ( newName )
    includesListWidget.clearSelection ()
    includesListWidget.setCurrentItem ( item ) 
  #
  #
  #
  def onRenameParam ( self, oldName, newName ) :
    isInputParam = False
    tab_idx = self.ui.tabs_param_list.currentIndex()
    if tab_idx == 0 : isInputParam = True
    param = None
    paramList = None
    if isInputParam :
      param = self.editNode.getInputParamByName ( oldName )
      paramList = self.ui.input_list
    else :
      param = self.editNode.getOutputParamByName ( oldName )
      paramList = self.ui.output_list
    
    self.editNode.renameParamName ( param, newName )
    
    item = paramList.ui.listWidget.findItems( oldName, QtCore.Qt.MatchExactly )[0]
    item.setText ( param.name )
    paramList.setName ( param.name )
    paramList.ui.listWidget.clearSelection ()
    paramList.ui.listWidget.setCurrentItem ( item ) 
  #
  #
  #
  def onRenameParamLabel ( self, oldName, newName ) :
    param = self.nodeParamEditor.param
    self.editNode.renameParamLabel ( param, newName )
    self.nodeParamEditor.ui.label_lineEdit.setText ( param.label )
  #
  #
  #
  def onAddInternal ( self, newName ) :
    if DEBUG_MODE : print '>> NodeEditorPanel::onAddInternal (%s) ' % (newName) 
    # name can be changed to be unique
    newName = self.editNode.addInternal ( newName )  
    internalsListWidget = self.ui.internals_list.ui.listWidget
    internalsListWidget.addItem ( newName )
    internalsListWidget.setCurrentItem ( internalsListWidget.findItems( newName, QtCore.Qt.MatchExactly )[0] ) 
  #
  #
  #
  def onAddInclude ( self, newName ) :
    if DEBUG_MODE : print '>> NodeEditorPanel::onAddInclude (%s) ' % (newName)  
    # name can be changed to be unique
    newName = self.editNode.addInclude ( newName )  
    includesListWidget = self.ui.includes_list.ui.listWidget
    includesListWidget.addItem ( newName )
    includesListWidget.setCurrentItem ( includesListWidget.findItems( newName, QtCore.Qt.MatchExactly )[0] ) 
  #
  #
  #
  def onAddParam ( self, newName ) :
    if DEBUG_MODE : print '>> NodeEditorPanel::onAddParam (%s) ' % (newName) 
    isInputParam = False
    paramType = None
    isRibParam = ( self.editNode.type == 'rib' or self.editNode.type == 'rib_code' )
    tab_idx = self.ui.tabs_param_list.currentIndex()
    if tab_idx == 0 : isInputParam = True
    # ask user about param type
    typeDialog = QtGui.QDialog () # Qt.MSWindowsFixedSizeDialogHint 
    typeDialog.setModal ( True )

    typeDialog.setWindowTitle ( 'Parameter Type' )
    typeDialog.resize (180, 100 )
    sizePolicy = QtGui.QSizePolicy ( QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed )
    sizePolicy.setHorizontalStretch ( 0 )
    sizePolicy.setVerticalStretch ( 0 )
    sizePolicy.setHeightForWidth ( typeDialog.sizePolicy().hasHeightForWidth() )
    typeDialog.setSizePolicy ( sizePolicy )
    typeDialog.setSizeGripEnabled ( False )
    
    typeDialog.verticalLayout = QtGui.QVBoxLayout ( typeDialog )
    typeDialog.verticalLayout.setSizeConstraint ( QtGui.QLayout.SetMinimumSize )
    typeDialog.type_comboBox = QtGui.QComboBox ( typeDialog )
    for label in [ 'float', 'int', 'color', 'string', 'normal', 'point', 'vector', 'matrix', 
                   'surface', 'displacement', 'volume', 'light', 
                   'rib', 'text', 'transform','image'  ]  :
      typeDialog.type_comboBox.addItem ( label )
    typeDialog.verticalLayout.addWidget ( typeDialog.type_comboBox )
    
    typeDialog.btnBox = QtGui.QDialogButtonBox ( QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, parent = typeDialog )
    typeDialog.btnBox.setCenterButtons ( True )
    typeDialog.verticalLayout.addWidget ( typeDialog.btnBox )
           
    QtCore.QObject.connect ( typeDialog.btnBox, QtCore.SIGNAL('accepted()'), typeDialog.accept )
    QtCore.QObject.connect ( typeDialog.btnBox, QtCore.SIGNAL('rejected()'), typeDialog.reject )
    
    if typeDialog.exec_() == QtGui.QDialog.Accepted  :
      paramType = str ( typeDialog.type_comboBox.currentText () )
      if DEBUG_MODE : print '>> NodeEditorPanel::onAddParam typeDialog Accepted (%s)' % paramType
      # create empty xml node parameter
      dom = QtXml.QDomDocument ( newName )
      xmlnode = dom.createElement( "property" )
  
      xmlnode.setAttribute ( "name", newName )
      xmlnode.setAttribute ( "label", newName )
      xmlnode.setAttribute ( "type", paramType )
      param = createParamFromXml ( xmlnode, isRibParam, isInputParam )
      item = QtGui.QListWidgetItem( param.name )  
      
      paramListWidget = self.ui.input_list.ui.listWidget
      if isInputParam :
        self.editNode.addInputParam ( param )
      else :
        self.editNode.addOutputParam ( param )
        paramListWidget = self.ui.output_list.ui.listWidget
        
      paramListWidget.addItem ( param.name )
      paramListWidget.setCurrentItem ( paramListWidget.findItems( param.name, QtCore.Qt.MatchExactly )[0] )
      #self.nodeParamEditor.setParam ( param )
  #
  #
  #
  def onEditCode ( self ) :
    if DEBUG_MODE : print '>> NodeEditorPanel::onEditCode'
    if self.nodeCodeEditor is not None :
      #self.nodeCodeEditor.ui.textEdit
      self.editNode.code = str ( self.nodeCodeEditor.ui.textEdit.toPlainText () )
  #
  #
  #
  def onEditParamCode ( self ) :
    if DEBUG_MODE : print '>> NodeEditorPanel::onEditParamCode'
    if self.paramCodeEditor is None :
      #self.paramCodeEditor.ui.textEdit
      self.editNode.param_code = str ( self.paramCodeEditor.ui.textEdit.toPlainText () )
  #
  # Ignore default Enter press event
  #
  def keyPressEvent ( self, event  ) :
    #if DEBUG_MODE : print '>> NodeEditorPanel::keyPressEvent' 
    if  event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
      event.ignore()
    else:
      QtGui.QDialog.keyPressEvent ( self, event )  
  #
  #  
  def accept ( self ) :
    if DEBUG_MODE : print '>> NodeEditorPanel::accept'  
    self.done ( QtGui.QDialog.Accepted )
