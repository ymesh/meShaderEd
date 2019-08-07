"""

    textNodeParam.py

"""
from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# TextNodeParam
#
class TextNodeParam ( NodeParam ) :
    #
    # __init__
    #
    def __init__ ( self, xml_param = None, isRibParam = False ) :
        #
        NodeParam.__init__ ( self, xml_param, isRibParam )
        self.type = 'text'
    #
    # encodedTypeStr
    #
    def encodedTypeStr ( self ) : return 'X'
    #
    # copy
    #
    def copy ( self ) :
        #
        newParam = TextNodeParam ()
        self.copySetup ( newParam )
        return newParam
    #
    # valueToStr
    #
    # Skip here conversation to str because text
    # can contain unicode characters
    #
    def valueToStr ( self, value ) :
        return unicode ( value )
