#===============================================================================
# imageNode.py
#===============================================================================
import os, sys
from PyQt4 import QtCore

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
    if DEBUG_MODE : print '>> ImageNode( %s ).__init__' % self.label
  #
  # copy
  #
  def copy ( self ) :
    #
    if DEBUG_MODE : print '>> ImageNode( %s ).copy' % self.label
    newNode = ImageNode ()
    self.copySetup ( newNode )
    return newNode
  #
  # computeNode
  #
  def computeNode ( self ) :
    #
    print '>> ImageNode( %s ).computeNode' % self.label
    # inside param_code, imageName value can be assigned from different
    # input parameters
    self.execParamCode ()
    return self.imageName
