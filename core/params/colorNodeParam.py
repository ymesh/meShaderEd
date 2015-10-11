"""

	colorNodeParam.py

"""
import re
import copy
from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# ColorNodeParam
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
		color3_pattern_str = 'color\(([+]?([0-9]*\.)?[0-9]+,){2}[+]?([0-9]*\.)?[0-9]+\)'
		color1_pattern_str = 'color\(([+]?([0-9]*\.)?[0-9]+\))'
		color3_space_pattern_str = 'color"[A-z]*"\(([+]?([0-9]*\.)?[0-9]+,){2}[+]?([0-9]*\.)?[0-9]+\)'
		color1_space_pattern_str = 'color"[A-z]*"\(([+]?([0-9]*\.)?[0-9]+\))'
		float_pattern_str = '[+]?[0-9]*\.?[0-9]+'
		space_pattern_str = '"[A-z]*"'
			
		if not self.isArray () :
			value = [ 0.0, 0.0, 0.0 ]
			if strValue != '' :
				strValue = strValue.replace ( ' ', '' )
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
		else :
			arrayValue = []
			spaceValue = []
			strValue = strValue.strip ( '[]' )
			if strValue != '' :
				strValue = strValue.replace ( ' ', '' )
				strArrayValue = []
				args = strValue.split ( 'color' )
				for a in args :
					if a != '' :
						strArrayValue.append ( 'color' + a.rstrip (',') )
				for strValue in strArrayValue :		
					value = [ 0.0, 0.0, 0.0 ]
					space = None
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
								space = s [0].strip ( '"' )
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
									space = s [0].strip ( '"' )
								else :
									err = 'Cannot parse color %s values' % self.name
									raise Exception ( err )
					arrayValue.append ( value )
					spaceValue.append ( space )
			self.spaceArray = copy.deepcopy ( spaceValue ) 
			value = arrayValue								
		return value
	#
	# valueFromRIB
	#
	def valueFromRIB ( self, strValue ) :
		#
		value = [ 0.0, 0.0, 0.0 ]
		if strValue != '' :
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
		if not self.isArray () :
			strValue = 'color'
			if self.space != None and self.space != '' :
				strValue += ' "' + self.space + '" '
			strValue += '(' + ''.join ( '%.3f' % f + ',' for f in value [: - 1] ) + '%.3f' % value [ - 1] + ')'
		else :
			arrayStrValue = '{'
			for i in range ( self.arraySize ) :
				strValue = 'color'
				space = self.spaceArray [ i ]
				if space != None and space != '' :
					strValue += ' "' + space + '" '
				strValue += '(' + ''.join ( '%.3f' % f + ',' for f in value [ i ][: - 1] ) + '%.3f' % value [ i ][ - 1] + ')'
				if i != ( self.arraySize - 1 ) :
					strValue += ','
				arrayStrValue += strValue
			arrayStrValue += '}'
			strValue = arrayStrValue
		return strValue
	#
	# getValueToRIB
	#
	def getValueToRIB ( self, value ) :
		#
		if not self.isArray () :
			strValue = ''.join ( '%.3f' % f + ' ' for f in value [: - 1] ) + '%.3f' % value [ - 1]
		else :
			arrayStrValue = '['
			for i in range ( self.arraySize ) :
				strValue = ''.join ( '%.3f' % f + ' ' for f in value [ i ][: - 1] ) + '%.3f' % value [ i ][ - 1]
				if i != ( self.arraySize - 1 ) :
					strValue += ','
				arrayStrValue += strValue
			arrayStrValue += ']'
			strValue = arrayStrValue
		return strValue
