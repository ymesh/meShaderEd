"""

	vectorNodeParam.py

"""
import re

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
		value = [ 0.0, 0.0, 0.0 ]

		if strValue != '' :
			strValue = strValue.replace ( ' ', '' )
			vector3_pattern_str = 'vector\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
			vector1_pattern_str = 'vector\(([-+]?([0-9]*\.)?[0-9]+\))'
			vector3_space_pattern_str = 'vector"[a-z]*"\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
			vector1_space_pattern_str = 'vector"[a-z]*"\(([-+]?([0-9]*\.)?[0-9]+\))'
			float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
			space_pattern_str = '"[a-z]*"'

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
		return value
	#
	# valueToStr
	#
	def valueToStr ( self, value ) :
		#
		ret_str = 'vector'

		if self.space != None :
			if self.space != '' :
				ret_str += ' "' + self.space + '" '
		return ret_str +'(' + ''.join ( '%.3f' % f + ',' for f in value[: - 1] ) + '%.3f' % value [ - 1] + ')'
