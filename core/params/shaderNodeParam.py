"""

    shaderNodeParam.py

"""
from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# ShaderNodeParam
#
class ShaderNodeParam ( NodeParam ) :
    #
    # __init__
    #
    def __init__ ( self, xml_param = None, isRibParam = False ) :
        #
        NodeParam.__init__ ( self, xml_param, isRibParam )
        self.type = 'shader'
    #
    # encodedTypeStr
    #
    def encodedTypeStr ( self ) : return 'S'
    #
    # copy
    #
    def copy ( self ) :
        #
        newParam = ShaderNodeParam ()
        self.copySetup ( newParam )
        return newParam
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
