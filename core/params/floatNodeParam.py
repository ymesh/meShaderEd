"""

    floatNodeParam.py

"""
import re

from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import parseGlobalVars
#
# FloatNodeParam
#
class FloatNodeParam ( NodeParam ) :
    #
    # __init__
    #
    def __init__ ( self, xml_param = None, isRibParam = False ) :
        #
        NodeParam.__init__ ( self, xml_param, isRibParam )
        #super ( FloatNodeParam, self ).__init__ ( xml_param, isRibParam )
        self.type = 'float'
    #
    # encodedTypeStr
    #
    def encodedTypeStr ( self ) : return 'f'
    #
    # copy
    #
    def copy ( self ) :
        #
        newParam = FloatNodeParam ()
        self.copySetup ( newParam )
        return newParam
    #
    # valueFromStr
    #
    def valueFromStr ( self, strValue ) :
        #
        if not self.isArray () :
            value = 0.0
            if strValue != '' :
                try: value = float ( strValue )
                except: raise Exception ( 'Cannot parse float value for parameter %s' % ( self.name ) )
        else :
            value = []
            s = re.findall ( r'[+-]?[\d\.]+', strValue )
            f = map ( float, s )
            value = f
        return value
    #
    # valueToStr
    #
    def valueToStr ( self, value ) : 
        #
        if not self.isArray () :
            strValue = '%.3f' % float ( value )
        else :
            strValue = '{' + ''.join ( '%.3f' % f + ',' for f in value [: - 1] ) + '%.3f' % value [ - 1] + '}'
        return strValue
    #
    # getValueToRIB
    #
    def getValueToRIB ( self, value ) :
        #
        if not self.isArray () :
            strValue = '%.3f' % float ( value )
        else :
            strValue = '[' + ''.join ( '%.3f' % f + ' ' for f in value [: - 1] ) + '%.3f' % value [ - 1] + ']'
        return strValue
    #
    # getRangeValues
    #
    def getRangeValues ( self ) :
        # if subtype == selector then return list of (label,value) pairs
        # It's supposed, that range is defined as "value1:value2:value3"
        # or "label1=value1:label2=value2:label3=value3:"
        #
        # if subtype == slider then return list [min, max, step] from
        # space separated string range="min max step"
        #
        rangeList = []
        i = 0
        if self.range != '' :
            #
            # get range for selector
            #
            if self.subtype == 'selector' :
                tmp_list = str ( self.range ).split ( ':' )
                for s in tmp_list :
                    pair = s.split ( '=' )
                    if len ( pair ) > 1 :
                        label = pair [0]
                        value = float ( pair [1] )
                    else :
                        label = s
                        value = float ( i )
                    i += 1
                    rangeList.append ( ( parseGlobalVars ( label ), value ) )
            #
            # get range for slider
            #
            elif self.subtype == 'slider' or self.subtype == 'vslider' :
                tmp_list = str ( self.range ).split ()
                for i in range ( 0, 3 ) :
                    value = 0.0
                    if i < len ( tmp_list ) :
                        value = float ( tmp_list[ i ] )
                    rangeList.append ( value )

        return rangeList
