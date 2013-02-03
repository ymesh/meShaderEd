#===============================================================================
# noteNode.py
#
# 
#
#===============================================================================
import os, sys
from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# ImageNode
#
class NoteNode( Node ):
  #
  #
  def __init__ ( self, xml_node = None ):
    #
    Node.__init__( self, xml_node )
    if DEBUG_MODE : print ">> NoteNode __init__" 
  #
  #
  def copy ( self ):
    if DEBUG_MODE : print '>> NoteNode::copy (%s)' % self.label
    newNode = NoteNode()
    self.copySetup ( newNode )                                
    return newNode   
  #
  #
  def computeNode ( self ) :
    print '>> NoteNode (%s).computeNode' % self.label
