"""

 nodeGroup.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore

from core.node import Node
from core.nodeParam import NodeParam
from core.nodeNetwork import NodeNetwork
from global_vars import app_global_vars, DEBUG_MODE

import gui.ui_settings as UI
#
# NodeGroup
#
class NodeGroup ( Node ) :
	#
	# __init__
	#
	def __init__ ( self, xml_node = None ) :
		#
		self.nodenet = None
		self.state = 'closed' # 'closed' 'open'
		
		Node.__init__ ( self, xml_node )
		
		if xml_node != None :
			self.parseFromXML ( xml_node )
		else :
			self.type = 'nodegroup'
			self.name = self.label = self.type
			self.nodenet = NodeNetwork ( self.name )
		
		if DEBUG_MODE : print ( '>> NodeGroup( %s ).__init__' % self.label )
	#
	# copy
	#
	def copy ( self ) :
		#
		if DEBUG_MODE : print ( '>> NodeGroup( %s ).copy' % self.label )
		newNode = NodeGroup ()
		self.copySetup ( newNode )
		return newNode
	#
	# copySetup
	#
	def copySetup ( self, newNode ) :
		#
		if DEBUG_MODE : print ( '>> NodeGroup( %s ).copySetup ' % self.label )
		Node.copySetup ( self, newNode )
		newNode.nodenet = self.nodenet.copy ()
		newNode.state = self.state
	#
	# computeNode
	#
	def computeNode ( self ) :
		#
		if DEBUG_MODE : print ( '>> NodeGroup( %s ).computeNode' % self.label )
		self.execControlCode ()
	#
	# parseFromXML
	#
	def parseFromXML ( self, xml_node ) :
		#
		print ( '>> NodeGroup.parseFromXML ...' )
		Node.parseFromXML ( self, xml_node )
		xml_nodenet = xml_node.namedItem ( 'nodenet' )
		if not xml_nodenet.isNull () :
			print ( ':: NodeNetwork available ! (%s)' % str ( xml_nodenet.nodeName () )  )
			#print xml_node.nodeType ()
			#print xml_nodenet.nodeType ()
			self.nodenet = NodeNetwork ( self.name, xml_nodenet.toElement () )
	#
	# parseToXML
	#
	def parseToXML ( self, dom ) :
		#
		pass
