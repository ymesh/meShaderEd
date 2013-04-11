#===============================================================================
# nodeSwatchParam.py
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

from ui_nodeSwatchParam import Ui_NodeSwatchParam

import ui_settings as UI
#
#
#
class NodeSwatchParam ( QtGui.QWidget ) :
  #
  # __init__
  #
  def __init__ ( self ) :
    #
    QtGui.QWidget.__init__ ( self )

    self.ui = Ui_NodeSwatchParam () 
    self.ui.setupUi ( self )

    self.buildGui ()
    self.updateGui ()
  #
  # buildGui
  #
  def buildGui ( self ) :
    #
    pass 
    #
  # updateGui
  #
  def updateGui ( self ) :
    #
    pass 
    #            