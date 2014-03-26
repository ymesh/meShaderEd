"""

 nodeParam.py

"""
import os, sys
import re
import copy
from PyQt4 import QtCore

from core.node import Node
from global_vars import app_global_vars, DEBUG_MODE, VALID_RIB_NODE_TYPES
from core.meCommon import parseGlobalVars
#
# Abstract Node Parameter Class
#
class NodeParam ( QtCore.QObject ) :
  #
  isInput = True
  isRibParam = False
  id = 0
  #
  # __init__
  #
  def __init__ ( self, xml_param = None, isRibParam = False ) :
    #
    super ( NodeParam, self ).__init__ ()

    self.id = None
    self.name = None
    self.label = None
    self.type = None
    self.help = None  # short description

    self.default = None
    self.value = None
    self.shaderParam = False

    self.isRibParam = isRibParam
    self.display = True
    self.enabled = True
    self.removable = False

    # extra parameter description
    self.detail = '' # variable, uniform
    self.provider = '' # primitive, connection, constant, variable, expression

    # ui decorative parameters
    self.subtype = ''
    self.range = ''

    self.space = None # actual for color, point, vector, normal, matrix
    self.spaceDef = None # default value space

    self.arraySize = None # otherwise, it should be a list of values ( or empty list )

    self.defaultArray = []
    self.valueArray = []
    #self.spaceArray = []
    #self.spaceDefArray = []

    if xml_param != None : self.parseFromXML ( xml_param )
  #
  # isArray
  #
  def isArray ( self ) : return ( self.array is not None )
  #
  # setup
  #
  def setup ( self, name, label = '', detail = None, provider = None ) :
    #
    self.name = name
    if label == '' or label is None : self.label = name
    else: self.label = label

    self.detail = detail
    self.provider = provider
  #
  # copy
  #
  def copy ( self ) : assert 0, 'copy needs to be implemented!'
  #
  # copySetup
  #
  def copySetup ( self, newParam ) :
    #
    #if DEBUG_MODE : print '>> NodeParam( %s ).copySetup' % self.label
    newParam.id = self.id
    newParam.name = self.name
    newParam.label = self.label
    newParam.type = self.type
    newParam.help = self.help
    newParam.isInput = self.isInput
    newParam.shaderParam = self.shaderParam
    newParam.isRibParam = self.isRibParam
    newParam.display = self.display
    newParam.enabled = self.enabled
    newParam.removable = self.removable
    newParam.detail = self.detail
    newParam.provider = self.provider
    newParam.subtype = self.subtype
    newParam.range = self.range
    newParam.space = self.space
    newParam.spaceDef = self.spaceDef

    newParam.default = copy.deepcopy ( self.default )
    newParam.value = copy.deepcopy ( self.value )
  #
  # typeToStr
  #
  def typeToStr ( self ) :
    #
    str = self.detail + ' ' + self.type
    return str.lstrip ()
  #
  # encodedTypeStr
  #
  def encodedTypeStr ( self ) : assert 0, 'encodedStr needs to be implemented!'
  #
  # setValueFromStr
  #
  def setValueFromStr ( self, strValue ) : self.value = self.valueFromStr ( strValue )
  #
  # setDefaultFromStr
  #
  def setDefaultFromStr ( self, strValue ) : self.default = self.valueFromStr ( strValue )

  #
  # Virtual functions
  #

  #
  # valueFromStr
  #
  def valueFromStr ( self, strValue ) : return strValue
  #
  # getValueToStr
  #
  def getValueToStr ( self ) :
    #
    if self.value != None :
      return self.valueToStr ( self.value )
    else :
      return None
  #
  # getDefaultToStr
  #
  def getDefaultToStr ( self ) :
    #
    if self.default != None :
      return self.valueToStr ( self.default )
    else :
      return None
  #
  # virtual function
  #
  def valueToStr ( self, value ) : return str ( value )
  #
  # paramChanged
  #
  def paramChanged ( self ) :
    #
    if DEBUG_MODE : print '>> NodeParam.paramChanged (name = %s)' % self.name
    self.emit ( QtCore.SIGNAL ( 'paramChanged(QObject)' ), self )
  #
  # setupUI
  #
  def setupUI ( self, subtype, range ) :
    #
    self.subtype = subtype
    self.range = range
  #
  # setValue
  #
  def setValue ( self, value ) :
    #
    if self.value != value :
      self.value = value
      self.paramChanged ()
  #
  # removeItemFromRange
  #
  def removeItemFromRange ( self, item_label ) :
    #
    newRangeList = []
    if self.range != '' : # and self.subtype == 'selector':
      tmp_list = str ( self.range ).split ( ':' )
      for s in tmp_list :
        pair = s.split ( '=' )
        if len ( pair ) > 1 :
          label = pair [0]
          value = pair [1]
        else :
          label = s
          value = s
        #
        if label != item_label :
          newRangeList.append ( s )
      self.range = ( ':' ).join ( newRangeList )  
  #
  # renameItemInRange
  #
  def renameItemInRange ( self, item_label, newLabel ) :
    #
    newRangeList = []
    if self.range != '' : # and self.subtype == 'selector':
      tmp_list = str ( self.range ).split ( ':' )
      for s in tmp_list :
        pair = s.split ( '=' )
        if len ( pair ) > 1 :
          label = pair [0]
          value = pair [1]
        else :
          label = s
          value = s
        #
        if label == item_label :
          s = s.replace ( label, newLabel, 1 ) # replace only label
        newRangeList.append ( s )
      self.range = ( ':' ).join ( newRangeList )    
  #
  # parseFromXML
  #
  def parseFromXML ( self, xml_param ) :
    #
    self.name        = str ( xml_param.attributes ().namedItem ( 'name' ).nodeValue () )
    self.label       = str ( xml_param.attributes ().namedItem ( 'label' ).nodeValue () )
    if self.label == '' : self.label = self.name
    self.type        = str ( xml_param.attributes ().namedItem ( 'type' ).nodeValue () )
    self.shaderParam = xml_param.attributes ().namedItem ( 'shaderParam' ).nodeValue () == '1'

    self.detail      = str ( xml_param.attributes ().namedItem ( 'detail' ).nodeValue () )
    self.provider    = str ( xml_param.attributes ().namedItem ( 'provider' ).nodeValue () )
    self.subtype     = str ( xml_param.attributes ().namedItem ( 'subtype' ).nodeValue () )
    self.range       = str ( xml_param.attributes ().namedItem ( 'range' ).nodeValue () )

    self.display = True
    if not xml_param.attributes ().namedItem ( 'display' ).isNull () :
      self.display = xml_param.attributes ().namedItem ( 'display' ).nodeValue () == '1'

    self.enabled = True
    if not xml_param.attributes ().namedItem ( 'enabled' ).isNull () :
      self.enabled = xml_param.attributes ().namedItem ( 'enabled' ).nodeValue () == '1'
      
    self.removable = False
    if not xml_param.attributes ().namedItem ( 'removable' ).isNull () :
      self.removable = xml_param.attributes ().namedItem ( 'removable' ).nodeValue () == '1'

    if not xml_param.attributes ().namedItem ( 'space' ).isNull () :
      space = str ( xml_param.attributes ().namedItem ( 'space' ).nodeValue () )
      if space != '' :
        self.space = space
        self.spaceDef = space

    if not xml_param.attributes ().namedItem ( 'spaceDef' ).isNull () :
      spaceDef = str ( xml_param.attributes ().namedItem ( 'spaceDef' ).nodeValue () )
      if spaceDef != '' :
        self.spaceDef = space

    self.setDefaultFromStr ( xml_param.attributes ().namedItem ( 'default' ).nodeValue () )

    if not xml_param.attributes ().namedItem ( 'value' ).isNull () :
      self.setValueFromStr ( xml_param.attributes ().namedItem ( 'value' ).nodeValue () )
    else :
      self.value = self.default

    #print ':: value = %s default = %s' % ( self.getValueToStr(), self.getDefaultToStr()  )

    help_tag = xml_param.namedItem ( 'help' )

    if not help_tag.isNull () :
      self.help = str ( help_tag.toElement ().text () )
  #
  # parseToXML
  #
  def parseToXML ( self, dom ) :
    #
    xmlnode = dom.createElement( 'property' )

    if self.name != None   : xmlnode.setAttribute ( 'name', self.name )
    if self.label != None  : xmlnode.setAttribute ( 'label', self.label )
    if self.type != None   : xmlnode.setAttribute ( 'type', self.type )
    if self.shaderParam    : xmlnode.setAttribute ( 'shaderParam', True )
    if not self.display    : xmlnode.setAttribute ( 'display', False )
    if not self.enabled    : xmlnode.setAttribute ( 'enabled', False )
    if self.removable      : xmlnode.setAttribute ( 'removable', True )
    if self.detail != ''   : xmlnode.setAttribute ( 'detail', self.detail )
    if self.provider != '' : xmlnode.setAttribute ( 'provider', self.provider )
    # ui decorative parameters
    if self.subtype != ''  : xmlnode.setAttribute ( 'subtype', self.subtype )
    if self.range != ''    : xmlnode.setAttribute ( 'range', self.range )

    if self.space != None  :
      if self.space != ''  : xmlnode.setAttribute ( 'space', self.space )

    # write default value space only if it differs from value space
    if self.spaceDef != None  :
      if self.spaceDef != '' and  self.spaceDef != self.space : xmlnode.setAttribute ( 'spaceDef', self.spaceDef )

    if self.default != None :
      value = self.getDefaultToStr ()
      if not self.type in VALID_RIB_NODE_TYPES : value = value.strip ( '\"' )
      xmlnode.setAttribute ( 'default', value )

    if self.value != None :
      value = self.getValueToStr ()
      if not self.type in VALID_RIB_NODE_TYPES : value = value.strip ( '\"' )
      xmlnode.setAttribute ( 'value', value )

    if self.help != None :
      # append node help (short description)
      help_tag = dom.createElement ( 'help' )
      help_text = dom.createTextNode ( self.help )
      help_tag.appendChild ( help_text )
      xmlnode.appendChild ( help_tag )

    return xmlnode
