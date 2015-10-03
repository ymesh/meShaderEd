"""

	geomNodeParam.py

"""
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# Geometry
# 
class GeomNodeParam ( NodeParam ) :    
	#
	# __init__
	#
	def __init__ ( self, xml_param = None, isRibParam = False ) :
		#
		NodeParam.__init__ ( self, xml_param, isRibParam )  
		self.type = 'geom' 
	#
	# encodedTypeStr
	#
	def encodedTypeStr ( self ) : return 'G'
	#
	# copy
	#
	def copy ( self ) :
		#
		newParam = GeomNodeParam ()
		self.copySetup ( newParam )
		return newParam