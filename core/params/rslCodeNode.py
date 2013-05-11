#===============================================================================
# rslCodeNode.py
#===============================================================================
import os, sys
from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam

from global_vars import app_global_vars, DEBUG_MODE
from core.node_global_vars import node_global_vars
#
# RSLCodeNode
#
class RSLCodeNode ( Node ) :
  #
  # __init__
  #
  def __init__ ( self, xml_node = None ) :
    #
    Node.__init__ ( self, xml_node )
    self.shaderName = ''
  #
  # copy
  #
  def copy ( self ) :
    if DEBUG_MODE : print '>> RSL_code( %s ).copy' % self.label
    newNode = RSLCodeNode ()
    self.copySetup ( newNode )
    return newNode