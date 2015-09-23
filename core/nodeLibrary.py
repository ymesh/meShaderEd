"""

	nodeLibrary.py

"""
from core.mePyQt import QtCore, QtGui, QtXml
#from QtCore import QDir, QFile, QVariant
#from QtGui  import QStandardItemModel, QStandardItem

from global_vars import app_global_vars

from core.node import Node
from core.nodeParam import NodeParam
#
# NodeLibrary
#  
class NodeLibrary ( QtCore.QObject ) : # QtCore.QObject
	#
	# __init__
	#
	def __init__ ( self, dirName ) :
		#
		self.dirName = dirName
		self.libdir = QtCore.QDir ( dirName );
		self.model = 	QtGui.QStandardItemModel ()
		self.parentItem = self.model.invisibleRootItem ()
		
		print '>> NodeLibrary: libdir = %s' % dirName 
		
		self.liblevel = ''
		self.scanLibDir ()
	#    
	# scanLibDir
	#
	def scanLibDir ( self ) :
		# process directories
		sortFlags = QtCore.QDir.Name
		filterFlags = ( QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot )
		fileList = self.libdir.entryInfoList ( filterFlags, sortFlags ) 
		
		for f in fileList :
			item = QtGui.QStandardItem ( f.fileName () )
			item.setEditable ( False )
			item.setDragEnabled ( False )
			
			# set bold font for folders
			font = item.font()
			font.setBold ( True )
			item.setFont ( font )
			
			item.setWhatsThis ( 'folder' )
			
			currparent = self.parentItem
			self.parentItem.appendRow ( item )
			self.parentItem = item
			
			currlevel = self.liblevel # store current level
			self.liblevel = self.liblevel + f.fileName () + '/' 
			self.libdir.cd ( f.fileName () )
			
			self.scanLibDir () # recurcive call itself
			
			self.liblevel = currlevel # restore current level
			self.libdir.cdUp ()
			
			self.parentItem = currparent
				
		# process XML files
		filterFlags = QtCore.QDir.Files    
		fileList = self.libdir.entryInfoList ( [ '*.xml' ], filterFlags, sortFlags ) 
		for f in fileList :
			self.scanXmlNodes ( f.fileName () )
	#
	# scanXmlNodes
	#
	def scanXmlNodes ( self, filename ) :      
		#
		dom = QtXml.QDomDocument ( '' )
		nodeFilename = self.dirName + '/' + self.liblevel + filename
		
		file = QtCore.QFile ( self.libdir.filePath ( filename )  )
		
		if file.open ( QtCore.QIODevice.ReadOnly ) :
			if dom.setContent ( file ) :
				node = dom.documentElement () 
				if node.nodeName () == 'nodenet' or node.nodeName () == 'node' :
					nodeName   = node.attributes ().namedItem ( 'name' ).nodeValue ()
					nodeType   = node.attributes ().namedItem ( 'type' ).nodeValue ()
					nodeAuthor = node.attributes ().namedItem ( 'author' ).nodeValue ()
					nodeIcon   = node.attributes ().namedItem ( 'icon' ).nodeValue ()
					nodeHelp   = ''
					help_tag   = node.namedItem ('help')
					
					if not help_tag.isNull() : nodeHelp = help_tag.toElement ().text ()
					
					item = QtGui.QStandardItem ( nodeName )
					item.setEditable ( False )
					
					item.setData ( QtCore.QVariant ( nodeAuthor ),   QtCore.Qt.UserRole + 1 )
					item.setData ( QtCore.QVariant ( nodeType ),     QtCore.Qt.UserRole + 2 )
					item.setData ( QtCore.QVariant ( nodeHelp ),     QtCore.Qt.UserRole + 3 )
					item.setData ( QtCore.QVariant ( nodeFilename ), QtCore.Qt.UserRole + 4 )
					item.setData ( QtCore.QVariant ( nodeIcon ),     QtCore.Qt.UserRole + 5 )
					
					if node.nodeName () == 'nodenet' :
						# set Blue color for nodenet items
						brush = QtGui.QBrush ()
						brush.setColor ( QtCore.Qt.blue )
						item.setForeground ( brush )
						item.setWhatsThis ( 'nodenet' )
					else:
						item.setWhatsThis ( 'node' )
					
					self.parentItem.appendRow ( item )
		file.close ()
