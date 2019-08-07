"""

    nodeTreeView.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

from core.node import Node
from core.nodeLibrary import NodeLibrary
from global_vars import DEBUG_MODE

if not usePyQt5 :
    QtModule = QtGui
else :
    from core.mePyQt import QtWidgets
    QtModule = QtWidgets
#
# NodeTreeView
#
class  NodeTreeView ( QtModule.QTreeView ) :
    #
    # __init__
    #
    def __init__( self, parent = None ):
        #
        QtModule.QTreeView.__init__ ( self, parent )
        self.setMinimumHeight ( 200 )
    #
    # startDrag
    #    
    def startDrag ( self, dropActions ):
        #
        if DEBUG_MODE : print ( '>> NodeTreeView::startDrag' )
        selectedIdx = self.selectedIndexes () 
        # for idx in selectedIdx :
        idx = selectedIdx[ 0 ]
        item = self.model().itemFromIndex( idx ) 
        #print "item = %s" % item.text()
        # set custom data
        data = QtCore.QByteArray ()
        stream = QtCore.QDataStream ( data, QtCore.QIODevice.WriteOnly )
        itemName = item.text ()
        if usePyQt4 :
            itemFilename = item.data( QtCore.Qt.UserRole + 4 ).toString ()
        else :
            itemFilename = item.data( QtCore.Qt.UserRole + 4 )
        if not usePyQt5 :	
            if usePySide :
                stream.writeString ( itemFilename )
            else :
                stream << itemFilename
        else :	
            stream.writeBytes ( itemFilename ) 
        if DEBUG_MODE : print ( '* write itemFilename = %s' % ( itemFilename ) )
        mimeData = QtCore.QMimeData()
        mimeData.setData ( 'application/x-text', data )
        # set drag
        drag = QtGui.QDrag ( self )
        drag.setMimeData ( mimeData )
        #drag.setPixmap ( QtGui.QPixmap(':/node.png') )
        if not usePyQt5 :
            drag.start ( QtCore.Qt.CopyAction )
        else :
            drag.exec_ ( QtCore.Qt.CopyAction )

