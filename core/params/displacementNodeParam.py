"""

    displacementNodeParam.py

"""
from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# DisplacementNodeParam
#
class DisplacementNodeParam ( NodeParam ) :
    #
    # __init__
    #
    def __init__ ( self, xml_param = None, isRibParam = False ) :
        #
        NodeParam.__init__ ( self, xml_param, isRibParam )
        self.type = 'displacement'
    #
    # encodedTypeStr
    #
    def encodedTypeStr ( self ) : return 'D'
    #
    # copy
    #
    def copy ( self ):
        #
        newParam = DisplacementNodeParam ()
        self.copySetup ( newParam )
        return newParam
