#===============================================================================
# nodeEditor.py.py
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

import gui.ui_settings as UI

from core.node import Node

from ui_nodeEditor import Ui_NodeEditor
#
# NodeEditor
#
class NodeEditor ( QtGui.QWidget ) :
  #
  # __init__
  #
  def __init__ ( self, parent, editNode = None ) :
    #
    QtGui.QDialog.__init__ ( self )

    self.editNode = editNode
          
    #self.debugPrint()
    self.buildGui ()
    self.setNode ( editNode )
  #
  # buildGui
  #
  def buildGui ( self ) :
    # build the gui created with QtDesigner
    self.ui = Ui_NodeEditor ()
    self.ui.setupUi ( self )
  #  
  # setNode
  #  
  def setNode ( self, editNode ) :
    # 
    self.disconnectSignals ()
    self.editNode = editNode
    
    if self.editNode is not None :
      #
      name = self.editNode.name
      if self.editNode.name is None : name = ''
      self.ui.name_lineEdit.setText ( name ) 
      
      label = self.editNode.label
      if self.editNode.label is None : label = ''
      self.ui.label_lineEdit.setText ( label )
      
      author = self.editNode.author
      if self.editNode.author is None : author = ''
      self.ui.author_lineEdit.setText ( author ) 
      
      master = self.editNode.master
      if self.editNode.master is None : master = '' 
      self.ui.master_lineEdit.setText ( master ) 
      
      icon = self.editNode.icon
      if self.editNode.icon is None : icon = '' 
      self.ui.icon_lineEdit.setText ( icon )
      # print '* self.editNode.help = %s' %  self.editNode.help
      
      doc = QtGui.QTextDocument ()
      help_text = ''
      if self.editNode.help != None : 
        help_text = self.editNode.help  
      
      doc.setPlainText ( help_text )
      layout = QtGui.QPlainTextDocumentLayout( doc )
      doc.setDocumentLayout( layout )
        
      self.ui.help_plainTextEdit.setDocument ( doc )  
      
      self.ui.id_lineEdit.setText ( str ( self.editNode.id ) ) 
      
      self.ui.type_comboBox.setEditable ( False )
      self.ui.type_comboBox.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
      self.ui.type_comboBox.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
      
      currentIdx = -1
      i = 0
      for label in [ 'rib', 'rib_code', 'rsl_code', 'image', 'surface', 'displacement', 'light', 'volume', 'variable', 'connector', 'swatch' ]  :
        self.ui.type_comboBox.addItem ( label )
        if label == self.editNode.type : 
          currentIdx = i
        i += 1
      self.ui.type_comboBox.setCurrentIndex ( currentIdx )
      
      # temporary disabled, until "how to do it gracefully" will be clear ... 
      self.ui.type_comboBox.setEnabled ( False )
      
      self.connectSignals ()
  #
  # connectSignals
  #
  def connectSignals ( self ) :
    # QtCore.QObject.
    self.connect ( self.ui.name_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrName )
    self.connect ( self.ui.label_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrLabel )
    self.connect ( self.ui.master_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrMaster )
    self.connect ( self.ui.author_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrAuthor )
    self.connect ( self.ui.icon_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrIcon )
    self.connect ( self.ui.type_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditNodeType )
    self.connect ( self.ui.help_plainTextEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditNodeTxtAttr )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self ) :
    #
    if self.editNode is not None :
      self.disconnect ( self.ui.name_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrName )
      self.disconnect ( self.ui.label_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrLabel )
      self.disconnect ( self.ui.master_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrMaster )
      self.disconnect ( self.ui.author_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrAuthor )
      self.disconnect ( self.ui.icon_lineEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditNodeStrAttrIcon )
      self.disconnect ( self.ui.type_comboBox, QtCore.SIGNAL ( 'activated(int)' ), self.onEditNodeType )
      self.disconnect ( self.ui.help_plainTextEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditNodeTxtAttr )
  #
  # doesn't work ...
  #
  def onEditNodeStrAttr ( self, attr = None ) :
    if attr is not None and self.editNode is not None:
      if attr == 'name' : 
        self.editNode.name = str ( self.ui.name_lineEdit.text () )
      elif attr == 'label' : 
        self.editNode.label = str ( self.ui.label_lineEdit.text () )
      elif attr == 'master' : 
        self.editNode.master = str ( self.ui.master_lineEdit.text () )
      elif attr == 'author' :
        self.editNode.author = str ( self.ui.author_lineEdit.text () )
      elif attr == 'icon' :
        self.editNode.icon = str ( self.ui.icon_lineEdit.text () )
  #
  #
  #
  def onEditNodeStrAttrName ( self ) : self.editNode.name = str ( self.ui.name_lineEdit.text () )
  def onEditNodeStrAttrLabel ( self ) : self.editNode.label = str ( self.ui.label_lineEdit.text () )
  def onEditNodeStrAttrMaster ( self ) : self.editNode.master = str ( self.ui.master_lineEdit.text () )
  def onEditNodeStrAttrAuthor ( self ) : self.editNode.author = str ( self.ui.author_lineEdit.text () ) 
  def onEditNodeStrAttrIcon ( self ) : self.editNode.icon = str ( self.ui.icon_lineEdit.text () )      
  #
  # onEditNodeTxtAttr
  #
  def onEditNodeTxtAttr ( self ) : self.editNode.help = str ( self.ui.help_plainTextEdit.toPlainText () )
  #
  # onEditNodeType
  #
  def onEditNodeType ( self, idx ) : self.editNode.type = str ( self.ui.type_comboBox.itemText ( idx ) )

  
          
    
