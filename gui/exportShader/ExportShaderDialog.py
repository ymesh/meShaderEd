"""
 ExportShaderDialog.py

 ver. 1.0.0
 Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
 
 Dialog for export node as SL shader 

""" 
import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars

import gui.ui_settings as UI

from core.node import Node

from ui_exportShaderDialog import Ui_ExportShaderDialog
#
# ExportShaderDialog
#
class ExportShaderDialog ( QtGui.QDialog ) :
  #
  # __init__
  #
  def __init__ ( self, node ) :
    #
    QtGui.QDialog.__init__ ( self )
    
    self.editNode = None

    self.buildGui ()
  #
  # buildGui
  #
  def buildGui ( self ) :
    # build the gui created with QtDesigner
    self.ui = Ui_ExportShaderDialog ()
    self.ui.setupUi ( self )
  #
  # connectSignals
  #
  def connectSignals ( self ) :
    # QtCore.QObject.
    pass
    """
    self.connect ( self.ui.name_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrName )
    self.connect ( self.ui.label_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrLabel )
    self.connect ( self.ui.master_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrMaster )
    self.connect ( self.ui.author_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrAuthor )
    self.connect ( self.ui.icon_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrIcon )
    self.connect ( self.ui.type_comboBox, QtCore.SIGNAL( 'activated(int)' ), self.onEditNodeType )
    self.connect ( self.ui.help_plainTextEdit, QtCore.SIGNAL( 'textChanged()' ), self.onEditNodeTxtAttr )
    """
  #
  # disconnectSignals
  #
  def disconnectSignals ( self ) :
    #
    pass
    """
    if self.editNode is not None :
      self.disconnect ( self.ui.name_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrName )
      self.disconnect ( self.ui.label_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrLabel )
      self.disconnect ( self.ui.master_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrMaster )
      self.disconnect ( self.ui.author_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrAuthor )
      self.disconnect ( self.ui.icon_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrIcon )
      self.disconnect ( self.ui.type_comboBox, QtCore.SIGNAL( 'activated(int)' ), self.onEditNodeType )
      self.disconnect ( self.ui.help_plainTextEdit, QtCore.SIGNAL( 'textChanged()' ), self.onEditNodeTxtAttr )
    """