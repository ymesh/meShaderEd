"""

	geomNode.py
	
"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore

from core.node import Node

from global_vars import app_global_vars, DEBUG_MODE
#
# GeomNode
#
class GeomNode ( Node ) :
	#
	# __init__
	#
	def __init__ ( self, xml_node = None ) :
		#
		Node.__init__( self, xml_node )
		
		self.imageName = ''
		
		print ( ">> GeomNode __init__" )
	#
	# copy
	#
	def copy ( self ) :
		#
		if DEBUG_MODE : print ( '>> GeomNode( %s ).copy' % self.label )
		newNode = GeomNode ()
		self.copySetup ( newNode )
		return newNode
	#
	# computeNode
	#
	def computeNode ( self ) :
		#
		print ( '>> GeomNode( %s ).computeNode' % self.label )
		#
		# inside param_code, imageName value can be assigned from different  
		# input parameters
		
		self.execParamCode ()
		
		return self.imageName
