"""

    normalNodeParam.py

"""
import re
import copy
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
    # 
    def valueFromStr ( self, strValue ) :
        #
        strValue = str ( strValue )
        normal3_pattern_str = 'normal\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
        normal1_pattern_str = 'normal\(([-+]?([0-9]*\.)?[0-9]+\))'
        normal3_space_pattern_str = 'normal"[A-z]*"\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)'
        normal1_space_pattern_str = 'normal"[A-z]*"\(([-+]?([0-9]*\.)?[0-9]+\))'
        float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
        space_pattern_str = '"[A-z]*"'
        if not self.isArray () :
            value = [ 0.0, 0.0, 0.0 ]
            if strValue != '' :
                strValue = strValue.replace ( ' ', '' )
                
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
        else :
            arrayValue = []
            spaceValue = []
            strValue = strValue.strip ( '[]' )
            if strValue != '' :
                strValue = strValue.replace ( ' ', '' )
                #print strValue
                strArrayValue = []
                args = strValue.split ( 'normal' )
                for a in args :
                    if a != '' :
                        strArrayValue.append ( 'normal' + a.rstrip (',') )
                #print strArrayValue	 
                for strValue in strArrayValue :
                    value = [ 0.0, 0.0, 0.0 ]
                    space = None
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
                                space = s [0].strip ( '"' )
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
                                    space = s [0].strip ( '"' )
                                else :
                                    err = 'Cannot parse normal %s values' % self.name
                                    raise Exception ( err )
                    arrayValue.append ( value )
                    spaceValue.append ( space )
            self.spaceArray = copy.deepcopy ( spaceValue ) 
            value = arrayValue
        return value
    #
    # valueToStr
    #
    def valueToStr ( self, value ) :
        #
        if not self.isArray () :
            strValue = 'normal'
            if self.space != None and self.space != '' :
                strValue += ' "' + self.space + '" '
            strValue += '(' + ''.join ( '%.3f' % f + ',' for f in value [: - 1] ) + '%.3f' % value [ - 1] + ')'
        else :
            arrayStrValue = '{'
            for i in range ( self.arraySize ) :
                strValue = 'normal'
                space = self.spaceArray [ i ]
                if space != None and space != '' :
                    strValue += ' "' + space + '" '
                strValue += '(' + ''.join ( '%.3f' % f + ',' for f in value [ i ][: - 1] ) + '%.3f' % value [ i ][ - 1] + ')'
                if i != ( self.arraySize - 1 ) :
                    strValue += ','
                arrayStrValue += strValue
            arrayStrValue += '}'
            strValue = arrayStrValue
        return strValue
    #
    # getValueToRIB
    #
    def getValueToRIB ( self, value ) :
        #
        if not self.isArray () :
            strValue = ''.join ( '%.3f' % f + ' ' for f in value [: - 1] ) + '%.3f' % value [ - 1]
        else :
            arrayStrValue = '['
            for i in range ( self.arraySize ) :
                strValue = ''.join ( '%.3f' % f + ' ' for f in value [ i ][: - 1] ) + '%.3f' % value [ i ][ - 1]
                if i != ( self.arraySize - 1 ) :
                    strValue += ','
                arrayStrValue += strValue
            arrayStrValue += ']'
            strValue = arrayStrValue
        return  strValue
            