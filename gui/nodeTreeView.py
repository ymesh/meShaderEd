"""

	nodeTreeView.py

"""
from core.mePyQt import QtCore, QtGui, Qt

#from PyQt4.QtCore import QDir, QString, QModelIndex
#from PyQt4.QtGui  import QFileSystemModel
#from PyQt4.QtGui  import QFileIconProvider

from core.node import Node
from core.nodeLibrary import NodeLibrary

if QtCore.QT_VERSION < 50000 :
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
		#print ">> NodeTreeWidget init"
		QtModule.QTreeView.__init__ ( self, parent )
		self.setMinimumHeight ( 200 )
	#
	# startDrag
	#    
	def startDrag ( self, dropActions ) :
		#print ">> NodeTreeView startDrag "
		selectedIdx = self.selectedIndexes () 
		# for idx in selectedIdx :
		idx = selectedIdx[ 0 ]
		item = self.model().itemFromIndex( idx ) 
		#print "item = %s" % item.text()

		# set custom data
		data = QtCore.QByteArray ()
		stream = QtCore.QDataStream ( data, QtCore.QIODevice.WriteOnly )
		
		itemName = item.text ()
		if QtCore.QT_VERSION < 50000 :
			itemFilename = item.data( QtCore.Qt.UserRole + 4 ).toString ()
			stream << itemFilename
		else :
			itemFilename = item.data( QtCore.Qt.UserRole + 4 )
			stream.writeBytes ( itemFilename  )
		
		mimeData = QtCore.QMimeData()
		mimeData.setData ( 'application/x-text', data )
		
		# set drag
		drag = QtGui.QDrag ( self )
		drag.setMimeData ( mimeData )
		#drag.setPixmap ( QtGui.QPixmap(':/node.png') )
		if QtCore.QT_VERSION < 50000 :
			drag.start ( QtCore.Qt.CopyAction )
		else :
			drag.exec_ ( QtCore.Qt.CopyAction )

