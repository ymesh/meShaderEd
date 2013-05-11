#===============================================================================
# imageNodeParam.py
#===============================================================================
import os, sys

from PyQt4 import QtCore

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# Image
#
class ImageNodeParam ( NodeParam ) :
  #
  # __init__
  #
  def __init__ ( self, xml_param = None, isRibParam = False ) :
    #
    NodeParam.__init__ ( self, xml_param, isRibParam )
    self.type = 'image'
  #
  # encodedTypeStr
  #
  def encodedTypeStr ( self ) : return 'I'
  #
  # copy
  #
  def copy ( self ) :
    #
    newParam = ImageNodeParam ()
    self.copySetup ( newParam )
    return newParam
  #
  # if subtype == selector then return list of (label,value) pairs
  # It's supposed, that range is defined as "value1:value2:value3"
  # or "label1=value1:label2=value2:label3=value3:"
  #
  def getRangeValues ( self ) :
    #
    rangeList = []

    if self.range != '' : # and self.subtype == 'texture':
      tmp_list = str ( self.range ).split ( ':' )
      for s in tmp_list :
        pair = s.split ( '=' )
        if len( pair ) > 1 :
          label = pair [ 0 ]
          value = pair [ 1 ]
        else :
          label = s
          value = s
        rangeList.append ( (label, value) )

    return rangeList