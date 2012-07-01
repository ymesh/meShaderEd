#===============================================================================
# nodeParam.py
#
# 
#
#===============================================================================
import os, sys
import re
from PyQt4 import QtCore

from node import Node
#
# Abstract Parameter Class
#
class NodeParam ( QtCore.QObject ):
  isInput = True
  isRibParam = False
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    #
    QtCore.QObject.__init__ ( self )
    
    self.name = None
    self.label = None
    self.type = None
    self.help = None  # short description
    
    self.default = None
    self.value = None
    self.shaderParam = False
    
    self.isRibParam = isRibParam

    # extra parameter description
    self.detail = '' # variable, uniform
    self.provider = '' # primitive, connection, constant, variable, expression
    
    # ui decorative parameters
    self.subtype = ''
    self.range = ''
    
    if xml_param != None :
      self.parseFromXML ( xml_param )
    
  #
  #
  def setup ( self, name, label, detail, provider ):
    self.name = name
    if label == '' : self.label = name
    else: self.label = label
      
    self.detail = detail
    self.provider = provider
  #
  #
  def typeToStr ( self ):
    str = self.detail + ' ' + self.type
    return str.lstrip()
  #
  #
  def encodedTypeStr ( self ): assert 0, 'encodedStr needs to be implemented!'
  #
  #
  def setValueFromStr ( self, strValue ): self.value = self.valueFromStr( strValue )
  def setDefaultFromStr ( self, strValue ): self.default = self.valueFromStr( strValue )
  #
  # virtual function
  # 
  def valueFromStr ( self, strValue ) : return strValue
  #
  #
  def getValueToStr ( self ): 
    if self.value != None :
      return self.valueToStr ( self.value )
    else :
      return None
      
  def getDefaultToStr ( self ): 
    if self.default != None :
      return self.valueToStr ( self.default )
    else :
      return None
  #
  # virtual function
  #  
  def valueToStr ( self, value ) : return str( value )
  #
  #
  def copy ( self ): assert 0, 'copy needs to be implemented!'
  #        
  #
  def paramChanged ( self ): self.emit( QtCore.SIGNAL( 'paramChanged(QObject)' ), self ) 
  #
  # 
  def setupUI ( self, subtype, range ):
    #if subtype != '' :
    #  print ">> NodeParam.setUI: %s subtype = %s range = %s" % ( self.name, subtype, range ) )
    self.subtype = subtype
    self.range = range
  #
  #
  #
  def setValue ( self, value ) :
    print '>> NodeParam.setValue'
    self.value = value
    self.paramChanged () 
  #
  #
  #
  def parseFromXML ( self, xml_param ) :
    #
    self.name = str ( xml_param.attributes().namedItem( 'name' ).nodeValue() )
    self.label = str ( xml_param.attributes().namedItem( 'label' ).nodeValue() )
    self.type = str ( xml_param.attributes().namedItem( 'type' ).nodeValue() )
    self.shaderParam = xml_param.attributes().namedItem( 'shaderParam' ).nodeValue() == '1'
    
    if self.label == '' : self.label = self.name
    #print '--> parsing param name= %s label= %s type= %s' % ( self.name, self.label, self.type ) 
    #if self.shaderParam :
    #  print '--> is shaderParam'
      
    self.detail = str ( xml_param.attributes().namedItem( 'detail' ).nodeValue() )
    self.provider = str ( xml_param.attributes().namedItem( 'provider' ).nodeValue() )
    
    self.subtype = str ( xml_param.attributes().namedItem( 'subtype' ).nodeValue() )
    self.range = str ( xml_param.attributes().namedItem( 'range' ).nodeValue() )
    
    self.setDefaultFromStr ( str ( xml_param.attributes().namedItem( 'default' ).nodeValue() ) )
    
    if not xml_param.attributes().namedItem( 'value' ).isNull() :
      self.setValueFromStr ( str ( xml_param.attributes().namedItem( 'value' ).nodeValue() ) )
    else :
      self.value = self.default
      
    print ':: value = %s default = %s' % ( self.getValueToStr(), self.getDefaultToStr()  )
    
    help_tag = xml_param.namedItem ( 'help' )
    
    if not help_tag.isNull() :
      help = help_tag.toElement().text()
      self.help = help
      #print '--> help= %s' % self.help
  #
  #
  #  
  def parseToXML ( self, dom ) :
    #
    xmlnode = dom.createElement( "property" )

    if self.name != None :xmlnode.setAttribute ( "name", self.name )
    if self.label != None : xmlnode.setAttribute ( "label", self.label )
    if self.type != None : xmlnode.setAttribute ( "type", self.type )
    if self.shaderParam : xmlnode.setAttribute ( "shaderParam", True )
      
    if self.detail != '' : xmlnode.setAttribute ( "detail", self.detail )
    if self.provider != '' : xmlnode.setAttribute ( "provider", self.provider )
    
    # ui decorative parameters
    if self.subtype != '' : xmlnode.setAttribute ( "subtype", self.subtype )
    if self.range != '' : xmlnode.setAttribute ( "range", self.range )
      
    if self.default != None : xmlnode.setAttribute ( "default", self.getDefaultToStr().strip('\"')  )
    if self.value != None : xmlnode.setAttribute ( "value", self.getValueToStr().strip('\"')  )
    
    if self.help != None :
      # append node help (short description)      
      help_tag = dom.createElement ( "help" )
      help_text = dom.createTextNode ( self.help ) 
      help_tag.appendChild ( help_text ) 
      xmlnode.appendChild ( help_tag )
    
    return xmlnode
