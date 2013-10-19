"""
 
 ViewComputedCodeDialog.py

 ver. 1.0.0
 Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
 
 Dialog for managing node code
 
"""
import os, sys
from PyQt4 import QtCore, QtGui

from global_vars import app_global_vars, DEBUG_MODE, VALID_RIB_NODE_TYPES, VALID_RSL_NODE_TYPES, VALID_RSL_SHADER_TYPES

from nodeEditor.nodeCodeEditor import NodeCodeEditor
from ui_viewComputedCodeDialog import Ui_ViewComputedCodeDialog
#
# ViewComputedCodeDialog
#
class ViewComputedCodeDialog ( QtGui.QDialog ) :
  #
  # __init__
  #
  def __init__ ( self, node = None ):
    #
    QtGui.QDialog.__init__ ( self )

    self.node = node
    self.code = self.getComputedCode ( node )
    self.buildGui ()
    
  #
  #  buildGui
  #
  def buildGui ( self ) :
    # build the gui created with QtDesigner
    self.ui = Ui_ViewComputedCodeDialog ()
    self.ui.setupUi ( self )  
    self.ui.codeEdit.setNodeCode ( self.code, 'SL', readOnly = True )
  #
  # getComputedCode
  #
  def getComputedCode ( self, node ) :
    #
    computedCode = None
    if node is not None :
      computedCode = node.getComputedCode ( CodeOnly = True )
        
    return computedCode