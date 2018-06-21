"""

 nodeNetwork.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtXml

from node import *

from nodes.rslNode				import RSLNode
from nodes.ribNode				import RIBNode
from nodes.imageNode			import ImageNode
from nodes.connectorNode	import ConnectorNode
from nodes.noteNode				import NoteNode
from nodes.swatchNode			import SwatchNode
from nodes.geomNode 			import GeomNode

from nodeParam import NodeParam
from nodeLink import NodeLink

from global_vars import DEBUG_MODE
#
# NodeNetwork
#
class NodeNetwork ( QtCore.QObject ) :
	#
	#  __init__
	#
	def __init__ ( self, name = '', xml_nodenet = None ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).__init__ ' % name )
		QtCore.QObject.__init__ ( self )

		self.node_id = 0
		self.link_id = 0

		self.name = name
		self.fileName = ''

		self.help = 'Short NodeNetwork description'

		self.isDirty = False

		self.nodes = {}
		self.links = {}

		if xml_nodenet != None : 
			self.parseFromXML ( xml_nodenet )
	#
	# __del__
	#
	def __del__ ( self ) :
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).__del__ ' % self.name )
	#
	# getName
	#
	def getName ( self ) : return self.name
	#
	# copy
	#
	def copy ( self ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).copy ' % self.name )
		newNode = NodeNetwork ()
		self.copySetup ( newNode )
		return newNode
	#
	# copySetup
	#
	def copySetup ( self, newNode ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).copySetup ' % self.label )

		newNode.node_id = self.node_id
		newNode.link_id = self.link_id

		newNode.name = self.name
		newNode.fileName = self.fileName

		newNode.help = self.help

		newNode.isDirty = self.isDirty

		newNode.nodes = {}
		newNode.links = {}

	#
	# renameNodeLabel
	#
	def renameNodeLabel ( self, node, newLabel ) :
		# assign new unique label to node
		from meCommon import getUniqueName
		labels = []
		for nd in self.getNodesList () : labels.append ( nd.label )
		node.label = getUniqueName ( newLabel, labels )
		return node.label
	#
	# renameNodeName
	#
	def renameNodeName ( self, node, newName ) :
		# assign new unique label to node
		from meCommon import getUniqueName
		names = []
		for nd in self.getNodesList () : names.append ( nd.name )
		node.name = getUniqueName ( newName, names )
		return node.name
	#
	# get list of nodes
	#
	def getNodesList ( self ) : return self.nodes.values ()
	#
	# get list of links
	#
	def getLinksList ( self ) : return self.links.values ()
	#
	# addNode
	#
	def addNode ( self, node ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).addNode (%s)' % ( self.name, node.label ) )
		if node.id == None :
			# if node comes from library -- it should have id = None
			self.node_id = self.node_id + 1
			node.id = self.node_id
		else :
			# while importing from other NodeNet
			node.id = self.node_id + node.id

		if DEBUG_MODE : print '** node.id -> %d' % node.id

		# check if node with this label already exists and assign new label
		self.renameNodeLabel ( node, node.label )

		if node.id in self.nodes :
			# print '!!! node.id %d already exists !!!' % node.id
			while node.id in self.nodes : node.id += 1
			if DEBUG_MODE : print '!! node.id changed to %d' % node.id

		# add node to NodeNetwork
		self.nodes [ node.id ] = node
		node.nodenet = self
	#
	# addLink
	#
	def addLink ( self, link ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s )::addLink (id = %d)' % ( self.name, link.id ) )
		if link.id == None :
			self.link_id = self.link_id + 1
			link.id = self.link_id
		else :
			# while importing from other NodeNet
			link.id = self.link_id + link.id

		if DEBUG_MODE : print ( '** link.id -> %d' % link.id )

		if link.id in self.links :
			# print '!!! link.id %d already exists !!!' % link.id
			while link.id in self.links : link.id += 1
			if DEBUG_MODE : print ( '!! link.id changed to %d' % link.id )

		# add link to NodeNetwork
		self.links [ link.id ] = link
		link.nodenet = self

		# attach link to nodes
		link.connect ()
		#if connectSrcNode :
		#  link.srcNode.attachOutputParamToLink ( link.srcParam, link )
		#if connectDstNode :
		#  link.dstNode.attachInputParamToLink ( link.dstParam, link )

		# add child (since it is a set no duplicates allowed)
		if DEBUG_MODE : print ( '** add child %s to %s ' % ( link.srcNode.label, link.dstNode.label ) )
		link.dstNode.addChild ( link.srcNode )
	#
	# removeNode
	#
	def removeNode ( self, node ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).removeNode %s (id = %d) ...' % ( self.name, node.name, node.id ) )
		inputLinksToRemove = []
		outputLinksToRemove = []
		if self.hasThisNode ( node ) :
			nodePopped = self.nodes.pop ( node.id )
			node.nodenet = None
			inputLinksToRemove = nodePopped.getInputLinks ()
			outputLinksToRemove = nodePopped.getOutputLinks ()
		return ( inputLinksToRemove, outputLinksToRemove )
	#
	# removeLink
	#
	def removeLink ( self, link, disconnectSrcNode = True, disconnectDstNode = True ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).removeLink (id = %d) ...' % ( self.name, link.id ) )
		if self.hasThisLink ( link ) :
			linkPopped = self.links.pop ( link.id )
			dstNode = linkPopped.dstNode
			srcNode = linkPopped.srcNode
			# detach nodes from link
			linkPopped.remove ()
			# check if we can remove a child from destination node
			sourceNodeReferenceCount = 0
			for inputLink in dstNode.inputLinks.values () :
				if inputLink.srcNode == srcNode :
					sourceNodeReferenceCount += 1
			if sourceNodeReferenceCount == 0 :
				if srcNode in dstNode.childs :
					dstNode.removeChild ( srcNode )
			
	#
	# hasThisLink
	#
	def hasThisLink ( self, link ) : return ( link.id in self.links.keys () ) and ( link.nodenet == self )
	#
	# hasThisNode
	#
	def hasThisNode ( self, node ) : return ( node.id in self.nodes.keys () ) and ( node.nodenet == self )
	#
	# clear
	#
	def clear ( self ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).clear' % ( self.name ) )
		#
		for node in self.nodes.values() : self.removeNode ( node )
		for link in self.links.values() : self.removeLink ( link )

		self.nodes = {}
		self.links = {}

		self.node_id = 0
		self.link_id = 0
	#
	# getNodeByName
	#
	# def getNodeByName ( self, nodeName ) :
	#  for node in self.nodes.values () :
	#    if node.name == nodeName:
	#      return node
	#  return None

	#
	# getNodeByID
	#
	def getNodeByID ( self, id ) :
		#
		node = None
		if id in self.nodes.keys () : node = self.nodes [ id ]
		return node
	#
	# parseToXML
	#
	def parseToXML ( self, dom ) :
		#
		if DEBUG_MODE : print ( '>> NodeNetwork( %s ).parseToXML ...' % self.name )
		root = dom.createElement ( 'nodenet' )
		root.setAttribute ( 'name', self.name )
		root.setAttribute ( 'author', 'meShaderEd' )

		# append network help (short description)
		help_tag = dom.createElement ( 'help' )
		help_text = dom.createTextNode ( self.help )
		help_tag.appendChild ( help_text )
		root.appendChild ( help_tag )

		nodes_tag = dom.createElement ( 'nodes' )

		#print ':: parsing nodes to XML ...'
		for id in self.nodes.keys () :
			node = self.nodes [ id ]
			if DEBUG_MODE : print ( '=> parsing node ( %s ) to XML ...' % node.label )
			xml_node = node.parseToXML ( dom )
			nodes_tag.appendChild ( xml_node )

		root.appendChild ( nodes_tag )

		links_tag = dom.createElement ( 'links' )

		#print ':: parsing links to XML ...'
		for id in self.links.keys() :
			link = self.links [ id ]
			# print '=> parsing link to XML ...'
			# link.printInfo ()
			xml_link = link.parseToXML ( dom )
			links_tag.appendChild ( xml_link )

		root.appendChild ( links_tag )
		dom.appendChild ( root )
	#
	# parseFromXML
	#
	def parseFromXML ( self, root ) :
		#
		print ( '>> NodeNetwork.parseFromXML ...' )
		#print root.nodeType ()
		self.name = str ( root.attributes ().namedItem ( 'name' ).nodeValue () )
		self.author = str ( root.attributes ().namedItem ( 'author' ).nodeValue () )
		
		nodes_tag = root.elementsByTagName ( 'nodes' )
		for i in range ( 0, nodes_tag.length () ) :
			xml_nodes = nodes_tag.item ( i )	
			xml_nodeList = xml_nodes.childNodes ()
			for i in range ( 0, xml_nodeList.length () ) :
				xml_node = xml_nodeList.item ( i )
				if xml_node.nodeName() == 'node' :
					node = self.addNodeFromXML ( xml_node )
					print ( ':: node = %s' %  node.name )
		
		links_tag = root.elementsByTagName ( 'links' )
		for i in range ( 0, links_tag.length () ) :
			xml_links = links_tag.item ( i )	
			xml_linkList = xml_links.childNodes ()
			for i in range ( 0, xml_linkList.length () ) :
				xml_link = xml_linkList.item ( i )
				if xml_link.nodeName() == 'link' :
					link = NodeLink ( self, xml_link )
					self.addLink ( link )
					#link.printInfo ()
	#
	# addNodeFromXML
	#
	def addNodeFromXML ( self, xml_node ) :
		#
		node = createNodeFromXML ( xml_node )
		self.addNode ( node )
		return node
	#
	# save NodeNetwork to .xml document
	#
	def save ( self ) :
		#
		result = False

		dom = QtXml.QDomDocument ( self.name )
		self.parseToXML ( dom )

		file = QtCore.QFile ( self.fileName )
		if file.open ( QtCore.QIODevice.WriteOnly ) :
			if file.write ( dom.toByteArray () ) != -1 :
				result = True
		file.close()
		return result
	#
	# open NodeNetwork from .xml document
	#
	def open ( self, fileName ) :
		#
		nodes = []
		links = []

		dom = QtXml.QDomDocument ( self.name )

		file = QtCore.QFile ( fileName )
		if file.open ( QtCore.QIODevice.ReadOnly ) :
			if dom.setContent ( file )  :
				self.fileName = fileName
				root = dom.documentElement ()
				if root.nodeName () == 'node' :
					#print ':: parsing node from XML ...'
					nodes.append ( self.addNodeFromXML ( root ) )
				elif root.nodeName () == 'nodenet' :
					#print ':: parsing nodenet from XML ...'
					self.parseFromXML ( root )
					nodes = self.getNodesList ()
					links = self.getLinksList ()
				else :
					print '!! unknown XML document format'
				self.correct_id ( nodes, links )
		file.close()
		#if DEBUG_MODE : print '>> NodeNetwork( %s ).open node_id = %d link_id = %d' % ( self.name, self.node_id, self.link_id )
		#if DEBUG_MODE : self.printInfo ()
		return ( nodes, links )
	#
	# insert NodeNetwork from .xml document
	#
	def insert ( self, fileName ) :
		#
		nodes = []
		links = []

		dom = QtXml.QDomDocument ( self.name )

		file = QtCore.QFile ( fileName )
		if file.open ( QtCore.QIODevice.ReadOnly ) :
			if dom.setContent ( file )  :
				root = dom.documentElement ()
				if root.nodeName () == 'node' :
					#print ':: parsing node from XML ...'
					nodes.append ( self.addNodeFromXML ( root ) )
					self.correct_id ( nodes, links )
				elif root.nodeName () == 'nodenet' :
					#print ':: parsing nodenet from XML ...'
					nodeNet = NodeNetwork ( 'tmp', root )
					nodeNet.fileName = fileName
					( nodes, links ) = self.add ( nodeNet )
				else :
					print ( '!! unknown XML document format' )
		file.close ()
		#if DEBUG_MODE : print '>> NodeNetwork( %s ).insert node_id = %d link_id = %d' % ( self.name, self.node_id, self.link_id )
		#if DEBUG_MODE : self.printInfo ()
		return ( nodes, links )
	#
	# correct currnet NodeNetwork node_id and link_id
	# according to max id values from opened network
	#
	def correct_id ( self, nodes, links ) :
		#
		max_node_id = 0
		for node in nodes : max_node_id = max ( max_node_id, node.id )

		max_link_id = 0
		for link in links : max_link_id = max ( max_link_id, link.id )

		self.node_id =  max_node_id
		self.link_id =  max_link_id
	#
	# add NodeNetwork
	#
	def add ( self, nodeNet ) :
		#
		nodes = nodeNet.getNodesList ()
		links = nodeNet.getLinksList ()
		for node in nodes : self.addNode ( node )
		for link in links : self.addLink ( link )
		self.correct_id ( nodes, links )
		return ( nodes, links )
	
	#
	# printInfo
	#
	def printInfo ( self ) :
		#
		print ( '>> NodeNetwork( %s ).printInfo' % ( self.name ) )
		print ( '*** links ***' )
		for id in self.links.keys () : self.links [ id ].printInfo ()
		print ( '*** nodes ****' )
		for id in self.nodes.keys () : self.nodes [ id ].printInfo ()
#
# createNodeFromXML
#
def createNodeFromXML ( xml_node ) :
	#
	node_type = str ( xml_node.attributes ().namedItem ( 'type' ).nodeValue () )
	node_format = str ( xml_node.attributes ().namedItem ( 'format' ).nodeValue () )
	node_version = str ( xml_node.attributes ().namedItem ( 'version' ).nodeValue () )
	#
	# try to convert from old format nodes
	#
	if node_type != 'nodegroup' :
	if node_version == '' or node_version is None :
		if node_format == '' or node_format is None :
			( node_type, node_format ) = translateOldType ( node_type )
	node = None
	createNode = None
	if node_type == 'node' : 
		if node_format == 'rsl' :
			createNode = RSLNode
		elif node_format == 'rib' :
			createNode = RIBNode
		elif node_format == 'image' :
			createNode = ImageNode
		elif node_format == 'geom' :
			createNode = GeomNode
	elif node_type == 'connector' :
		createNode = ConnectorNode
	elif node_type == 'note' :
		createNode = NoteNode  
	elif node_type == 'swatch' :
		createNode = SwatchNode 
	elif node_type == 'nodegroup' :
		from nodeGroup import NodeGroup
		createNode = NodeGroup
	elif node_type == 'variable' :
		if node_format == 'rsl' :
			createNode = RSLNode  

	if createNode is not None :
		node = createNode ( xml_node )
	else :
		print ( 'Unknown node type or format! (type=%s format=%s)' % (node_type, node_format)  )
	return node
