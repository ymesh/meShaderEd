#===============================================================================
# coonectorNode.py
#===============================================================================
import os, sys
from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# ImageNode
#
class ConnectorNode( Node ) :
  #
  # __init__
  #
  def __init__ ( self, xml_node = None ) :
    #
    Node.__init__( self, xml_node )
    if xml_node is None :
      self.type = 'connector'
      self.name = self.label = self.type
    if DEBUG_MODE : print ">> ConnectorNode( %s ).__init__" % self.label
  #
  # copy
  #
  def copy ( self ) :
    #
    if DEBUG_MODE : print '>> ConnectorNode( %s ).copy' % self.label
    newNode = ConnectorNode ()
    self.copySetup ( newNode )
    return newNode
  #
  # computeNode
  #
  def computeNode ( self ) :
    #
    print '>> ConnectorNode( %s ).computeNode (dummy call)' % self.label
