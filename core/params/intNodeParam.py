#===============================================================================
# intNodeParam.py
#===============================================================================
import os, sys

from PyQt4 import QtCore

from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# Integer
#
class IntNodeParam ( NodeParam ) :
  #
  # __init__
  #
  def __init__ ( self, xml_param = None, isRibParam = False  ) :
    #
    NodeParam.__init__ ( self, xml_param, isRibParam )
    self.type = 'int'
  #
  # encodedTypeStr
  #
  def encodedTypeStr ( self ) : return 'i'
  #
  # copy
  #
  def copy ( self ) :
    #
    newParam = IntNodeParam ()
    self.copySetup ( newParam )
    return newParam
  #
  # valueFromStr
  #
  def valueFromStr ( self, str ) :
    #
    value = 0
    
    if str != '' :
      try: value = int ( str )
      except: raise Exception ( 'Cannot parse integer value for parameter %s' % ( self.name ) )
    return value
  #
  # valueToStr
  #
  def valueToStr ( self, value ) : return '%d'% value
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
    i = 0
    if self.range != '' :
      #
      # get range for selector
      #
      if self.subtype == 'selector' :
        tmp_list = str ( self.range ).split ( ':' )
        for s in tmp_list :
          pair = s.split ( '=' )
          if len ( pair ) > 1 :
            label = pair [0]
            value = int ( pair [1] )
          else :
            label = s
            value = int ( i )
          i += 1
          rangeList.append ( (label, value) )
      #
      # get range for slider
      #
      elif self.subtype == 'slider' or self.subtype == 'vslider' :
        tmp_list = str ( self.range ).split ()
        for i in range ( 0, 3 ) :
          value = 0
          if i < len ( tmp_list ) :
            value = int ( tmp_list [ i ] )
          rangeList.append ( value )

    return rangeList
