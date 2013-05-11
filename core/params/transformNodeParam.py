#===============================================================================
# transformNodeParam.py
#===============================================================================
import os, sys

from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars

#
# Transform parameter that used in RIB
#
class TransformNodeParam ( NodeParam ) :
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = True ) :
    #
    NodeParam.__init__ ( self, xml_param, isRibParam )
    self.type = 'transform'
  #
  #
  def encodedTypeStr ( self ) : return 'T'
  #
  #
  def copy ( self ) :
    #
    newParam = TransformNodeParam ()
    self.copySetup ( newParam )
    return newParam
  #
  #
  def valueFromStr ( self, strValue ) :
    #
    value = [ 0.0, 0.0, 0.0 ]
    if strValue != '' :
      #str = str.replace( ' ', '' )
      transform_values = strValue.split ( ' ' )
      f = map ( float, transform_values )
      value = [ f[0], f[1], f[2] ]
    return value
  #
  #
  def valueToStr ( self, value ):
    return ''.join ( '%.3f' % f + ' ' for f in value[: - 1] ) + '%.3f' % value [ - 1]