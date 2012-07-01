#===============================================================================
# nodeTreeView.py
#
# 
#
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import QDir, QString, QModelIndex
from PyQt4.QtGui  import QFileSystemModel
from PyQt4.QtGui  import QFileIconProvider

from core.node import Node
from core.nodeLibrary import NodeLibrary
#
#
#
class  NodeTreeView ( QtGui.QTreeView ):
  #
  #
  def __init__( self, parent = None ):
    #print ">> NodeTreeWidget init"
    QtGui.QTreeView.__init__ ( self, parent )
    self.setMinimumHeight ( 200 )
  #
  #    
  def startDrag ( self, dropActions ):
    #print ">> NodeTreeView startDrag "
    selectedIdx = self.selectedIndexes () 
    # for idx in selectedIdx :
    idx = selectedIdx[ 0 ]
    item = self.model().itemFromIndex( idx ) 
    #print "item = %s" % item.text()

    itemName = item.text()
    itemFilename = item.data( QtCore.Qt.UserRole + 4 ).toString()
    
    # set custom data
    data = QtCore.QByteArray ()
    stream = QtCore.QDataStream ( data, QtCore.QIODevice.WriteOnly )
    stream << itemFilename
    mimeData = QtCore.QMimeData()
    mimeData.setData ( 'application/x-text', data )
    
    # set drag
    drag = QtGui.QDrag ( self )
    drag.setMimeData ( mimeData )
    #drag.setPixmap ( QtGui.QPixmap(':/node.png') )
    drag.start ( QtCore.Qt.CopyAction )

