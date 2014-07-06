"""

	pointNodeParam.py

"""
import re

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# PointNodeParam
#
class PointNodeParam ( NodeParam ) :
	#
	# __init__
	#
	def __init__ ( self, xml_param = None, isRibParam = False ) :
		#
		NodeParam.__init__ ( self, xml_param, isRibParam )
		self.type = 'point'
	#
	# encodedTypeStr
	#
	def encodedTypeStr ( self ) : return 'p'
	#
	# copy
	#
	def copy ( self ) :
		#
		newParam = PointNodeParam ()
		self.copySetup ( newParam )
		return newParam
	#
	# valueFromStr
	#
	def valueFromStr ( self, strValue ) :
		#
		value = [ 0.0, 0.0, 0.0 ]

		if strValue != '' :
			strValue = strValue.replace ( ' ', '' )
			
			point3_pattern_str = 'point\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
			point1_pattern_str = 'point\(([-+]?([0-9]*\.)?[0-9]+\))'
			point3_space_pattern_str = 'point"[a-z]*"\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
			point1_space_pattern_str = 'point"[a-z]*"\(([-+]?([0-9]*\.)?[0-9]+\))'
			float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
			space_pattern_str = '"[a-z]*"'
			
			p = re.compile ( point3_pattern_str )
			match = p.match ( strValue )
			if match :
				# point(0,0,0)
				p = re.compile ( float_pattern_str )
				f = p.findall ( strValue )
				f = map ( float, f )
				value = [ f [0], f [1], f [2] ]
			else :
				# point(0)
				p = re.compile ( point1_pattern_str )
				match = p.match ( strValue )
				if match :
					p = re.compile ( float_pattern_str )
					f = p.findall ( strValue )
					f = map ( float, f )
					value = [ f [0], f [0], f [0] ]
				else :
					# point "space" (0,0,0)
					p = re.compile ( point3_space_pattern_str )
					match = p.match ( strValue )
					if match :
						p = re.compile ( float_pattern_str )
						f = p.findall ( strValue )
						f = map ( float, f )
						value = [ f [0], f [1], f [2] ]

						p = re.compile ( space_pattern_str )
						s = p.findall ( strValue )
						sp = str ( s[0] )
						self.space = sp.strip ( '"' )
					else :
						# point "space" (0)
						p = re.compile ( point1_space_pattern_str )
						match = p.match ( strValue )
						if match :
							p = re.compile ( float_pattern_str )
							f = p.findall ( strValue )
							f = map ( float, f )
							value = [ f [0], f [0], f [0] ]

							p = re.compile ( space_pattern_str )
							s = p.findall ( strValue )
							sp = str ( s[0] )
							self.space = sp.strip ( '"' )
						else :
							err = 'Cannot parse point %s values' % self.name
							raise Exception ( err )
		return value
	#
	# valueToStr
	#
	def valueToStr ( self, value ) :
		#
		ret_str = 'point'
		
		if self.space != None :
			if self.space != '' :
				ret_str += ' "' + self.space + '" '
		return ret_str + '(' + ''.join ( '%.3f' % f + ',' for f in value [: - 1] ) + '%.3f' % value [ - 1] + ')'
