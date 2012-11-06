#===============================================================================
# nodeNetwork.py
#
# 
#
#===============================================================================
import os, sys

from PyQt4 import QtCore, QtXml
from PyQt4.QtCore import QDir, QFile, QVariant

from node import *
from rslNode import RSLNode
from ribCodeNode import RIBCodeNode
from ribNode import RIBNode
from imageNode import ImageNode

from nodeParam import NodeParam
from nodeLink import NodeLink

from global_vars import DEBUG_MODE
#
# NodeNetwork
# 
class NodeNetwork ( QtCore.QObject ):
  #
  #  
  def __init__ ( self, name = '', xml_nodenet = None ):
    if DEBUG_MODE : print '>> NodeNetwork: __init__ ' + name
    QtCore.QObject.__init__( self )
    
    self.node_id = 0       
    self.link_id = 0
    
    self.name = name
    self.fileName = ''
    
    self.help = 'Short NodeNetwork description'
    
    self.isDirty = False
    
    self.nodes = {}
    self.links = {}
    
    if xml_nodenet != None :
      self.parseFromXML ( xml_nodenet )

  #
  #
  def renameNodeLabel ( self, node, newLabel ):
    # assign new unique label to node
    from meCommon import getUniqueName
    labels = []
    for nd in self.getNodesList () : labels.append ( nd.label )
    node.label = getUniqueName ( newLabel, labels )
    return node.label
  #
  #
  def renameNodeName ( self, node, newName ):
    # assign new unique label to node
    from meCommon import getUniqueName
    names = []
    for nd in self.getNodesList () : names.append ( nd.name )
    node.name = getUniqueName ( newName, names )
    return node.name
  #
  # get list of nodes
  #
  def getNodesList ( self ) : return self.nodes.values()
  #
  # get list of links
  #
  def getLinksList ( self ) : return self.links.values()  
  #
  #    
  def addNode ( self, node ):
    #print '>> NodeNetwork: adding node ' + node.label
    if node.id == None :
      # if node comes from library -- it should have id = None 
      self.node_id = self.node_id + 1
      node.id = self.node_id
    else :
      # while importing from other NodeNet
      node.id = self.node_id + node.id   
      
    # check if node with this label already exists and assign new label
    self.renameNodeLabel ( node, node.label )
    # add node to NodeNetwork
    self.nodes[ node.id ] = node
  #
  #    
  def addLink ( self, link ):
    #print '>> NodeNetwork: adding link'
    if link.id == None :
      self.link_id = self.link_id + 1
      link.id = self.link_id
    else :
      # while importing from other NodeNet
      link.nodenet = self
      link.id = self.link_id + link.id  
    
    # add link to NodeNetwork
    self.links[ link.id ] = link
    
    # attach link to nodes
    link.srcNode.attachOutputParamToLink ( link.srcParam, link )
    link.dstNode.attachInputParamToLink ( link.dstParam, link )
    
    # add child (since it is a set no duplicates allowed)
    link.dstNode.childs.add ( link.srcNode )
  #
  #                        
  def removeNode ( self, node ):
    if DEBUG_MODE :print ':: NodeNetwork: removing node %s (%d)' % ( node.name, node.id )
    # remove from NodeNetwork
    if node.id in self.nodes.keys() :
      if DEBUG_MODE :print '...found in keys'
      nodePopped = self.nodes.pop( node.id )        
  #
  #
  def removeLink ( self, link ):
    if DEBUG_MODE :print ':: NodeNetwork: removing link (%d)' % link.id
    # remove from model links
    if link.id in self.links.keys() :
      if DEBUG_MODE :print '...found in keys'
      linkPopped = self.links.pop( link.id )
      
      # detach node from links
      linkPopped.srcNode.detachOutputParamFromLink( linkPopped.srcParam, linkPopped )
      linkPopped.dstNode.detachInputParamFromLink( linkPopped.dstParam )
      
      # check if we can remove a child from destination node
      dstNode = linkPopped.dstNode
      srcNode = linkPopped.srcNode
      
      sourceNodeReferenceCount = 0
      for inputLink in dstNode.inputLinks.values():
        if inputLink.srcNode == srcNode:
          sourceNodeReferenceCount += 1
      if sourceNodeReferenceCount == 0:
        if srcNode in dstNode.childs :
          dstNode.childs.remove( srcNode )                
  #
  #      
  def clear ( self ):
    if DEBUG_MODE :print ':: NodeNetwork: clearing nodes ...'
    # remove links
    for link in self.links.values():
      self.removeLink ( link )
    
    # remove nodes    
    for node in self.nodes.values():
      self.removeNode ( node )
        
    self.nodes = {}
    self.links = {}

    self.node_id = 0       
    self.link_id = 0
  #
  #      
  def getNodeFromName ( self, nodeName ):
    for node in self.nodes.values():
      if node.name == nodeName:
        return node
    return None
  #
  #
  #  
  def parseToXML ( self, dom ) :
    #
    root = dom.createElement( "nodenet" )
    root.setAttribute ( "name", self.name )
    root.setAttribute ( "author", "meShaderEd" )
    
    # append network help (short description)      
    
    help_tag = dom.createElement ( "help" )
    help_text = dom.createTextNode ( self.help ) 
    help_tag.appendChild ( help_text ) 
    root.appendChild ( help_tag )
    
    nodes_tag = dom.createElement ( "nodes" )
    
    #print ':: parsing nodes to XML ...' 
    for id in self.nodes.keys() :
      node = self.nodes [ id ]
      #if DEBUG_MODE :print '=> parsing node to XML: %s ...' % node.label
      xml_node = node.parseToXML ( dom )
      nodes_tag.appendChild ( xml_node )
    
    root.appendChild ( nodes_tag )
    
    links_tag = dom.createElement ( "links" )
    
    #print ':: parsing links to XML ...'
    for id in self.links.keys() :
      link = self.links [ id ]
      #print '=> parsing link to XML: ...' 
      #link.printInfo ()
      xml_link = link.parseToXML ( dom )
      links_tag.appendChild ( xml_link )
    
    root.appendChild ( links_tag )
      
    dom.appendChild ( root )
    #print ':: %s NodeNet have parsed to XML ...' % self.name
  #
  #
  #  
  def parseFromXML ( self, root ) :
    #
    self.name = str ( root.attributes().namedItem('name').nodeValue() )
    self.author = str ( root.attributes().namedItem('author').nodeValue() ) 
                              
    xml_nodeList = root.elementsByTagName ( 'node' )
    for i in range( 0, xml_nodeList.length() ) :
      xml_node = xml_nodeList.item( i )
      node = self.addNodeFromXML ( xml_node )

    xml_linkList = root.elementsByTagName ( 'link' )
    for i in range( 0, xml_linkList.length() ) :
      xml_link = xml_linkList.item( i )
      link = NodeLink ( self, xml_link )
      #link.printInfo () 
      self.addLink ( link )
  #
  #
  #  
  def addNodeFromXML ( self, xml_node ) :
    #
    node = createNodeFromXML ( xml_node ) 
    self.addNode ( node )
    return node          
  #
  # save NodeNetwork to .xml document      
  #
  def save ( self ):
    #
    result = False
      
    dom = QtXml.QDomDocument ( self.name ) 
    self.parseToXML ( dom )
    
    file = QFile ( self.fileName ) 
    if file.open ( QtCore.QIODevice.WriteOnly ) :
      if file.write ( dom.toByteArray () ) != -1 :
        result = True      
    file.close()
    return result
  #
  # open NodeNetwork from .xml document      
  #
  def open ( self, fileName ):
    #
    nodes = []
    links = []
      
    dom = QtXml.QDomDocument ( self.name ) 
    
    file = QFile ( fileName ) 
    if file.open ( QtCore.QIODevice.ReadOnly ) :
      if dom.setContent ( file )  : 
        self.fileName = fileName
        
        root = dom.documentElement() 
        if root.nodeName() == 'node' :
          #print ':: parsing node from XML ...'
          nodes.append ( self.addNodeFromXML ( root ) )
        elif root.nodeName() == 'nodenet' :
          #print ':: parsing nodenet from XML ...'
          self.parseFromXML ( root ) 
          nodes = self.getNodesList ()
          links = self.getLinksList () 
        else :
          print ':: unknown XML document format'  
    file.close()
    #
    # correct currnet NodeNetwork node_id and link_id 
    # according to max id values from opened network
    #
    max_node_id = 0
    for node in nodes :
      max_node_id = max ( max_node_id, node.id )
      
    max_link_id = 0
    for link in links :
      max_link_id = max ( max_link_id, link.id )  
    
    self.node_id =  max_node_id
    self.link_id =  max_link_id
    
    #print ':: NodeNetwork node_id = %d link_id = %d' % ( self.node_id, self.link_id )
          
    return ( nodes, links )   
  #
  # insert NodeNetwork from .xml document      
  #
  def insert ( self, fileName ):
    #
    nodes = []
    links = [] 
    
    dom = QtXml.QDomDocument ( self.name ) 
    
    file = QFile ( fileName ) 
    if file.open ( QtCore.QIODevice.ReadOnly ) :
      if dom.setContent ( file )  : 
        #self.fileName = fileName
        root = dom.documentElement() 
        if root.nodeName() == 'node' :
          #print ':: parsing node from XML ...'
          nodes.append ( self.addNodeFromXML ( root ) )
        elif root.nodeName() == 'nodenet' :
          #print ':: parsing nodenet from XML ...'
          nodeNet = NodeNetwork ( 'tmp', root )
          nodeNet.fileName = fileName
           
          nodes = nodeNet.getNodesList ()
          links = nodeNet.getLinksList () 
          
          for node in nodes : self.addNode ( node )        
          for link in links : self.addLink ( link )
        else :
          print ':: unknown XML document format'  
    file.close()
    
    max_node_id = 0
    for node in nodes :
      max_node_id = max ( max_node_id, node.id )
      
    max_link_id = 0
    for link in links :
      max_link_id = max ( max_link_id, link.id )  
    
    self.node_id =  max_node_id
    self.link_id =  max_link_id
    
    #print ':: NodeNetwork node_id = %d link_id = %d' % ( self.node_id, self.link_id )
    
    return ( nodes, links )
    
#
#
#  
def createNodeFromXML ( xml_node ) :
  #
  createNodeTable = { 'rib':RIBNode 
                     ,'rib_code':RIBCodeNode 
                     ,'image':ImageNode 
                     ,'surface':RSLNode 
                     ,'displacement':RSLNode
                     ,'light':RSLNode 
                     ,'volume':RSLNode 
                    }  
  
  node_type = str ( xml_node.attributes().namedItem( 'type' ).nodeValue() )
  createNode = RSLNode # Node
  if node_type in createNodeTable.keys() :
    createNode = createNodeTable[ node_type ] 
  
  #print '-> creating node type = %s (%s)' % ( node_type, str( createNode ) ) 
  node = createNode ( xml_node )

  return node            
