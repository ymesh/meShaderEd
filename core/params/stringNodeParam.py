"""

	stringNodeParam.py

"""
import re

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# StringNodeParam
#
class StringNodeParam ( NodeParam ) :
	#
	# __init__
	#
	def __init__ ( self, xml_param = None, isRibParam = False ) :
		#
		NodeParam.__init__ ( self, xml_param, isRibParam )
		self.type = 'string'
	#
	# encodedTypeStr
	#
	def encodedTypeStr ( self ) : return 's'
	#
	# copy
	#
	def copy ( self ) :
		#
		newParam = StringNodeParam ()
		self.copySetup ( newParam )
		return newParam
	#
	# valueFromStr
	#
	def valueFromStr ( self, strValue ) : 
		#
		if not self.isArray () :
			value = parseGlobalVars ( strValue )
		else :
			value = []
			strValue = strValue.strip ( '[]' )
			s = strValue.split ( ',' )
			for i in range ( len ( s ) ) :
				value.append ( parseGlobalVars( s[ i ].strip ( "\" " ) ) )
		return value
	#
	# valueToStr
	#
	def valueToStr ( self, value ) :
		#
		if not self.isArray () :
			strValue = parseGlobalVars ( value )
			if not self.isRibParam : 
				strValue = str ( "\"" + value + "\"" )
		else :
			strValue = '{' + ''.join ( '"%s"' % f + ',' for f in value [: - 1] ) + '"%s"' % value [ - 1] + '}'
		return strValue
	#
	# getValueToRSL
	#
	def getValueToRSL ( self, value ) : return self.valueToStr ( value )
	#
	# getValueToRIB
	#
	def getValueToRIB ( self, value ) : return self.valueToStr ( value )
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
