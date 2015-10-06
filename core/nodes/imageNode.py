"""

 imageNode.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore

from core.node import Node

from global_vars import app_global_vars, DEBUG_MODE
#
# ImageNode
#
class ImageNode ( Node ) :
	#
	# __init__
	#
	def __init__ ( self, xml_node = None ) :
		#
		Node.__init__ ( self, xml_node )
		
		self.imageName = ''
		if DEBUG_MODE : print ( '>> ImageNode( %s ).__init__' % self.label )
	#
	# copy
	#
	def copy ( self ) :
		#
		if DEBUG_MODE : print ( '>> ImageNode( %s ).copy' % self.label )
		newNode = ImageNode ()
		self.copySetup ( newNode )
		return newNode
	#
	# thisIs
	#
	def thisIs ( self ) :
		#
		this_is = 'image_node'
		if len ( self.outputParams ) == 0:
			this_is = 'image_render_node'
		return this_is
	#
	# computeNode
	#
	def computeNode ( self, CodeOnly = False ) :
		#
		print ( '>> ImageNode( %s ).computeNode' % self.label )
		# inside control_code, imageName value can be assigned from different
		# input parameters
		self.execControlCode ()
		
		return self.imageName
