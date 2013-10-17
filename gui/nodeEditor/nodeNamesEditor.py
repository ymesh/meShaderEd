#===============================================================================
# nodeNamesEditor.py.py
#
# ver. 1.0.0
# Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
# 
# Widget for manage names in list
# 
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

#from core.meCommon import *
from global_vars import app_global_vars, DEBUG_MODE

from ui_nodeNamesEditor import Ui_NodeNamesEditor
#
# NodeNamesEditor
#
class NodeNamesEditor ( QtGui.QWidget ) :
  #
  # __init__
  #
  def __init__ ( self, parent ) :
    #
    QtGui.QWidget.__init__ ( self, parent )
    self.saved_text = ''
    self.approvedNewName = ''
    self.buildGui ()
  #
  # buildGui
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_NodeNamesEditor ( )
    self.ui.setupUi ( self )
  #
  # setName
  #
  def setName ( self, newName ) :
    #
    if newName == '' :
      if self.saved_text != '' :
        newName = self.saved_text

    self.ui.name_lineEdit.setText ( newName )
    self.saved_text = newName     
  #
  # onAddItem
  #
  def onAddItem ( self ) :
    #
    if DEBUG_MODE : print '>> NodeNamesEditor: onAddItem'
    new_text = str ( self.ui.name_lineEdit.text () ).strip ()
    if new_text != '' :
      self.emit ( QtCore.SIGNAL ( 'addItem' ), new_text ) 
  #  
  # onRemoveItem
  #
  def onRemoveItem ( self ) :
    #
    if DEBUG_MODE : print '>> NodeNamesEditor::onRemoveItem'
    list_item = self.ui.listWidget.currentItem ()
    
    if list_item is not None :
      item_text = str ( list_item.text () )
      #self.ui.listWidget.takeItem ( self.ui.listWidget.currentRow () )
      #self.ui.listWidget.removeItemWidget ( list_item )
      self.emit ( QtCore.SIGNAL ( 'removeItem' ), item_text )
  #
  # onRenameItem
  #
  def onRenameItem ( self ) :
    #
    if DEBUG_MODE : print '>> NodeNamesEditor::onRenameItem'
    new_text = str ( self.ui.name_lineEdit.text () ).strip ()
    
    if new_text == '' :
      if self.saved_text != '' :
        new_text = self.saved_text
        self.ui.name_lineEdit.setText ( new_text )  
            
    list_item = self.ui.listWidget.currentItem ()
    
    if list_item is not None : # e.g. listWidget is not empty
      old_text = list_item.text ()
      if new_text != old_text :
        self.emit ( QtCore.SIGNAL( 'renameItem' ), old_text, new_text )
      else :  
        self.ui.listWidget.clearSelection ()
        self.ui.listWidget.setCurrentItem ( None )
  #    
  # onSelectionChanged
  #
  def onSelectionChanged ( self ) :
    #
    if DEBUG_MODE : print '>> NodeNamesEditor::onSelectionChanged'
    list_item = self.ui.listWidget.currentItem ()
    
    if list_item is not None :
      self.saved_text = str ( list_item.text() )
      self.ui.name_lineEdit.setText ( self.saved_text  )
      self.emit ( QtCore.SIGNAL ( 'selectionChanged' ), self.saved_text  )   
