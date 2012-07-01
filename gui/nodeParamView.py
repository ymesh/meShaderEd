#===============================================================================
# nodeParamView.py
#
# 
#
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import QDir, QString, QModelIndex
from PyQt4.QtGui  import QFileSystemModel
from PyQt4.QtGui  import QFileIconProvider

#from ui_nodeParam import Ui_nodeParam
#from MainWindow import MainWindow

from core.node import Node
from core.nodeLibrary import NodeLibrary

import gui.ui_settings as UI
from gui.params.StringWidget import StringWidget 
from gui.params.FloatWidget import FloatWidget 
from gui.params.IntWidget import IntWidget 
from gui.params.ColorWidget import ColorWidget
from gui.params.NormalWidget import NormalWidget
from gui.params.PointWidget import PointWidget
from gui.params.VectorWidget import VectorWidget
from gui.params.MatrixWidget import MatrixWidget
#
#
#
class NodeParamView ( QtGui.QWidget ):
  #
  #
  def __init__ ( self ):
    QtGui.QWidget.__init__ ( self )
    
    self.gfxNode = None
    
    # core.model.FloatProperty : modifier.view.FloatPropertyModifier,     
    #self.modifiers = {core.model.ColorProperty : modifier.ColorWidget.ColorWidget,
    #                  core.model.FloatProperty : modifier.FloatWidget.FloatWidget,
    #                  core.model.MatrixProperty : modifier.view.MatrixPropertyModifier,
    #                  core.model.PointProperty : modifier.view.Tuple3DPropertyModifier,
    #                  core.model.VectorProperty : modifier.view.Tuple3DPropertyModifier,
    #                  core.model.NormalProperty : modifier.view.Tuple3DPropertyModifier,
    #                  core.model.StringProperty : modifier.view.StringPropertyModifier}
    
    self.paramWidgets = {  'string' : StringWidget
                          ,'image' : StringWidget
                          ,'rib' : StringWidget
                          ,'surface' : StringWidget 
                          ,'displacement' : StringWidget 
                          ,'light' : StringWidget  
                          ,'volume' : StringWidget
                          ,'float' : FloatWidget
                          ,'int' : IntWidget
                          ,'color' : ColorWidget
                          ,'normal' : NormalWidget
                          ,'transform' : PointWidget
                          ,'point' : PointWidget
                          ,'vector' : VectorWidget
                          ,'matrix' : MatrixWidget
                        }
    self.buildGui ()
    self.updateGui ()
    self.connectLabelSignals ()              
  #
  #
  def connectLabelSignals ( self ) :
    self.connect( self.nameEdit, QtCore.SIGNAL( 'editingFinished()' ), self.nodeLabelChanged )
  #
  #
  def disconnectLabelSignals ( self ) :
    self.disconnect( self.nameEdit, QtCore.SIGNAL( 'editingFinished()' ), self.nodeLabelChanged )
    
  #
  #
  def connectParamSignals ( self ) :
    #print ">> NodeParamView: connectParamSignals"
    if self.gfxNode is not None :
      for inputParam in self.gfxNode.node.inputParams:
        self.connect( inputParam, QtCore.SIGNAL( 'paramChanged(QObject)' ), self.onParamChanged )
  #
  #
  def disconnectParamSignals ( self ) :
    #print ">> NodeParamView: disconnectParamSignals"
    if self.gfxNode is not None :
      for inputParam in self.gfxNode.node.inputParams:
        self.disconnect( inputParam, QtCore.SIGNAL( 'paramChanged(QObject)' ), self.onParamChanged )          
  #
  #
  def setNode ( self, gfxNode ):
    self.disconnectParamSignals ()
    self.gfxNode = gfxNode
    self.nameEdit.setEnabled ( self.gfxNode is not None )
    self.updateGui ()
    self.connectParamSignals ()
  #
  #
  def onParamChanged ( self, param ):
    print ">> NodeParamView: onParamChanged node = %s param = %s" % ( self.gfxNode.node.label, param.name )  
    self.emit( QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self.gfxNode.node, param )   
  #
  #
  def nodeLabelChanged ( self ):
    if self.gfxNode is not None : 
      newLabel = self.nameEdit.text().simplified()
      newLabel = newLabel.replace ( ' ', "_" )
      if not newLabel.isEmpty() :
        # update label only if realy changed    
        if newLabel != self.gfxNode.node.label :
          # rename node label if same name exists in NodeNet      
          self.emit( QtCore.SIGNAL( 'nodeLabelChanged' ), self.gfxNode, newLabel ) 
          self.nameEdit.clear()
      self.nameEdit.setText( self.gfxNode.node.label )
  #
  #
  def buildGui ( self ):
    #currentWidget = self.stackedWidget.currentWidget()
    #self.stackedWidget.removeWidget(currentWidget)
        
    label = QtGui.QLabel ()
    label.setMinimumSize ( QtCore.QSize ( UI.NODE_LABEL_WIDTH, UI.HEIGHT ) )
    label.setMaximumSize ( QtCore.QSize ( UI.NODE_LABEL_WIDTH, UI.HEIGHT ) )
    
    font = QtGui.QFont()
    label.setFont ( font )
    #label.setAlignment(QtCore.Qt.AlignCenter)
    label.setText ('Node Label')

    self.nameEdit = QtGui.QLineEdit () 
    self.nameEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )   
        
    headerLayout = QtGui.QHBoxLayout()
    headerLayout.setSpacing ( UI.SPACING )
    headerLayout.setMargin ( UI.SPACING )
    
    headerLayout.addWidget( label )
    headerLayout.addWidget( self.nameEdit )
    
    self.stackedWidget = QtGui.QStackedWidget ( self )
    frame = QtGui.QFrame()
    self.stackedWidget.addWidget ( frame )
    
    mainLayout = QtGui.QVBoxLayout()
    mainLayout.addLayout ( headerLayout )
    mainLayout.addWidget ( self.stackedWidget )
   
    self.setLayout ( mainLayout )
    self.nameEdit.setEnabled ( False )
  #
  #
  def updateGui ( self ):
    currentWidget = self.stackedWidget.currentWidget ()
    self.stackedWidget.removeWidget ( currentWidget )
    
    
    frame = QtGui.QFrame()
        
    frameLayout = QtGui.QVBoxLayout ()
    frameLayout.setSpacing ( UI.SPACING )
    frameLayout.setMargin ( UI.SPACING )
    frameLayout.setAlignment ( QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft )
    
    frame.setLayout( frameLayout )
    
    self.nameEdit.clear()
    
    if self.gfxNode is not None :
      self.nameEdit.setText ( self.gfxNode.node.label )
      for inputParam in self.gfxNode.node.inputParams:
        if not self.gfxNode.node.isInputParamLinked( inputParam ):
          if inputParam.type in self.paramWidgets.keys() :
            #print '%s type = %s' % ( inputParam.label, inputParam.type )  
            paramWidget = apply ( self.paramWidgets [ inputParam.type ], [ inputParam, self.gfxNode, self ] )
            frameLayout.addWidget ( paramWidget ) 
            
    
    spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding )
    frameLayout.addItem ( spacer )
    # build a scroll area
    scrollArea = QtGui.QScrollArea () 
    scrollArea.setWidgetResizable ( True )        
    scrollArea.setWidget ( frame )
    
    self.stackedWidget.addWidget ( scrollArea )
  
    
