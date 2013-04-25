#===============================================================================
# ControlWidget.py
#===============================================================================

from PyQt4 import QtGui, QtCore

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI
from paramWidget import ParamWidget

#
# ControlWidget
#
class ControlWidget ( ParamWidget ) :
  #
  # buildGui
  #
  def buildGui ( self ) :
    #
    if not self.ignoreSubtype :
      if self.param.subtype == 'button':
        self.ui = Ui_ControlWidget_button ()
      else:
        self.ui = Ui_ControlWidget_field ()
    else :
      self.ui = Ui_ControlWidget_field ()

    self.ui.setupUi ( self )
#
# Ui_ControlWidget_field
#
class Ui_ControlWidget_field ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, ControlWidget ) :
    #
    self.widget = ControlWidget

    self.stringEdit = QtGui.QLineEdit ( ControlWidget )

    self.stringEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
    self.stringEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )

    self.widget.hl.addWidget ( self.stringEdit )
    self.widget.hl.setStretch ( 1, 1 )

    QtCore.QMetaObject.connectSlotsByName ( ControlWidget )
    self.connectSignals ( ControlWidget )
  #
  # connectSignals
  #
  def connectSignals ( self, ControlWidget ) :
    #
    ControlWidget.connect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, ControlWidget ) :
    #
    ControlWidget.disconnect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
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
    self.stringEdit.setText ( value )
#
# Ui_ControlWidget_button
#
class Ui_ControlWidget_button ( object ) :
  #
  # setupUi
  #
  def setupUi ( self, ControlWidget ) :
    #
    self.widget = ControlWidget

    self.button = QtGui.QPushButton ( self.widget.param.label, ControlWidget )
    #self.button.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
    #self.button.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.COMBO_HEIGHT ) )

    spacer = QtGui.QSpacerItem ( UI.HEIGHT, UI.HEIGHT, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )

    self.widget.hl.addWidget ( self.button )
    self.widget.hl.addItem ( spacer )

    QtCore.QMetaObject.connectSlotsByName ( ControlWidget )
    self.connectSignals ( ControlWidget )
  #
  # connectSignals
  #
  def connectSignals ( self, ControlWidget ) :
    #
    ControlWidget.connect ( self.button, QtCore.SIGNAL ( 'clicked()' ), self.onClicked )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self, ControlWidget ) :
    #
    ControlWidget.disconnect ( self.button, QtCore.SIGNAL ( 'clicked()' ), self.onClicked )
  #
  # onClicked
  #
  def onClicked ( self ) :
    #
    if DEBUG_MODE : print '>> Ui_ControlWidget_button.clicked()'
    self.widget.param.execControlCode ( self.widget.gfxNode.node )
  #
  # updateGui
  #
  def updateGui ( self, value ) :
    #
    pass
    #self.button.setText ( value )
