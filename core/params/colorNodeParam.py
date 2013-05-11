#===============================================================================
# colorNodeParam.py
#===============================================================================
import os, sys
import re

from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# Color
#
class ColorNodeParam ( NodeParam ) :
  #
  # __init__
  #
  def __init__ ( self, xml_param = None, isRibParam = False  ) :
    #
    NodeParam.__init__ ( self, xml_param, isRibParam )
    self.type = 'color'
  #
  # encodedTypeStr
  #
  def encodedTypeStr ( self ) : return 'c'
  #
  # copy
  #
  def copy ( self ) :
    #
    newParam = ColorNodeParam ()
    self.copySetup ( newParam )
    return newParam
  #
  # valueFromStr
  #
  def valueFromStr ( self, strValue ) :
    #
    if self.isRibParam :
      return self.valueFromRIB ( strValue )
    else :
      return self.valueFromRSL ( strValue )
  #
  # valueFromRSL
  #
  def valueFromRSL ( self, strValue ) :
    #
    value = [ 0.0, 0.0, 0.0 ]

    if strValue != '' :
      strValue = strValue.replace ( ' ', '' )
      color3_pattern_str = 'color\(([+]?([0-9]*\.)?[0-9]+,){2}[+]?([0-9]*\.)?[0-9]+\)'
      color1_pattern_str = 'color\(([+]?([0-9]*\.)?[0-9]+\))'
      color3_space_pattern_str = 'color"[A-z]*"\(([+]?([0-9]*\.)?[0-9]+,){2}[+]?([0-9]*\.)?[0-9]+\)'
      color1_space_pattern_str = 'color"[A-z]*"\(([+]?([0-9]*\.)?[0-9]+\))'
      float_pattern_str = '[+]?[0-9]*\.?[0-9]+'
      space_pattern_str = '"[A-z]*"'

      p = re.compile ( color3_pattern_str )
      match = p.match ( strValue )
      if match :
        p = re.compile ( float_pattern_str )
        f = p.findall ( strValue )
        f = map ( float, f )
        value = [ f [0], f [1], f [2] ]
      else :
        p = re.compile ( color1_pattern_str )
        match = p.match( strValue )
        if match :
          p = re.compile ( float_pattern_str )
          f = p.findall( strValue )
          f = map ( float, f )
          value = [ f [0], f [0], f [0] ]
        else :
          p = re.compile ( color3_space_pattern_str )
          match = p.match( strValue )
          if match :
            p = re.compile ( float_pattern_str )
            f = p.findall ( strValue )
            f = map ( float, f )
            value = [ f [0], f [1], f [2] ]

            p = re.compile ( space_pattern_str )
            s = p.findall ( strValue )
            self.space = s [0].strip ( '"' )
          else :
            p = re.compile ( color1_space_pattern_str )
            match = p.match( strValue )
            if match :
              p = re.compile ( float_pattern_str )
              f = p.findall ( strValue )
              f = map ( float, f )
              value = [ f [0], f [0], f [0] ]

              p = re.compile ( space_pattern_str )
              s = p.findall ( strValue )
              self.space = s [0].strip ( '"' )
            else :
              err = 'Cannot parse color %s values' % self.name
              raise Exception ( err )
    return value
  #
  # valueFromRIB
  #
  def valueFromRIB ( self, strValue ) :
    #
    value = [ 0.0, 0.0, 0.0 ]

    if strValue != '' :
      #str = str.replace( ' ', '' )
      color_values = strValue.split ( ' ' )
      f = map ( float, color_values )
      value = [ f [0], f [1], f [2] ]
    return value
  #
  # valueToStr
  #
  def valueToStr ( self, value ) :
    #
    if self.isRibParam :
      return self.getValueToRIB ( value )
    else :
      return self.getValueToRSL ( value )
  #
  # getValueToRSL
  #
  def getValueToRSL ( self, value ) :
    #
    ret_str = 'color'
    if self.space != None :
      if self.space != '' :
        ret_str += ' "' + self.space + '" '
    return ret_str + '(' + ''.join ( '%.3f' % f + ',' for f in value [: - 1] ) + '%.3f' % value [ - 1] + ')'
  #
  # getValueToRIB
  #
  def getValueToRIB ( self, value ) :
    #
    return ''.join ( '%.3f' % f + ' ' for f in value [: - 1] ) + '%.3f' % value [ - 1]
