"""

 linkWidget.py

"""
from PyQt4 import QtGui, QtCore

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI 
from paramWidget import ParamWidget 
#
# LinkWidget widgets for linked parameter
#
class LinkWidget ( ParamWidget ) :
  #
  # buildGui
  #                 
  def buildGui ( self ) :
    #
    self.ui = Ui_LinkWidget ()    
    self.ui.setupUi ( self )
    if DEBUG_MODE : print ">> LinkWidget.buildGui"
#
# Ui_LinkWidget
#
class Ui_LinkWidget ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, LinkWidget ) :
    #
    self.widget = LinkWidget
    self.stringEdit = QtGui.QLineEdit ( LinkWidget )
    self.stringEdit.setEnabled ( False )
    
    self.stringEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.stringEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
    
    self.widget.hl.addWidget ( self.stringEdit )
    self.widget.hl.setStretch ( 1, 1 )
    
    QtCore.QMetaObject.connectSlotsByName ( LinkWidget )
    self.connectSignals ( LinkWidget )
  #
  # connectSignals
  #
  def connectSignals ( self, LinkWidget ) :
    #
    LinkWidget.connect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, LinkWidget ) :
    #
    LinkWidget.disconnect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
  #
  # onStringEditEditingFinished
  #
  def onStringEditEditingFinished ( self ) :
    #
    stringValue = self.stringEdit.text ()
    self.widget.param.setValue ( str ( stringValue ) )
  #
  # updateGui
  #
  def updateGui ( self, value ) :
    # 
    print ">> LinkWidget.updateGui",  value
    # self.stringEdit.setText ( value )