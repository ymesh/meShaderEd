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
# NodeParamList
#
class NodeParamList ( QtGui.QWidget ) :
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
    self.stackedWidget = None
    self.buildGui ()
    self.updateGui ()
  #
  # setNode
  #
  def setNode ( self, gfxNode ) :
    #
    if DEBUG_MODE :print ">> NodeParamList.setNode"
    self.gfxNode = gfxNode
    self.updateGui ()
  #
  # buildGui
  #
  def buildGui ( self ) :
    #
    pass
    """
    self.stackedWidget = QtGui.QStackedWidget ( self )
    self.frame = QtGui.QFrame ()
    self.stackedWidget.addWidget ( self.frame )
    """
  #
  # updateGui
  #
  def updateGui ( self ) :
    #
    if self.stackedWidget is not None :
      currentWidget = self.stackedWidget.currentWidget ()
      self.stackedWidget.removeWidget ( currentWidget )
      
      if self.gfxNode is not None :
        frame = QtGui.QFrame ()
    
        frameLayout = QtGui.QVBoxLayout ()
        frameLayout.setSpacing ( UI.SPACING )
        frameLayout.setMargin ( UI.SPACING )
        frameLayout.setAlignment ( QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft )
    
        frame.setLayout ( frameLayout )
        
        params = []
        if self.isInput :
          params = self.gfxNode.node.inputParams
        else :
          params = self.gfxNode.node.outputParams
          
        for param in params :
          isParamLinked = False
          if self.isInput :
            ( srcNode, srcParam ) = self.gfxNode.node.getLinkedSrcNode ( param )
            isParamLinked = srcNode is not None 
          else :
            isParamLinked = self.gfxNode.node.isOutputParamLinked ( param )
          
          if param.display :
            if param.type in self.paramWidgets.keys () :
              #print '%s type = %s' % ( inputParam.label, inputParam.type )
              if isParamLinked :
                if self.showConnected :
                  paramWidget = LinkWidget ( param, self.gfxNode )
                else :
                  continue
              else :
                paramWidget = apply ( self.paramWidgets [ param.type ], [ param, self.gfxNode ] )
              
              frameLayout.addWidget ( paramWidget )
              if not param.enabled :
                paramWidget.setEnabled ( False )
              
              if param.removable :
                QtCore.QObject.connect ( paramWidget, QtCore.SIGNAL ( 'nodeParamRemoved' ), self.nodeParamView.onParamRemoved )
    
        spacer = QtGui.QSpacerItem ( 20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding )
        frameLayout.addItem ( spacer )
        # build a scroll area
        scrollArea = QtGui.QScrollArea ()
        scrollArea.setWidgetResizable ( True )
        scrollArea.setWidget ( frame )
    
        self.stackedWidget.addWidget ( scrollArea )