#
# Float
#      
class FloatNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam ) 
    self.type = 'float' 
    #print "FloatNodeParam.__init__"
  #
  #
  def encodedTypeStr( self ): return 'f'    
  #
  #
  def valueFromStr ( self, str ):
    value = 0.0
    #print "FloatNodeParam.setValueFromStr %s" % str
    if str != '': 
      try: value = float( str )
      except: raise Exception( 'Cannot parse float value for parameter %s' % (self.name) ) 
    return value
  #
  #
  def valueToStr ( self, value ) : return '%.3f' % float( value )
  #
  # if subtype == selector then return list of (label,value) pairs
  # It's supposed, that range is defined as "value1:value2:value3" 
  # or "label1=value1:label2=value2:label3=value3:"
  #
  # if subtype == slider then return list [min, max, step] from 
  # space separated string range="min max step"
  # 
  #
  def getRangeValues ( self ):
    #
    rangeList = []
    i = 0 
    if self.range != '' :
      #
      # get range for selector
      #
      if self.subtype == 'selector':
        tmp_list = str( self.range ).split( ':' )
        for s in tmp_list :
          pair = s.split( '=' )
          if len( pair ) > 1 :
            label = pair[0]
            value = float( pair[1] )
          else :
            label = s
            value = float( i ) 
          i += 1  
          rangeList.append( (label, value) )
      #
      # get range for slider
      #    
      elif self.subtype == 'slider' or self.subtype == 'slider': 
        tmp_list = str( self.range ).split() 
        for i in range( 0, 3 ) :
          value = 0.0
          if i < len( tmp_list ) :
            value = float( tmp_list[ i ] )
          rangeList.append( value ) 
          #print '-> range[%d] = %f' % ( i, value )
      
    return rangeList
#
# Integer
#      
class IntNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False  ):
    NodeParam.__init__ ( self, xml_param, isRibParam ) 
    self.type = 'int' 
    #print "FloatNodeParam.__init__"
  #
  #
  def encodedTypeStr( self ): return 'i'    
  #
  #
  def valueFromStr ( self, str ):
    value = 0
    #print "FloatNodeParam.setValueFromStr %s" % str
    if str != '' : 
      try: value = int( str )
      except: raise Exception( 'Cannot parse integer value for parameter %s' % (self.name) ) 
    return value
  #
  #
  def valueToStr ( self, value ) : return '%d'% value

  #
  # if subtype == selector then return list of (label,value) pairs
  # It's supposed, that range is defined as "value1:value2:value3" 
  # or "label1=value1:label2=value2:label3=value3:"
  #
  def getRangeValues ( self ):
    #
    rangeList = []
    i = 0 
    if self.range != '' :
      #
      # get range for selector
      #
      if self.subtype == 'selector':
        tmp_list = str( self.range ).split( ':' )
        for s in tmp_list :
          pair = s.split( '=' )
          if len( pair ) > 1 :
            label = pair[0]
            value = int( pair[1] )
          else :
            label = s
            value = int( i ) 
          i += 1  
          rangeList.append( (label, value) )
      #
      # get range for slider
      #    
      elif self.subtype == 'slider' or self.subtype == 'slider': 
        tmp_list = str( self.range ).split() 
        for i in range( 0, 3 ) :
          value = 0
          if i < len( tmp_list ) :
            value = int( tmp_list[ i ] )
          rangeList.append( value ) 
          #print '-> range[%d] = %f' % ( i, value )  
    return rangeList    
