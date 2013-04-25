#===============================================================================
# controlParam.py
#===============================================================================
import os, sys
import re
import copy
from PyQt4 import QtCore

from node import Node
from nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# ControlParam
#
class ControlParam ( NodeParam ) :
  #
  # __init__
  #
  def __init__ ( self, xml_param = None, isRibParam = False ) :
    #
    NodeParam.__init__ ( self, xml_param, isRibParam )

    if xml_param is None :
      self.type = 'control'
      self.control_code = ''

    if DEBUG_MODE : print '>> ControlParam ( %s ).__init__' % self.label
  #
  # encodedTypeStr
  #
  def encodedTypeStr ( self ) : return 'l'
  #
  # copy
  #
  def copy ( self ) :
    #
    newParam = ControlParam ()
    self.copySetup ( newParam )
    return newParam
  #
  # copySetup
  #
  def copySetup ( self, newParam ) :
    #
    if DEBUG_MODE : print '>> ControlParam ( %s ).copySetup' % self.label
    NodeParam.copySetup ( self, newParam )
    newParam.control_code = self.control_code
  #
  # valueFromStr
  #
  def valueFromStr ( self, str ) : return str
  #
  # valueToStr
  #
  def valueToStr ( self, value ) :
    #
    ret_str = str ( value )
    if not self.isRibParam : ret_str = str ( "\"" + value + "\"" )
    return ret_str
  #
  # getRangeValues
  #
  # if subtype == selector then return list of (label,value) pairs
  # It's supposed, that range is defined as "value1:value2:value3"
  # or "label1=value1:label2=value2:label3=value3:"
  #
  def getRangeValues ( self ) :
    #
    rangeList = []

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
        rangeList.append ( ( parseGlobalVars ( label ), parseGlobalVars ( value ) ) )
    return rangeList
  #
  # parseFromXML
  #
  def parseFromXML ( self, xml_param ) :
    #
    if DEBUG_MODE : print '>> ControlParam ( %s ).parseFromXML' % self.label
    NodeParam.parseFromXML ( self, xml_param )

    control_code_tag = xml_param.namedItem ( 'control_code' )
    if not control_code_tag.isNull () :
      self.control_code = str ( control_code_tag.toElement ().text () )
  #
  # execParamCode
  #
  def execControlCode ( self, node ) :
    #
    if self.control_code != None :
      control_code = self.control_code.lstrip ()
      if control_code != '' :
        exec ( control_code, { 'node' : node, 'self' : self } )
