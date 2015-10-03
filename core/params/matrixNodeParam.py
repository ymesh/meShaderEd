"""

	matrixNodeParam.py

"""
import re

from core.node import Node
from core.nodeParam import NodeParam

from global_vars import app_global_vars, DEBUG_MODE
#
# Matrix
#
class MatrixNodeParam ( NodeParam ) :
	#
	# __init__
	#
	def __init__ ( self, xml_param = None, isRibParam = False ) :
		NodeParam.__init__ ( self, xml_param, isRibParam )
		self.type = 'matrix'
	#
	# encodedTypeStr
	#
	def encodedTypeStr ( self ) : return 'm'
	#
	# copy
	#
	def copy ( self ) :
		#
		newParam = MatrixNodeParam ()
		self.copySetup ( newParam )
		return newParam
	#
	# valueFromStr
	#
	def valueFromStr ( self, strValue ) :
		#
		value = [ [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0] ]

		if strValue != '' and strValue != '0' :
			if strValue == '1' :
				value = [ [1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0] ] # default
			else:
				strValue = str.replace ( ' ', '' )

				matrix16_pattern_str = 'matrix\(([-+]?([0-9]*\.)?[0-9]+,){15}[-+]?([0-9]*\.)?[0-9]+\)'
				matrix1_pattern_str  = 'matrix\(([-+]?([0-9]*\.)?[0-9]+\))'
				matrix16_space_pattern_str = 'matrix"[a-z]*"\(([-+]?([0-9]*\.)?[0-9]+,){15}[-+]?([0-9]*\.)?[0-9]+\)'
				matrix1_space_pattern_str  = 'matrix"[a-z]*"\(([-+]?([0-9]*\.)?[0-9]+\))'
				float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
				space_pattern_str = '"[a-z]*"'

				p = re.compile ( matrix16_pattern_str )
				match = p.match ( strValue)
				if match :
					p = re.compile ( float_pattern_str )
					f = p.findall ( strValue )
					f = map ( float, f )
					value = [ f[0:4], f[4:8], f[8:12], f[12:16] ]
				else :
					p = re.compile ( matrix1_pattern_str )
					match = p.match ( strValue )
					if match :
						p = re.compile ( float_pattern_str )
						f = p.findall ( strValue )
						f = map ( float, f )
						value = [ [f[0], 0.0, 0.0, 0.0], [0.0, f[0], 0.0, 0.0], [0.0, 0.0, f[0], 0.0], [0.0, 0.0, 0.0, f[0]] ]
					else :
						p = re.compile ( matrix16_space_pattern_str )
						match = p.match ( strValue )
						if match :
							p = re.compile ( float_pattern_str )
							f = p.findall ( strValue )
							f = map ( float, f )
							value = [ f[0:4], f[4:8], f[8:12], f[12:16] ]

							p = re.compile ( space_pattern_str )
							s = p.findall ( strValue )
							self.space = s[0].strip ( '"' )
						else :
							p = re.compile ( matrix1_space_pattern_str )
							match = p.match ( strValue )
							if match :
								p = re.compile ( float_pattern_str )
								f = p.findall ( strValue )
								f = map ( float, f )
								value = [ [f[0], 0.0, 0.0, 0.0], [0.0, f[0], 0.0, 0.0], [0.0, 0.0, f[0], 0.0], [0.0, 0.0, 0.0, f[0]] ]

								p = re.compile ( space_pattern_str )
								s = p.findall ( strValue )
								self.space = s[0].strip ( '"' )
							else :
								err = 'Cannot parse matrix %s values' % self.name
								raise Exception ( err )
		return value
	#
	# valueToStr
	#
	def valueToStr ( self, value ) :
		#
		flatMat = sum ( value, [] )
		ret_str = 'matrix'
		if self.space != None :
			if self.space != '' :
				ret_str += ' "' + self.space + '" '
		return ret_str +'(' + ''.join ('%.3f' % f + ',' for f in flatMat[: - 1]) + '%.3f' % flatMat[ - 1] + ')'
	#
	# setValue
	#
	def setValue ( self, value ) :
		#
		if self.value != value :
			self.value = value
			self.paramChanged ()
