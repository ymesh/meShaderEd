"""
	
	noteNode.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# NoteNode
#
class NoteNode( Node ) :
	#
	# __init__
	#
	def __init__ ( self, xml_node = None ) :
		#
		Node.__init__( self, xml_node )
		if DEBUG_MODE : print ( '>> NoteNode( %s ).__init__' % self.label )
	#
	# __del__
	#
	def __del__ ( self ) :
		print ( '>>> NoteNode( %s ).__del__' % ( self.node.label ))
	#
	# copy
	#
	def copy ( self ) :
		if DEBUG_MODE : print ( '>> NoteNode( %s ).copy' % self.label )
		newNode = NoteNode ()
		self.copySetup ( newNode )
		return newNode   
	#
	# computeNode
	#
	def computeNode ( self ) :
		print ( '>> NoteNode (%s).computeNode' % self.label )
