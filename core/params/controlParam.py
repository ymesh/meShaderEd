"""

	controlParam.py

"""
import re
import copy

from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# ControlParam
#
class ControlParam ( NodeParam ) :
	#
	# __init__
	#
	def __init__ ( self, xml_param = None, isRibParam = False ) :
		#
		self.btext = '' # button text
		self.type = 'control'
		self.code = ''
		NodeParam.__init__ ( self, xml_param, isRibParam )

		if DEBUG_MODE : print ( '>> ControlParam ( %s ).__init__ btext = "%s"' % ( self.label, self.btext ) )
	#
	# encodedTypeStr
	#
	def encodedTypeStr ( self ) : return 'l'
	#
	# copy
	#
	def copy ( self ) :
		#
		newParam = ControlParam ()
		self.copySetup ( newParam )
		return newParam
	#
	# copySetup
	#
	def copySetup ( self, newParam ) :
		#
		if DEBUG_MODE : print ( '>> ControlParam ( %s ).copySetup' % self.label )
		NodeParam.copySetup ( self, newParam )
		newParam.code = self.code
		newParam.btext = self.btext
	#
	# valueFromStr
	#
	def valueFromStr ( self, str ) : return str
	#
	# valueToStr
	#
	def valueToStr ( self, value ) :
		#
		ret_str = str ( value )
		if not self.isRibParam : ret_str = str ( "\"" + value + "\"" )
		return ret_str
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
	#
	# parseFromXML
	#
	def parseFromXML ( self, xml_param ) :
		#
		if DEBUG_MODE : print ( '>> ControlParam ( %s ).parseFromXML' % self.label )
		NodeParam.parseFromXML ( self, xml_param )

		control_code_tag = xml_param.namedItem ( 'code' )
		if not control_code_tag.isNull () :
			self.code = str ( control_code_tag.toElement ().text () )
		else :
			# for temp. backward compatibility check 'control_code' also
			control_code_tag = xml_param.namedItem ( 'control_code' )
			if not control_code_tag.isNull () :
				code_str = str ( control_code_tag.toElement ().text () ).lstrip ()
				if code_str == '' : code_str = None
				self.code = code_str
			
		self.btext = str ( xml_param.attributes ().namedItem ( 'btext' ).nodeValue () )
	#
	# parseToXML
	#
	def parseToXML ( self, dom ) :
		#
		if DEBUG_MODE : print ( '>> ControlParam ( %s ).parseToXML' % self.label )
		xmlnode = NodeParam.parseToXML ( self, dom )

		if self.code is not None :
			code_tag = dom.createElement ( 'code' )
			code_text = dom.createTextNode ( self.code )
			code_tag.appendChild ( code_text )
			xmlnode.appendChild ( code_tag )
		
		if self.btext != '' : xmlnode.setAttribute ( 'btext', self.btext )

		return xmlnode
	#
	# execControlCode
	#
	def execControlCode ( self, node ) :
		#
		print ( '>> ControlParam ( %s ).execControlCode' % self.label )
		if self.code is not None :
			exec (  self.code, { 'node' : node, 'self' : self } )