#
# Color
#      
class ColorNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False  ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'color' 
    #print "ColorNodeParam.__init__"
  #
  #
  def encodedTypeStr( self ): return 'c'           
  #
  #
  def valueFromStr ( self, strValue ) :
    if self.isRibParam :
      return self.valueFromRIB ( strValue )
    else :
      return self.valueFromRSL ( strValue )   
  #
  #  
  def valueFromRSL ( self, strValue ) :
    value = [ 0.0, 0.0, 0.0 ]
    #print "ColorNodeParam.setValueFromStr %s" % str
    if strValue != '' : 
      strValue = strValue.replace( ' ', '' )
      color3_pattern_str = 'color\(([+]?([0-9]*\.)?[0-9]+,){2}[+]?([0-9]*\.)?[0-9]+\)'
      color1_pattern_str = 'color\(([+]?([0-9]*\.)?[0-9]+\))'
      float_pattern_str = '[+]?[0-9]*\.?[0-9]+'
      p = re.compile( color3_pattern_str )             
      match = p.match( strValue )
      if match :
        p = re.compile( float_pattern_str )
        f = p.findall( strValue ) 
        f = map( float, f )               
        value = [ f[0], f[1], f[2] ]
      else :
        p = re.compile( color1_pattern_str )             
        match = p.match( strValue )
        if match :
          p = re.compile( float_pattern_str )
          f = p.findall( strValue ) 
          f = map( float, f )               
          value = [ f[0], f[0], f[0] ]  
        else :
          raise Exception ( 'Cannot parse color property %s values' % self.name )  
    return value
  #
  #  
  def valueFromRIB ( self, strValue ) :
    value = [ 0.0, 0.0, 0.0 ]
    #print "ColorNodeParam.setValueFromStr %s" % str
    if strValue != '' : 
      #str = str.replace( ' ', '' )
      color_values = strValue.split( ' ')
      f = map( float, color_values )
      value = [ f[0], f[1], f[2] ]
    return value
  #
  #
  def valueToStr ( self, value ):
    if self.isRibParam :
      return self.getValueToRIB ( value )
    else :
      return self.getValueToRSL ( value )      
  #
  #
  def getValueToRSL ( self, value ):
    return 'color(' + ''.join('%.3f' % f + ',' for f in value[: - 1]) + '%.3f' % value[ - 1] + ')'
  #
  #
  def getValueToRIB ( self, value ):
    return ''.join('%.3f' % f + ' ' for f in value[: - 1]) + '%.3f' % value[ - 1]
#
# String
#      
class StringNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam ) 
    self.type = 'string' 
    #print "FloatNodeParam.__init__"
  #
  #
  def encodedTypeStr ( self ): return 's'    
  #
  #
  def valueFromStr ( self, str ): return str
    #print "StringNodeParam.setValueFromStr %s" % str
  #
  #
  def valueToStr ( self, value ): 
    if self.isRibParam :
      return str( value )
    else :
      return str( "\"" + value + "\"" )
  #
  # if subtype == selector then return list of (label,value) pairs
  # It's supposed, that range is defined as "value1:value2:value3" 
  # or "label1=value1:label2=value2:label3=value3:"
  #
  def getRangeValues ( self ):
    
    rangeList = []
     
    if self.range != '' : # and self.subtype == 'selector':
      tmp_list = str( self.range ).split( ':' )
      for s in tmp_list :
        pair = s.split( '=' )
        if len( pair ) > 1 :
          label = pair[0]
          value = pair[1]
        else :
          label = s
          value = s 
        rangeList.append( (label, value) )
      
    return rangeList
