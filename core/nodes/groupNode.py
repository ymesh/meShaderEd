#===============================================================================
# groupNode.py
#===============================================================================
import os, sys
from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from core.nodeNetwork import NodeNetwork
from global_vars import app_global_vars, DEBUG_MODE

import gui.ui_settings as UI

#
# GroupNode
#
class GroupNode ( Node ) :
  #
  # __init__
  #
  def __init__ ( self, xml_node = None ) :
    #
    Node.__init__ ( self, xml_node )
    
    if xml_node is None :
      self.type = 'nodegroup'
      self.name = self.label = self.type
      self.nodenet = NodeNetwork ()

    if DEBUG_MODE : print '>> GroupNode( %s ).__init__' % self.label
  #
  # copy
  #
  def copy ( self ) :
    if DEBUG_MODE : print '>> GrouphNode( %s ).copy' % self.label
    newNode = GroupNode ()
    self.copySetup ( newNode )
    return newNode
  #
  # copySetup
  #
  def copySetup ( self, newNode ) :
    #
    if DEBUG_MODE : print '>> GrouphNode( %s ).copySetup ' % self.label
    Node.copySetup ( self, newNode )
    newNode.nodenet = self.nodenet.copy ()
  #
  # computeNode
  #
  def computeNode ( self ) :
    #
    if DEBUG_MODE : print '>> GroupNode( %s ).computeNode' % self.label
    # inside param_code, imageName value can be assigned from different
    # input parameters
    self.execParamCode ()

