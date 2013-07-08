"""

 nodeParamView.py

"""
import os, sys
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import QDir, QString, QModelIndex
from PyQt4.QtGui  import QFileSystemModel
from PyQt4.QtGui  import QFileIconProvider

#from ui_nodeParam import Ui_nodeParam
#from MainWindow import MainWindow

from core.node import Node
from core.nodeLibrary import NodeLibrary
from gui.nodeParamList import NodeParamList

import gui.ui_settings as UI
from gui.params.StringWidget import StringWidget
from gui.params.FloatWidget import FloatWidget
from gui.params.IntWidget import IntWidget
from gui.params.ColorWidget import ColorWidget
from gui.params.NormalWidget import NormalWidget
from gui.params.PointWidget import PointWidget
from gui.params.VectorWidget import VectorWidget
from gui.params.MatrixWidget import MatrixWidget
from gui.params.TextWidget import TextWidget
from gui.params.ControlWidget import ControlWidget
#
# NodeParamView
#
class NodeParamView ( QtGui.QWidget ) :
  #
  # __init__
  #
  def __init__ ( self ) :
    #
    QtGui.QWidget.__init__ ( self )

    self.gfxNode = None
    
    self.inputParamList = None
    self.outputParamList = None
    
    self.showConnected = False
    self.buildGui ()
    self.updateGui ()
    self.connectLabelSignals ()
  #
  # setNode
  #
  def setNode ( self, gfxNode ) :
    #
    print ">> NodeParamView.setNode"
    self.disconnectParamSignals ()
    self.gfxNode = gfxNode
    self.inputParamList.setNode ( gfxNode )
    self.outputParamList.setNode ( gfxNode )
    self.nameEdit.setEnabled ( self.gfxNode is not None )
    self.updateGui ()
    self.connectParamSignals ()
    
  #
  # connectLabelSignals
  #
  def connectLabelSignals ( self ) :
    #
    self.connect( self.nameEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.nodeLabelChanged )
  #
  # disconnectLabelSignals
  #
  def disconnectLabelSignals ( self ) :
    #
    self.disconnect( self.nameEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.nodeLabelChanged )
  #
  # connectParamSignals
  #
  def connectParamSignals ( self ) :
    #print ">> NodeParamView.connectParamSignals"
    if self.gfxNode is not None :
      for inputParam in self.gfxNode.node.inputParams :
        self.connect ( inputParam, QtCore.SIGNAL ( 'paramChanged(QObject)' ), self.onParamChanged )
      for outputParam in self.gfxNode.node.outputParams :
        self.connect ( outputParam, QtCore.SIGNAL ( 'paramChanged(QObject)' ), self.onParamChanged )
  #
  # disconnectParamSignals
  #
  def disconnectParamSignals ( self ) :
    #print ">> NodeParamView.disconnectParamSignals"
    if self.gfxNode is not None :
      for inputParam in self.gfxNode.node.inputParams :
        self.disconnect ( inputParam, QtCore.SIGNAL ( 'paramChanged(QObject)' ), self.onParamChanged )
      for outputParam in self.gfxNode.node.outputParams :
        self.disconnect ( outputParam, QtCore.SIGNAL ( 'paramChanged(QObject)' ), self.onParamChanged )
  #
  # onParamChanged
  #
  def onParamChanged ( self, param ) :
    #
    print ">> NodeParamView.onParamChanged node = %s param = %s" % ( self.gfxNode.node.label, param.name )
    self.emit ( QtCore.SIGNAL ( 'nodeParamChanged' ), self.gfxNode, param ) # .node
  #
  # onParamRemoved
  #
  def onParamRemoved ( self, param ) :
    #
    print ">> NodeParamView.onRemoved node = %s param = %s" % ( self.gfxNode.node.label, param.name )
    self.gfxNode.node.removeParam ( param )
    #self.emit ( QtCore.SIGNAL ( 'nodeParamChanged' ), self.gfxNode, param ) # .node
    self.disconnectParamSignals ()
    self.updateGui ()
    self.connectParamSignals ()
  #
  # nodeLabelChanged
  #
  def nodeLabelChanged ( self ) :
    #
    if self.gfxNode is not None :
      from core.meCommon import getParsedLabel
      newLabel = getParsedLabel ( self.nameEdit.text () )
      if not newLabel.isEmpty () :
        # update label only if realy changed
        if newLabel != self.gfxNode.node.label :
          # rename node label if same name exists in NodeNet
          self.emit ( QtCore.SIGNAL ( 'nodeLabelChanged' ), self.gfxNode, newLabel )
          self.nameEdit.clear ()
      self.nameEdit.setText ( self.gfxNode.node.label )
  #
  # buildGui
  #
  def buildGui ( self ) :
    #
    label = QtGui.QLabel ()
    label.setMinimumSize ( QtCore.QSize ( UI.NODE_LABEL_WIDTH, UI.HEIGHT ) )
    label.setMaximumSize ( QtCore.QSize ( UI.NODE_LABEL_WIDTH, UI.HEIGHT ) )

    font = QtGui.QFont ()
    label.setFont ( font )
    #label.setAlignment(QtCore.Qt.AlignCenter)
    label.setText ('Node Label')

    self.nameEdit = QtGui.QLineEdit ()
    self.nameEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
    self.nameEdit.setEnabled ( False )
    
    self.showConnectButton = QtGui.QToolButton ( self )
    sizePolicy = QtGui.QSizePolicy ( QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed )
    sizePolicy.setHorizontalStretch ( 20 )
    sizePolicy.setVerticalStretch ( 20 )
    sizePolicy.setHeightForWidth ( self.showConnectButton.sizePolicy().hasHeightForWidth() )
    self.showConnectButton.setSizePolicy ( sizePolicy )
    self.showConnectButton.setMaximumSize ( QtCore.QSize ( 20, 20 ) )
    icon = QtGui.QIcon ()
    icon.addPixmap ( QtGui.QPixmap ( ':/show_icons/resources/show_connect.png' ), QtGui.QIcon.Normal, QtGui.QIcon.On )
    self.showConnectButton.setIcon ( icon )
    self.showConnectButton.setAutoRaise ( False )
    self.showConnectButton.setCheckable ( True )
    self.showConnectButton.setToolTip ( 'Show connected parameters' )
    #self.showConnectButton.setIconSize ( QtCore.QSize ( 16, 16 ) )
    self.showConnectButton.setObjectName ( 'showConnectButton' )

    headerLayout = QtGui.QHBoxLayout ()
    headerLayout.setSpacing ( UI.SPACING )
    headerLayout.setMargin ( UI.SPACING )
    headerLayout.setStretch ( 1, 1 )

    headerLayout.addWidget ( label )
    headerLayout.addWidget ( self.nameEdit )
    headerLayout.addWidget ( self.showConnectButton )

    mainLayout = QtGui.QVBoxLayout ()
    mainLayout.addLayout ( headerLayout )
    
    self.params_tabs = QtGui.QTabWidget ( self )
    
    self.inputs_tab = QtGui.QWidget ()
    self.inputs_grid = QtGui.QGridLayout ( self.inputs_tab )
    self.inputParamList = NodeParamList ( self, self.gfxNode, isInput = True, showConnected = self.showConnected )
    self.inputs_grid.addWidget ( self.inputParamList, 0, 0, 1, 1 )
    self.params_tabs.addTab ( self.inputs_tab, 'Input' )
    
    self.inputsStackedWidget = QtGui.QStackedWidget ( self.inputs_tab )
    self.inputsFrame = QtGui.QFrame ()
    self.inputsStackedWidget.addWidget ( self.inputsFrame )
    self.inputs_grid.addWidget ( self.inputsStackedWidget )
    
    self.outputs_tab = QtGui.QWidget ()
    self.outputs_grid = QtGui.QGridLayout ( self.outputs_tab )
    self.outputParamList = NodeParamList ( self, self.gfxNode, isInput = False, showConnected = self.showConnected )
    self.outputs_grid.addWidget ( self.outputParamList, 0, 0, 1, 1)
    self.params_tabs.addTab ( self.outputs_tab, 'Output' )
    
    self.outputsStackedWidget = QtGui.QStackedWidget ( self.outputs_tab )
    self.outputsFrame = QtGui.QFrame ()
    self.outputsStackedWidget.addWidget ( self.outputsFrame )
    self.outputs_grid.addWidget ( self.outputsStackedWidget )
    
    self.params_tabs.setCurrentIndex ( 0 )
    
    mainLayout.addWidget ( self.params_tabs )
    
    self.setLayout ( mainLayout )
    
    self.inputParamList.stackedWidget = self.inputsStackedWidget
    self.outputParamList.stackedWidget = self.outputsStackedWidget
  #
  # updateGui
  #
  def updateGui ( self ) :
    #
    self.nameEdit.clear ()
    if self.gfxNode is not None :
      self.nameEdit.setText ( self.gfxNode.node.label )
    
    self.inputParamList.updateGui ()
    self.outputParamList.updateGui ()
    