#===============================================================================
# nodeLink.py
#
# 
#
#===============================================================================
import os, sys
from PyQt4 import QtCore

from node import Node
from nodeParam import NodeParam
#
# NodeLink
#
class NodeLink ():
  id = 0
  #
  #
  def __init__ ( self, nodenet = None, xml_link = None  ):
    self.id = None
    self.srcNode = None
    self.dstNode = None
    
    self.srcParam = None
    self.dstParam = None
    
    self.nodenet = nodenet
    
    if xml_link != None :
      self.parseFromXML ( xml_link )  
  #
  #
  @classmethod
  def build ( cls, srcNode, dstNode, srcParam, dstParam ):
    link = cls()

    NodeLink.id += 1
    link.id = NodeLink.id
            
    link.srcNode = srcNode
    link.dstNode = dstNode
    
    link.srcParam = srcParam
    link.dstParam = dstParam

    return link  
  #
  #
  def swapNodes ( self ):      
    # swap source and destination
    node = self.srcNode
    param = self.srcParam
    self.srcNode = self.dstNode
    self.srcParam = self.dstParam
    self.dstNode = node
    self.dstParam = param
  #
  #
  def printInfo ( self ) :
    print ':: NodeLink (id = %d) %s.%s -> %s.%s' % ( self.id, self.srcNode.label, self.srcParam.label, self.dstNode.label, self.dstParam.label  )
  #
  #
  #  
  def parseToXML ( self, dom ) :
    #
    xml_link = dom.createElement( "link" )
    
    xml_link.setAttribute ( "id", str( self.id ) )
    xml_link.setAttribute ( "srcNode_id", self.srcNode.id )
    xml_link.setAttribute ( "dstNode_id", self.dstNode.id )
    xml_link.setAttribute ( "srcParam", self.srcParam.name )
    xml_link.setAttribute ( "dstParam", self.dstParam.name )
    
    return xml_link
  #
  #
  #
  def parseFromXML ( self, xml_link ) :
    self.id = int ( xml_link.attributes().namedItem('id').nodeValue() )
    #print '-> parsing from XML link id = %d' % ( self.id ) 
    srcNode_id = int ( xml_link.attributes().namedItem('srcNode_id').nodeValue() )
    dstNode_id = int ( xml_link.attributes().namedItem('dstNode_id').nodeValue() )  
    self.srcNode = self.nodenet.nodes[ srcNode_id ]
    self.dstNode = self.nodenet.nodes[ dstNode_id ]
    srcParam_name = str ( xml_link.attributes().namedItem('srcParam').nodeValue() )
    dstParam_name = str ( xml_link.attributes().namedItem('dstParam').nodeValue() )
    self.srcParam = self.srcNode.getOutputParamByName ( srcParam_name )
    self.dstParam = self.dstNode.getInputParamByName ( dstParam_name )
    
    #self.printInfo ()