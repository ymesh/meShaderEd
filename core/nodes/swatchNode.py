"""

	swatchNode.py

"""
from core.mePyQt import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from core.nodes.imageNode import ImageNode

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI
#
# SwatchNode
#
class SwatchNode ( ImageNode ) :
	#
	# __init__
	#
	def __init__ ( self, xml_node = None ) :
		#
		ImageNode.__init__ ( self, xml_node )
		
		self.size = UI.SWATCH_SIZE  
		if DEBUG_MODE : print '>> SwatchNode( %s ).__init__' % self.label
	#
	# copy
	#
	def copy ( self ) :
		#
		if DEBUG_MODE : print '>> SwatchNode( %s ).copy' % self.label
		newNode = SwatchNode ()
		self.copySetup ( newNode )
		return newNode
	#
	# computeNode
	#
	def computeNode ( self ) :
		#
		if DEBUG_MODE : print '>> SwatchNode( %s ).computeNode' % self.label
		# inside control_code, imageName value can be assigned from different
		# input parameters
		self.execControlCode ()
		return self.imageName
