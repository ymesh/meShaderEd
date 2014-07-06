"""

	normalNodeParam.py

"""
import re

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# NormalNodeParam
#
class NormalNodeParam ( NodeParam ) :
	#
	# __init__
	#
	def __init__ ( self, xml_param = None, isRibParam = False ) :
		#
		NodeParam.__init__ ( self, xml_param, isRibParam )
		self.type = 'normal'
	#
	# encodedTypeStr
	#
	def encodedTypeStr ( self ) : return 'n'
	#
	# copy
	#
	def copy ( self ) :
		#
		newParam = NormalNodeParam ()
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
			normal3_pattern_str = 'normal\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
			normal1_pattern_str = 'normal\(([-+]?([0-9]*\.)?[0-9]+\))'
			normal3_space_pattern_str = 'normal"[a-z]*"\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
			normal1_space_pattern_str = 'normal"[a-z]*"\(([-+]?([0-9]*\.)?[0-9]+\))'
			float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
			space_pattern_str = '"[a-z]*"'

			p = re.compile ( normal3_pattern_str )
			match = p.match ( strValue )
			if match :
				# normal(0,0,0)
				p = re.compile ( float_pattern_str )
				f = p.findall ( strValue )
				f = map ( float, f )
				value = [ f [0], f [1], f [2] ]
			else :
				# normal(0)
				p = re.compile ( normal1_pattern_str )
				match = p.match ( strValue )
				if match :
					p = re.compile ( float_pattern_str )
					f = p.findall ( strValue )
					f = map ( float, f )
					value = [ f [0], f [0], f [0] ]
				else :
					# normal "space" (0,0,0)
					p = re.compile ( normal3_space_pattern_str )
					match = p.match ( strValue )
					if match :
						p = re.compile ( float_pattern_str )
						f = p.findall ( strValue )
						f = map ( float, f )
						value = [ f [0], f [1], f [2] ]

						p = re.compile ( space_pattern_str )
						s = p.findall ( strValue )
						self.space = s [0].strip ( '"' )
					else :
						# normal "space" (0)
						p = re.compile ( normal1_space_pattern_str )
						match = p.match ( strValue )
						if match :
							p = re.compile ( float_pattern_str )
							f = p.findall ( strValue )
							f = map ( float, f )
							value = [ f [0], f [0], f [0] ]

							p = re.compile ( space_pattern_str )
							s = p.findall ( strValue )
							self.space = s [0].strip ( '"' )
						else :
							err = 'Cannot parse normal %s values' % self.name
							raise Exception ( err )
		return value
	#
	# valueToStr
	#
	def valueToStr ( self, value ) :
		#
		ret_str = 'normal'

		if self.space != None :
			if self.space != '' :
				ret_str += ' "' + self.space + '" '
		return ret_str + '(' + ''.join ( '%.3f' % f + ',' for f in value [: - 1] ) + '%.3f' % value [ - 1] + ')'
