#===============================================================================
# nodeLink.py
#
# 
#
#===============================================================================
import os, sys
from core.mePyQt import QtCore

from global_vars import app_global_vars, DEBUG_MODE
from node import Node
from nodeParam import NodeParam
#
# NodeLink
#
class NodeLink () :
  id = 0
  #
  # __init__
  #
  def __init__ ( self, nodenet = None, xml_link = None  ) :
    #
    self.id = None
    self.srcNode = None
    self.dstNode = None
    
    self.srcParam = None
    self.dstParam = None
    
    self.nodenet = nodenet
    self.display = True
    
    if xml_link != None : self.parseFromXML ( xml_link )
  #
  # __del__
  #
  def __del__ ( self ) :
    if DEBUG_MODE : print '>> NodeLink( id = %s ).__del__ ' % str ( self.id )  
  #
  # build
  #
  @classmethod
  def build ( cls, srcNode, dstNode, srcParam, dstParam, display = True ) :
    #
    link = cls ()
    NodeLink.id += 1
    link.id = NodeLink.id
    link.setSrc ( srcNode, srcParam )
    link.setDst ( dstNode, dstParam )
    link.display = display
    return link 
  #
  # copySetup
  #
  def copySetup ( self, newLink ) :
    #
    newLink.id = self.id
    newLink.srcNode = self.srcNode
    newLink.dstNode = self.dstNode
    newLink.srcParam = self.srcParam
    newLink.dstParam = self.dstParam
    newLink.display = self.display
    newLink.nodenet = None # self.nodenet 
  #
  # copy
  #
  def copy ( self ) :
    #
    if DEBUG_MODE : print '>> NodeLink( id = %s ).copy' % str ( self.id )  
    newLink = NodeLink ()
    self.copySetup ( newLink )
    return newLink   
  #
  # connect
  #
  def connect ( self ) : 
    #
    if DEBUG_MODE : print '>> NodeLink( id = %s ).connect ...' % str ( self.id )  
    ( srcNode, srcParam ) = self.getSrc ()
    ( dstNode, dstParam ) = self.getDst ()
    
    if self.nodenet.hasThisNode ( srcNode ) : 
      if DEBUG_MODE : print '** to src ( %s )->( %s )' % ( srcNode.label, srcParam.label )
      srcNode.attachOutputParamToLink ( srcParam, self )
    if self.nodenet.hasThisNode ( dstNode ) :
      if DEBUG_MODE : print '** to dst ( %s )->( %s )' % ( dstNode.label, dstParam.label ) 
      dstNode.attachInputParamToLink ( dstParam, self )
  #
  # remove
  #
  def remove ( self ) : 
    #
    if DEBUG_MODE : print '>> NodeLink( id = %d ).remove ...' % self.id
    ( srcNode, srcParam ) = self.getSrc ()
    ( dstNode, dstParam ) = self.getDst ()
    
    if self.nodenet.hasThisNode ( srcNode ) :
      if DEBUG_MODE : print '** from src ( %s )->( %s )' % ( srcNode.label, srcParam.label ) 
      srcNode.detachOutputParamFromLink ( srcParam, self )
    if self.nodenet.hasThisNode ( dstNode ) :
      if DEBUG_MODE : print '** from dst ( %s )->( %s )' % ( dstNode.label, dstParam.label )  
      dstNode.detachInputParam ( dstParam )
    
    self.setSrc ( None, None )
    self.setDst ( None, None )
    self.nodenet = None
    #self.id = None
  #
  # swapNodes
  #
  def swapNodes ( self ) :      
    # swap source and destination
    ( node, param ) = self.getSrc ()
    self.setSrc ( self.dstNode, self.dstParam )
    self.setDst ( node, param )
  #
  # getSrc
  #
  def getSrc ( self ) : return ( self.srcNode, self.srcParam )
  #
  # getSrc
  #
  def getDst ( self ) : return ( self.dstNode, self.dstParam )
  #
  # setDst
  #
  def setDst ( self, node, param ) :      
    # 
    self.dstNode = node
    self.dstParam = param
  #
  # setSrc
  #
  def setSrc ( self, node, param ) :      
    # 
    self.srcNode = node
    self.srcParam = param
  #
  # setDstByParamName
  #
  def setDstByParamName ( self, node, name ) : self.setDst ( node, node.getInputParamByName ( name ) )
  #
  # setSrcByParamName
  #
  def setSrcByParamName ( self, node, name ) : self.setSrc ( node, node.getOutputParamByName ( name ) )
  #
  # printInfo
  #
  def printInfo ( self ) :
    print ':: NodeLink( id = %d ) %s.%s -> %s.%s' % ( self.id, self.srcNode.label, self.srcParam.label, self.dstNode.label, self.dstParam.label  )
  #
  # parseToXML
  #  
  def parseToXML ( self, dom ) :
    #
    xml_link = dom.createElement ( 'link' )
    xml_link.setAttribute ( 'id', str ( self.id ) )
    xml_link.setAttribute ( 'srcNode_id', self.srcNode.id )
    xml_link.setAttribute ( 'dstNode_id', self.dstNode.id )
    xml_link.setAttribute ( 'srcParam', self.srcParam.name )
    xml_link.setAttribute ( 'dstParam', self.dstParam.name )
    
    return xml_link
  #
  # parseFromXML
  #
  def parseFromXML ( self, xml_link ) :
    #
    self.id    = int ( xml_link.attributes ().namedItem ( 'id' ).nodeValue () )
    srcNode_id = int ( xml_link.attributes ().namedItem ( 'srcNode_id' ).nodeValue () )
    dstNode_id = int ( xml_link.attributes ().namedItem ( 'dstNode_id' ).nodeValue () )  
    self.srcNode  = self.nodenet.nodes [ srcNode_id ]
    self.dstNode  = self.nodenet.nodes [ dstNode_id ]
    srcParam_name = str ( xml_link.attributes ().namedItem ( 'srcParam' ).nodeValue () )
    dstParam_name = str ( xml_link.attributes ().namedItem ( 'dstParam' ).nodeValue () )
    self.srcParam = self.srcNode.getOutputParamByName ( srcParam_name )
    self.dstParam = self.dstNode.getInputParamByName ( dstParam_name )
    #self.printInfo ()