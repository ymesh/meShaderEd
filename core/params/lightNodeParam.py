"""

    lightNodeParam.py

"""
from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# LightNodeParam
#
class LightNodeParam ( NodeParam ) :
    #
    # __init__
    #
    def __init__ ( self, xml_param = None, isRibParam = False ) :
        #
        NodeParam.__init__ ( self, xml_param, isRibParam )
        self.type = 'light'
    #
    # encodedTypeStr
    #
    def encodedTypeStr ( self ) : return 'L'
    #
    # copy
    #
    def copy ( self ) :
        #
        newParam = LightNodeParam ()
        self.copySetup ( newParam )
        return newParam