#
# Normal
# 
class NormalNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'normal' 
    #print "NormalNodeParam.__init__"
  #
  #
  def encodedTypeStr ( self ): return 'n'           
  #
  #
  def valueFromStr ( self, str ):
    value = [ 0.0, 0.0, 0.0 ]
    #print "NormalNodeParam.setValueFromStr %s" % str
    if str != '' : 
      str = str.replace( ' ', '' )
      normal3_pattern_str = 'normal\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
      normal1_pattern_str = 'normal\(([-+]?([0-9]*\.)?[0-9]+\))'
      float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
      p = re.compile( normal3_pattern_str )             
      match = p.match( str )
      if match :
        p = re.compile( float_pattern_str )
        f = p.findall( str ) 
        f = map( float, f )               
        value = [ f[0], f[1], f[2] ]
      else :
        p = re.compile( normal1_pattern_str )             
        match = p.match( str )
        if match :
          p = re.compile( float_pattern_str )
          f = p.findall( str ) 
          f = map( float, f )               
          value = [ f[0], f[0], f[0] ]  
        else :
          raise Exception ( 'Cannot parse normal property %s values' % self.name )  
    return value      
  #
  #
  def valueToStr ( self, value ):
    return 'normal(' + ''.join('%.3f' % f + ',' for f in value[: - 1]) + '%.3f' % value[ - 1] + ')'    
#
# Point
# 
class PointNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'point' 
    #print "PointNodeParam.__init__"
  #
  #
  def encodedTypeStr ( self ): return 'p'           
  #
  #
  def valueFromStr ( self, str ):
    value = [ 0.0, 0.0, 0.0 ]
    #print "PointNodeParam.setValueFromStr %s" % str
    if str != '' : 
      str = str.replace( ' ', '' )
      point3_pattern_str = 'point\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
      point1_pattern_str = 'point\(([-+]?([0-9]*\.)?[0-9]+\))'
      float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
      p = re.compile( point3_pattern_str )             
      match = p.match( str )
      if match :
        p = re.compile( float_pattern_str )
        f = p.findall( str ) 
        f = map( float, f )               
        value = [ f[0], f[1], f[2] ]
      else :
        p = re.compile( point1_pattern_str )             
        match = p.match( str )
        if match :
          p = re.compile( float_pattern_str )
          f = p.findall( str ) 
          f = map( float, f )               
          value = [ f[0], f[0], f[0] ]  
        else :
          raise Exception ( 'Cannot parse point property %s values' % self.name )  
    return value
  #
  #
  def valueToStr ( self, value ):
    return 'point(' + ''.join('%.3f' % f + ',' for f in value[: - 1]) + '%.3f' % value[ - 1] + ')'     
#
# Vector
# 
class VectorNodeParam( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'vector' 
    #print "VectorNodeParam.__init__"
  #
  #
  def encodedTypeStr ( self ): return 'v'           
  #
  #
  def valueFromStr ( self, str ):
    value = [ 0.0, 0.0, 0.0 ]
    #print "VectorNodeParam.setValueFromStr %s" % str
    if str != '' : 
      str = str.replace( ' ', '' )
      vector3_pattern_str = 'vector\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
      vector1_pattern_str = 'vector\(([-+]?([0-9]*\.)?[0-9]+\))'
      float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
      p = re.compile( vector3_pattern_str )             
      match = p.match( str )
      if match :
        p = re.compile( float_pattern_str )
        f = p.findall( str ) 
        f = map( float, f )               
        value = [ f[0], f[1], f[2] ]
      else :
        p = re.compile( vector1_pattern_str )             
        match = p.match( str )
        if match :
          p = re.compile( float_pattern_str )
          f = p.findall( str ) 
          f = map( float, f )               
          value = [ f[0], f[0], f[0] ]  
        else :
          raise Exception ( 'Cannot parse vector property %s values' % self.name )
    return value        
  #
  #
  def valueToStr ( self, value ):
    return 'vector(' + ''.join('%.3f' % f + ',' for f in value[: - 1]) + '%.3f' % value[ - 1] + ')'     
#
# Matrix
# 
class MatrixNodeParam( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'matrix' 
    #print "MatrixNodeParam.__init__"
  #
  #
  def encodedTypeStr ( self ): return 'm'           
  #
  #
  def valueFromStr ( self, str ):
    value = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]   
    #print "MatrixNodeParam.setValueFromStr %s" % str
    if str != '' and str != '0':
      if str == '1' :  
        value = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]] # default
      else:
        str = str.replace( ' ', '' )
        matrix16_pattern_str = 'matrix\(([-+]?([0-9]*\.)?[0-9]+,){15}[-+]?([0-9]*\.)?[0-9]+\)'
        matrix1_pattern_str = 'matrix\(([-+]?([0-9]*\.)?[0-9]+\))'
        float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
        p = re.compile( matrix16_pattern_str )             
        match = p.match( str )
        if match :
          p = re.compile( float_pattern_str )
          f = p.findall( str ) 
          f = map( float, f )               
          value = [ f[0:4], f[4:8], f[8:12], f[12:16] ]
        else :
          p = re.compile( matrix1_pattern_str )             
          match = p.match( str )
          if match :
            p = re.compile( float_pattern_str )
            f = p.findall( str ) 
            f = map( float, f )               
            value = [[f[0], 0.0, 0.0, 0.0], [0.0, f[0], 0.0, 0.0], [0.0, 0.0, f[0], 0.0], [0.0, 0.0, 0.0, f[0]]] 
          else :
            raise Exception ( 'Cannot parse matrix property %s values' % self.name )
    return value        
  #
  #
  def valueToStr ( self, value ):
    flatMat = sum( value, [] )
    return 'matrix(' + ''.join('%.3f' % f + ',' for f in flatMat[: - 1]) + '%.3f' % flatMat[ - 1] + ')'    
