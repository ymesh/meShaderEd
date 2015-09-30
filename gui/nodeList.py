"""

	nodeList.py

"""
from core.mePyQt import QtCore, QtGui

#from PyQt4.QtCore import QDir, QString, QModelIndex
#from PyQt4.QtGui  import QFileSystemModel
#from PyQt4.QtGui  import QFileIconProvider

from ui_nodeList import Ui_nodeList
#from MainWindow import MainWindow

from core.node import Node
from core.nodeLibrary import NodeLibrary

if QtCore.QT_VERSION < 0x50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
	
#
# NodeList
#
class NodeList ( QtModule.QWidget ) :
	#
	# Define signals for PyQt5
	#
	if QtCore.QT_VERSION >= 0x50000 :
		setActiveNodeList = QtCore.pyqtSignal ( [QtModule.QWidget] )
		addNode = QtCore.pyqtSignal ( [str] )
	#
	# __init__
	#
	def __init__ ( self, parent ) :
		#
		QtModule.QWidget.__init__ ( self, parent )

		self.nodesLib = ''
		self.nodesDir = ''
		# This is always the same
		self.ui = Ui_nodeList () 
		self.ui.setupUi ( self )
		self.ui.treeView.setDragEnabled ( True )
		#self.ui.treeView.setRootIsDecorated( True )
		self.connectSignals ()
		self.updateGui ()
	#
	# connectSignals
	#
	def connectSignals ( self ) :
		#
		if QtCore.QT_VERSION < 0x50000 :
			QtCore.QObject.connect ( self.ui.treeView, QtCore.SIGNAL ( "pressed(QModelIndex)" ), self.clicked )
			QtCore.QObject.connect ( self.ui.treeView, QtCore.SIGNAL ( "doubleClicked(QModelIndex)" ), self.doubleClicked )
		else :
			self.ui.treeView.pressed.connect ( self.clicked )
			self.ui.treeView.doubleClicked.connect ( self.doubleClicked )
	#
	# updateGui
	#
	def updateGui ( self ) :
		#
		if self.nodesLib != '' :
			# self.ui.treeView.setupModel( self.nodesLib.model )
			
			self.ui.treeView.reset ()
			self.ui.treeView.setModel ( self.nodesLib.model ) 
			
			self.ui.infoText.clear ()
			#self.ui.infoText.setText( "<i>Node:</i><br /><i>Author:</i><br />" )
	#
	# setLibrary
	#
	def setLibrary ( self, dirName ) :
		#
		self.nodesDir = dirName
		self.nodesLib = NodeLibrary ( dirName )
		self.updateGui()
	#
	# reloadLibrary
	#
	def reloadLibrary ( self ) :
		#
		print '>> NodeList: reloadLibrary' 
		self.nodesLib = NodeLibrary ( self.nodesDir )
		self.updateGui ()
	#
	# clicked
	#
	def clicked ( self, index ) :
		#
		item = self.nodesLib.model.itemFromIndex ( index ) 
		self.showDescription ( item )
		#
		# send signal to MainWindow to help distinguish which nodeList
		# is active for addNode getNode events
		#
		if QtCore.QT_VERSION < 0x50000 :
			self.emit ( QtCore.SIGNAL ( "setActiveNodeList" ), self )
		else :
			self.setActiveNodeList.emit ( self )
	#      
	# doubleClicked
	#
	def doubleClicked ( self, index ) :
		#
		item = self.nodesLib.model.itemFromIndex ( index )
		nodeKind = item.whatsThis ()
		
		if nodeKind != 'folder' :
			if QtCore.QT_VERSION < 0x50000 :
				nodeFilename = item.data ( QtCore.Qt.UserRole + 4 ).toString ()
				self.emit ( QtCore.SIGNAL ( 'addNode' ), nodeFilename )
			else :
				nodeFilename = item.data ( QtCore.Qt.UserRole + 4 )
				self.addNode.emit ( nodeFilename )
	#    
	# showDescription
	#
	def showDescription ( self, item ) :
		#
		import os
		
		nodeName     = item.text ()
		nodeKind     = item.whatsThis ()
		if QtCore.QT_VERSION < 0x50000 :
			nodeAuthor   = item.data ( QtCore.Qt.UserRole + 1 ).toString ()
			nodeType     = item.data ( QtCore.Qt.UserRole + 2 ).toString ()
			nodeHelp     = item.data ( QtCore.Qt.UserRole + 3 ).toString ()
			nodeFilename = item.data ( QtCore.Qt.UserRole + 4 ).toString ()
			nodeIcon     = item.data ( QtCore.Qt.UserRole + 5 ).toString ()
		else :
			nodeAuthor   = item.data ( QtCore.Qt.UserRole + 1 )
			nodeType     = item.data ( QtCore.Qt.UserRole + 2 )
			nodeHelp     = item.data ( QtCore.Qt.UserRole + 3 )
			nodeFilename = item.data ( QtCore.Qt.UserRole + 4 )
			nodeIcon     = item.data ( QtCore.Qt.UserRole + 5 )
		
		self.ui.infoText.clear ()
		
		description = ''
		
		if nodeKind != 'folder' :
			if nodeIcon != '' :
				iconFileName = os.path.join ( os.path.dirname ( str ( nodeFilename ) ), str ( nodeIcon ) ) 
				print str ( iconFileName )
				description += '<img src="' + iconFileName + '" />'  # width="128" height="128"

			description += "<table>"
			#description += "<tr>"
			#description += "<td align=right>name:</td>"
			#description += "<td><b>" + nodeName + "</b></td>"
			#description += "</tr>"
			#description += "<tr>"
			#description += "<td align=right>type:</td>"
			#description += "<td><b>" + nodeType +"</b></td>"
			#description += "</tr>"
			#description += "<tr>"
			#description += "<td align=right>filename:</td>"
			#description += "<td>" + nodeFilename +"</td>"
			#description += "</tr>"
			description += "<tr>"
			description += "<td align=left>author:</td>"
			description += "<td><i>" + nodeAuthor +"</i></td>"
			description += "</tr>"
			description += "</table><br />"
			
			description += "<br />" + nodeHelp +"</b><br />"
			
			self.ui.infoText.setText ( description )
		
		#self.ui.infoText.clear()
		#self.ui.infoText.setText( "<i>Name:</i>" + nodeName + "<br /><i>Author:</i>" + nodeAuthor +"<br />" )
		#self.ui.infoText.setText( QString("Clicked on %1: ").arg(nodeKind) + item.text() )
