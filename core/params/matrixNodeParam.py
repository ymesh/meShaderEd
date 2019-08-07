"""

    matrixNodeParam.py

"""
import re
import copy
from core.node import Node
from core.nodeParam import NodeParam
from global_vars import app_global_vars, DEBUG_MODE
#
# MatrixNodeParam
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
        strValue = str ( strValue )
        matrix16_pattern_str = 'matrix\(([-+]?([0-9]*\.)?[0-9]+,){15}[-+]?([0-9]*\.)?[0-9]+\)'
        matrix1_pattern_str  = 'matrix\(([-+]?([0-9]*\.)?[0-9]+\))'
        matrix16_space_pattern_str = 'matrix"[A-z]*"\(([-+]?([0-9]*\.)?[0-9]+,){15}[-+]?([0-9]*\.)?[0-9]+\)'
        matrix1_space_pattern_str  = 'matrix"[A-z]*"\(([-+]?([0-9]*\.)?[0-9]+\))'
        float_pattern_str = '[-+]?[0-9]*\.?[0-9]+'
        space_pattern_str = '"[A-z]*"'
        
        if not self.isArray () :
            value = [ [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0] ]
            if strValue != '' and strValue != '0' :
                if strValue == '1' :
                    value = [ [1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0] ] # default
                else:
                    print ( '>>> matrixNodeParam.valueFromStr %s' % strValue )
                    strValue = strValue.replace ( ' ', '' )
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
        else :
            arrayValue = []
            spaceValue = []
            strValue = strValue.strip ( '[]' )
            if strValue != '' :
                strValue = strValue.replace ( ' ', '' )
                strArrayValue = []
                args = strValue.split ( 'matrix' )
                for a in args :
                    if a != '' :
                        strArrayValue.append ( 'matrix' + a.rstrip (',') )
                for strValue in strArrayValue :			
                    value = [ [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0] ]
                    space = None
                    if strValue != '0' :
                        if strValue == '1' :
                            value = [ [1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0] ] # default
                        else:
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
                                        space = s[0].strip ( '"' )
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
                                            space = s[0].strip ( '"' )
                                        else :
                                            err = 'Cannot parse matrix %s values' % self.name
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
            flatMat = sum ( value, [] ) # flatten matrix to list
            strValue = 'matrix'
            if self.space != None and self.space != '' : 
                strValue += ' "' + self.space + '" '
            strValue += '(' + ''.join ('%.3f' % f + ',' for f in flatMat[: - 1]) + '%.3f' % flatMat[ - 1] + ')'
        else :
            arrayStrValue = '{'
            for i in range ( self.arraySize ) :
                strValue = 'matrix'
                space = self.spaceArray [ i ]
                if space != None and space != '' :
                    strValue += ' "' + space + '" '
                flatMat = sum ( value [ i ], [] ) # flatten matrix to list
                strValue += '(' + ''.join ( '%.3f' % f + ',' for f in flatMat [: - 1] ) + '%.3f' % flatMat [ - 1] + ')'
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
            flatMat = sum ( value, [] ) # flatten matrix to list
            strValue = ''.join ('%.3f' % f + ' ' for f in flatMat[: - 1]) + '%.3f' % flatMat[ - 1]
        else :
            arrayStrValue = '['
            for i in range ( self.arraySize ) :
                flatMat = sum ( value [ i ], [] ) # flatten matrix to list
                strValue = '(' + ''.join ( '%.3f' % f + ',' for f in flatMat [: - 1] ) + '%.3f' % flatMat [ - 1] + ')'
                if i != ( self.arraySize - 1 ) :
                    strValue += ','
                arrayStrValue += strValue
            arrayStrValue += ']'
            strValue = arrayStrValue
        return strValue
    #
    # setValue
    #
    def setValue ( self, value ) :
        #
        if self.value != value :
            self.value = value
            self.paramChanged ()
