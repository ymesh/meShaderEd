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

from core.meCommon import *
from global_vars import app_global_vars, DEBUG_MODE

from ui_nodeNamesEditor import Ui_NodeNamesEditor
#
#
#
class NodeNamesEditor ( QtGui.QWidget ):
  #
  #
  def __init__ ( self, parent ):
    QtGui.QDialog.__init__ ( self )
    self.saved_text = ''
    self.buildGui()
  #
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_NodeNamesEditor ( )
    self.ui.setupUi ( self )
    
  #
  #
  def onAddItem ( self ) :
    if DEBUG_MODE : print '>> NodeNamesEditor: onAddItem'
    new_text = self.ui.name_lineEdit.text ()
    if str( new_text ).strip() != '' :
      # if the same name already exists
      i = 0
      while len( self.ui.listWidget.findItems( new_text, QtCore.Qt.MatchExactly ) ) > 0 :
        new_text += str( i )
        i += 1 
      self.ui.listWidget.addItem ( new_text )
      self.emit( QtCore.SIGNAL( "addItem" ), new_text ) 
    
  #
  #
  def onRemoveItem ( self ) :
    if DEBUG_MODE : print '>> NodeNamesEditor: onRemoveItem'
    list_item = self.ui.listWidget.currentItem()
    if list_item is not None :
      item_text = str ( list_item.text() )
      self.ui.listWidget.takeItem ( self.ui.listWidget.currentRow () )
      self.ui.listWidget.removeItemWidget ( list_item )
      self.emit( QtCore.SIGNAL( "removeItem" ), item_text )
  #
  #
  def onRenameItem ( self ) :
    if DEBUG_MODE : print '>> NodeNamesEditor: onRenameItem'
    new_text = str( self.ui.name_lineEdit.text () ).strip()
    
    if new_text == '' :
      if self.saved_text != '' :
        new_text = self.saved_text
        self.ui.name_lineEdit.setText ( new_text )  
      return
        
    list_item = self.ui.listWidget.currentItem()
    if list_item is not None : # e.g. listWidget is not empty
      old_text = list_item.text()
      if new_text != old_text :
        # if the same name already exists
        i = 0
        while len( self.ui.listWidget.findItems( new_text, QtCore.Qt.MatchExactly ) ) > 0 :
          new_text += str( i )
          i += 1 
        #if i > 0 : # if duplicates were found
          # correct new text
      self.ui.name_lineEdit.setText ( new_text )          
      list_item.setText ( new_text )
      self.saved_text = str ( new_text )
      self.ui.listWidget.clearSelection()
      self.ui.listWidget.setCurrentItem ( None )
      self.emit( QtCore.SIGNAL( "renameItem" ), old_text, new_text )
  #    
  #
  def onSelectionChanged ( self ) :
    if DEBUG_MODE : print '>> NodeNamesEditor: onSelectionChanged'
    list_item = self.ui.listWidget.currentItem()
    if list_item is not None :
      self.saved_text = str ( list_item.text() )
      self.ui.name_lineEdit.setText ( self.saved_text  )
      self.emit( QtCore.SIGNAL( "selectionChanged" ), self.saved_text  )   
