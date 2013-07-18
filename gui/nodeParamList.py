"""

 nodeParamList.py

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
from global_vars import DEBUG_MODE

import gui.ui_settings as UI
from gui.params.linkWidget import LinkWidget
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
# NodeParamListFrame
#
class NodeParamListTab ( QtGui.QWidget ) :
  #
  # __init__
  #
  def __init__ ( self, parent, gfxNode = None, isInput = True, showConnected = False ) :
    #
    QtGui.QWidget.__init__ ( self, parent )
    
    self.nodeParamView = parent
    self.gfxNode = gfxNode
    self.isInput = isInput
    
    self.showConnected = showConnected
    
    self.labelWidth = UI.CHECK_WIDTH + UI.LABEL_WIDTH + 6 + 20
    self.stackedWidget = None
    self.nodeParamList = None 
    
    self.buildGui ()
    self.updateGui ()
    self.connectSignals ()
  #
  # connectSignals
  #
  def connectSignals ( self ) :
    #
    self.connect ( self.paramHeader, QtCore.SIGNAL ( 'sectionResized(int,int,int)' ), self.onSectionResized )
  #
  # onSectionResized
  #
  def onSectionResized ( self, idx, oldSize, newSize ) :
    #
    #if DEBUG_MODE : print ( '>> NodeParamViewTab.onSectionResized %d %d %d' ) % ( idx, oldSize, newSize )
    if idx == 0 :
      self.labelWidth = newSize
      if self.nodeParamList is not None :
        self.nodeParamList.setLabelWidth ( newSize )
        #self.nodeParamList.updateGui ()
  #
  # setNode
  #
  def setNode ( self, gfxNode ) :
    #
    #if DEBUG_MODE :print ">> NodeParamListTab.setNode"
    self.gfxNode = gfxNode
    #self.nodeParamList.setNode ( gfxNode )
    self.updateGui ()
  #
  # onParamRemoved
  #
  def onParamRemoved ( self, param ) :
    #
    if DEBUG_MODE : print ">> NodeParamViewTab.onRemoved node = %s param = %s" % ( self.gfxNode.node.label, param.name )
    self.gfxNode.node.removeParam ( param )
    #self.emit ( QtCore.SIGNAL ( 'nodeParamChanged' ), self.gfxNode, param ) # .node
    self.nodeParamView.disconnectParamSignals ()
    self.updateGui ()
    self.nodeParamView.connectParamSignals ()
  #
  # buildGui
  #
  def buildGui ( self ) :
    #
    self.model = QtGui.QStandardItemModel ()
    self.model.setColumnCount ( 2 )
    self.model.setHeaderData ( 0, QtCore.Qt.Horizontal, QtCore.QVariant ( 'Parameter' ) )
    self.model.setHeaderData ( 1, QtCore.Qt.Horizontal, QtCore.QVariant ( 'Value' ) )
      
    self.paramHeader = QtGui.QHeaderView ( QtCore.Qt.Horizontal, self )
    self.paramHeader.setModel ( self.model )
    self.paramHeader.resizeSection ( 0, self.labelWidth )
    self.paramHeader.setMinimumSectionSize  ( self.labelWidth )
    self.paramHeader.setStretchLastSection ( True )
    self.paramHeader.setFixedHeight ( 24 )
    self.paramHeader.setFrameShape ( QtGui.QFrame.Box )
    self.paramHeader.setFrameShadow ( QtGui.QFrame.Raised )
    self.paramHeader.setLineWidth ( 1 )
    self.paramHeader.setMidLineWidth ( 2 )
    
    self.stackedWidget = QtGui.QStackedWidget ( self )
    
    self.paramsLayout = QtGui.QGridLayout ( self )
    self.paramsLayout.setContentsMargins ( 2, 2, 2, 2 )
    self.paramsLayout.setSizeConstraint ( QtGui.QLayout.SetNoConstraint )
    self.paramsLayout.setVerticalSpacing ( 0 )
    self.paramsLayout.setRowStretch ( 1, 1 )
    
    self.paramsLayout.addWidget ( self.paramHeader, 0, 0, 1, 1 )
    self.paramsLayout.addWidget ( self.stackedWidget, 1, 0, 1, 1 )
    
    frame = QtGui.QFrame ()
    self.stackedWidget.addWidget ( frame )
  #
  # updateGui
  #
  def updateGui ( self ) :
    #
    #if DEBUG_MODE : print '>> NodeParamListTab.updateGui %s' % self.gfxNode
    self.removeValueWidget ()
    if self.gfxNode is not None :
      frame = QtGui.QFrame ()
      
      self.nodeParamList = NodeParamList ( self, self.gfxNode, self.isInput, self.showConnected )
      self.nodeParamList.setLabelWidth ( self.labelWidth )
      frame.setLayout ( self.nodeParamList.paramListLayout )
      
      self.nodeParamList.updateGui ()
      
      # build a scroll area
      scrollArea = QtGui.QScrollArea ()
      scrollArea.setWidgetResizable ( True )
      scrollArea.setWidget ( frame )
  
      self.stackedWidget.addWidget ( scrollArea )
  #
  # Remove stackedWidget's layout every time,
  # when current parameter (or it's type) is changing
  #
  def removeValueWidget ( self ) :
    #
    if self.stackedWidget is not None :
      #while True :
      currentWidget = self.stackedWidget.currentWidget ()
      if currentWidget is not None :
        #print '> removeWidget: %s' % currentWidget
        self.stackedWidget.removeWidget ( currentWidget )
      #else :
      #    break
#
# NodeParamList
#
class NodeParamList ( QtGui.QWidget ) :
  #
  # __init__
  #
  def __init__ ( self, parent, gfxNode = None, isInput = True, showConnected = False ) :
    #
    QtGui.QWidget.__init__ ( self, parent )
    
    self.nodeParamViewTab = parent
    self.gfxNode = gfxNode
    self.isInput = isInput
    
    self.showConnected = showConnected
    
    self.paramWidgets = {  'string'       : StringWidget
                          ,'image'        : StringWidget
                          ,'rib'          : StringWidget
                          ,'surface'      : StringWidget
                          ,'displacement' : StringWidget
                          ,'light'        : StringWidget
                          ,'volume'       : StringWidget
                          ,'float'        : FloatWidget
                          ,'int'          : IntWidget
                          ,'color'        : ColorWidget
                          ,'normal'       : NormalWidget
                          ,'transform'    : PointWidget
                          ,'point'        : PointWidget
                          ,'vector'       : VectorWidget
                          ,'matrix'       : MatrixWidget
                          ,'text'         : TextWidget
                          ,'control'      : ControlWidget
                          ,'shader'       : StringWidget
                          ,'geom'         : StringWidget
                        }
    self.paramListLayout = None
    self.labelWidth = UI.CHECK_WIDTH + UI.LABEL_WIDTH
    self.buildGui ()
  #
  # setNode
  #
  def setNode ( self, gfxNode ) :
    #
    #if DEBUG_MODE :print ">> NodeParamList.setNode"
    self.gfxNode = gfxNode
    self.updateGui ()
  #
  # setLabelWidth
  #
  def setLabelWidth ( self, labelWidth ) :
    #
    self.labelWidth = labelWidth
    self.paramListLayout.setColumnMinimumWidth ( 0, self.labelWidth )
  #
  # buildGui
  #
  def buildGui ( self ) :
    #
    #if DEBUG_MODE : print '>> NodeParamList.buildGui'
      
    self.paramListLayout = QtGui.QGridLayout ()
    self.paramListLayout.setSizeConstraint ( QtGui.QLayout.SetNoConstraint )
    self.paramListLayout.setSpacing ( UI.SPACING )
    self.paramListLayout.setMargin ( UI.SPACING )
    self.paramListLayout.setAlignment ( QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft )
    self.paramListLayout.setColumnMinimumWidth ( 0, self.labelWidth )
    self.paramListLayout.setColumnStretch ( 1, 1 )
  #
  # updateGui
  #
  def updateGui ( self ) :
    #
    #if DEBUG_MODE : print '>> NodeParamList.updateGui %s' % self.gfxNode
    self.paramListLayout.setColumnMinimumWidth ( 0, self.labelWidth )
    if self.gfxNode is not None :
      params = []
      if self.isInput :
        params = self.gfxNode.node.inputParams
      else :
        params = self.gfxNode.node.outputParams
      paramWidget = None
      paramRows = 0
      for param in params :
        isParamLinked = False
        linkedParamsList = []
        
        if param.isInput :
          ( srcNode, srcParam ) = self.gfxNode.node.getLinkedSrcNode ( param )
          isParamLinked = srcNode is not None 
          if isParamLinked :
            linkedParamsList.append ( ( srcNode, srcParam ) )
        else :
          linkedParamsList = self.gfxNode.node.getLinkedDstNodes ( param, linkedParamsList )
          isParamLinked = ( len ( linkedParamsList ) > 0 )
        
        if param.display :
          if param.type in self.paramWidgets.keys () :
            if isParamLinked :
              #print '***', param.name, 'linked to', linkedParamsList
              if self.showConnected :
                paramWidget = LinkWidget ( param, self.gfxNode, False, linkedParamsList )
              else :
                continue
            else :
              paramWidget = apply ( self.paramWidgets [ param.type ], [ param, self.gfxNode ] )
            
            if paramWidget is not None :
              self.paramListLayout.addLayout ( paramWidget.label_vl, paramRows, 0, 1, 1 )
              self.paramListLayout.addLayout ( paramWidget.param_vl, paramRows, 1, 1, 1 )
              if not param.enabled :
                paramWidget.setEnabled ( False )
              
              if param.removable :
                QtCore.QObject.connect ( paramWidget, QtCore.SIGNAL ( 'nodeParamRemoved' ), self.nodeParamViewTab.onParamRemoved )
          paramRows += 1
      
      spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding )
      self.paramListLayout.addItem ( spacer, paramRows, 0, 1, 1 ) 
      self.paramListLayout.setRowStretch ( paramRows, 1 )