#
# Surface
# 
class SurfaceNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'surface' 
  #
  #
  def encodedTypeStr ( self ): return 'S' 
  #def valueToStr ( self, value ): return str( "\"" + value + "\"" )          
  
#
# Displacement
# 
class DisplacementNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'displacement' 
  #
  #
  def encodedTypeStr ( self ): return 'D'           
  #def valueToStr ( self, value ): return str( "\"" + value + "\"" )
#
# Light
# 
class LightNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'light' 
  #
  #
  def encodedTypeStr ( self ): return 'L'           
  #def valueToStr ( self, value ): return str( "\"" + value + "\"" )
#
# Volume
# 
class VolumeNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'volume' 
  #
  #
  def encodedTypeStr ( self ): return 'V'           
  #def valueToStr ( self, value ): return str( "\"" + value + "\"" )
#
# RIB
# 
class RibNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'rib' 
    
  #
  #
  def encodedTypeStr ( self ): return 'R'           
 
#
# Text
# 
class TextNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'text' 
  #
  #
  def encodedTypeStr ( self ): return 'X'           
#
# Transform parameter that used in RIB
# 
class TransformNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = True ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'transform' 
  #
  #
  def encodedTypeStr ( self ): return 'T' 
  #
  #
  def valueFromStr ( self, strValue ):
    value = [ 0.0, 0.0, 0.0 ]
    if strValue != '' : 
      #str = str.replace( ' ', '' )
      transform_values = strValue.split( ' ' )
      f = map( float, transform_values )
      value = [ f[0], f[1], f[2] ]
    return value 
  #
  #
  def valueToStr ( self, value ):
    return ''.join('%.3f' % f + ' ' for f in value[: - 1]) + '%.3f' % value[ - 1] 
           
#
# Image
# 
class ImageNodeParam ( NodeParam ):    
  #
  #
  def __init__ ( self, xml_param = None, isRibParam = False ):
    NodeParam.__init__ ( self, xml_param, isRibParam )  
    self.type = 'image' 
  #
  #
  def encodedTypeStr ( self ): return 'I'  
  #
  # if subtype == selector then return list of (label,value) pairs
  # It's supposed, that range is defined as "value1:value2:value3" 
  # or "label1=value1:label2=value2:label3=value3:"
  #
  def getRangeValues ( self ):
    
    rangeList = []
     
    if self.range != '' : # and self.subtype == 'texture':
      tmp_list = str( self.range ).split( ':' )
      for s in tmp_list :
        pair = s.split( '=' )
        if len( pair ) > 1 :
          label = pair[0]
          value = pair[1]
        else :
          label = s
          value = s 
        rangeList.append( (label, value) )
      
    return rangeList         
