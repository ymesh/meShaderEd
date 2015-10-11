"""

	vectorNodeParam.py

"""
import re
import copy
from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# VectorNodeParam
#
class VectorNodeParam ( NodeParam ) :
	#
	# __init__
	#
	def __init__ ( self, xml_param = None, isRibParam = False ) :
		#
		NodeParam.__init__ ( self, xml_param, isRibParam )
		self.type = 'vector'
	#
	# encodedTypeStr
	#
	def encodedTypeStr ( self ) : return 'v'
	#
	# copy
	#
	def copy ( self ) :
		#
		newParam = VectorNodeParam ()
		self.copySetup ( newParam )
		return newParam
	#
	# valueFromStr
	#
	def valueFromStr ( self, strValue ) :
		#
		vector3_pattern_str = 'vector\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
		vector1_pattern_str = 'vector\(([-+]?([0-9]*\.)?[0-9]+\))'
		vector3_space_pattern_str = 'vector"[A-z]*"\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
		vector1_space_pattern_str = 'vector"[A-z]*"\(([-+]?([0-9]*\.)?[0-9]+\))'
		float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
		space_pattern_str = '"[A-z]*"'
		
		if not self.isArray () :
			value = [ 0.0, 0.0, 0.0 ]
			if strValue != '' :
				strValue = strValue.replace ( ' ', '' )
				p = re.compile ( vector3_pattern_str )
				match = p.match ( strValue )
				if match :
					# vector(0,0,0)
					p = re.compile ( float_pattern_str )
					f = p.findall ( strValue )
					f = map ( float, f )
					value = [ f[0], f[1], f[2] ]
				else :
					# vector(0)
					p = re.compile ( vector1_pattern_str )
					match = p.match ( strValue )
					if match :
						p = re.compile ( float_pattern_str )
						f = p.findall ( strValue )
						f = map ( float, f )
						value = [ f[0], f[0], f[0] ]
					else :
						# vector "space" (0,0,0)
						p = re.compile ( vector3_space_pattern_str )
						match = p.match ( strValue )
						if match :
							p = re.compile ( float_pattern_str )
							f = p.findall ( strValue )
							f = map ( float, f )
							value = [ f[0], f[1], f[2] ]
	
							p = re.compile ( space_pattern_str )
							s = p.findall ( strValue )
							sp = str ( s[0] )
							self.space = sp.strip ( '"' )
						else :
							# vector "space" (0)
							p = re.compile ( vector1_space_pattern_str )
							match = p.match ( strValue )
							if match :
								p = re.compile ( float_pattern_str )
								f = p.findall ( strValue )
								f = map ( float, f )
								value = [ f[0], f[0], f[0] ]
	
								p = re.compile ( space_pattern_str )
								s = p.findall ( strValue )
								sp = str ( s[0] )
								self.space = sp.strip ( '"' )
							else :
								err = 'Cannot parse vector %s values' % self.name
								raise Exception ( err )
		else :
			arrayValue = []
			spaceValue = []
			strValue = strValue.strip ( '[]' )
			if strValue != '' :
				strValue = strValue.replace ( ' ', '' )
				#print strValue
				strArrayValue = []
				args = strValue.split ( 'vector' )
				for a in args :
					if a != '' :
						strArrayValue.append ( 'vector' + a.rstrip (',') )
				#print strArrayValue	 
				for strValue in strArrayValue :	
					value = [ 0.0, 0.0, 0.0 ]
					space = None
					p = re.compile ( vector3_pattern_str )
					match = p.match ( strValue )
					if match :
						# vector(0,0,0)
						p = re.compile ( float_pattern_str )
						f = p.findall ( strValue )
						f = map ( float, f )
						value = [ f[0], f[1], f[2] ]
					else :
						# vector(0)
						p = re.compile ( vector1_pattern_str )
						match = p.match ( strValue )
						if match :
							p = re.compile ( float_pattern_str )
							f = p.findall ( strValue )
							f = map ( float, f )
							value = [ f[0], f[0], f[0] ]
						else :
							# vector "space" (0,0,0)
							p = re.compile ( vector3_space_pattern_str )
							match = p.match ( strValue )
							if match :
								p = re.compile ( float_pattern_str )
								f = p.findall ( strValue )
								f = map ( float, f )
								value = [ f[0], f[1], f[2] ]
		
								p = re.compile ( space_pattern_str )
								s = p.findall ( strValue )
								sp = str ( s[0] )
								space = sp.strip ( '"' )
							else :
								# vector "space" (0)
								p = re.compile ( vector1_space_pattern_str )
								match = p.match ( strValue )
								if match :
									p = re.compile ( float_pattern_str )
									f = p.findall ( strValue )
									f = map ( float, f )
									value = [ f[0], f[0], f[0] ]
		
									p = re.compile ( space_pattern_str )
									s = p.findall ( strValue )
									sp = str ( s[0] )
									space = sp.strip ( '"' )
								else :
									err = 'Cannot parse vector %s values' % self.name
									raise Exception ( err )
					arrayValue.append ( value )
					spaceValue.append ( space )
			self.spaceArray = copy.deepcopy ( spaceValue )
			value = arrayValue
		return value
	#
	# valueToStr
	#
	def valueToStr ( self, value ) :
		#
		if not self.isArray () :
			strValue = 'vector'
			if self.space != None and self.space != '' :
					strValue += ' "' + self.space + '" '
			strValue += '(' + ''.join ( '%.3f' % f + ',' for f in value[: - 1] ) + '%.3f' % value [ - 1] + ')'
		else :
			arrayStrValue = '{'
			for i in range ( self.arraySize ) :
				strValue = 'vector'
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
			strValue = ''.join ( '%.3f' % f + ' ' for f in value[: - 1] ) + '%.3f' % value [ - 1]
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