#===============================================================================
# codeSyntaxHighlighter.py
#
# ver. 1.0.0
# Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
# 
# Dialog for managing node code
# 
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars

import gui.ui_settings as UI
#
#
#
class CodeSyntaxHighlighter( QtGui.QSyntaxHighlighter ):
  #
  def __init__( self, textDocument, mode = 'SL' ):
    QtGui.QSyntaxHighlighter.__init__( self, textDocument )
    
    self.mode = mode
    self.highlightingRules = []
    
    syntax_colors = {}
    
    syntax_colors['types'] = QtCore.Qt.blue
    syntax_colors['literal'] = QtCore.Qt.darkGreen
    syntax_colors['comment'] = QtCore.Qt.darkCyan
    syntax_colors['function'] = QtCore.Qt.darkMagenta
    
    # types
    self.typeFormat = QtGui.QTextCharFormat()
    self.typeFormat.setForeground ( syntax_colors['types'] )
    
    typePatterns = ['\\bfloat\\b', '\\bcolor\\b', '\\bmatrix\\b', '\\bvector\\b', '\\bstring\\b',
                    '\\bpoint\\b', '\\bnormal\\b']
    
    for typePattern in typePatterns:
      typeRule = ( QtCore.QRegExp ( typePattern ), self.typeFormat )
      self.highlightingRules.append ( typeRule )
    
    # single line comment
    self.singleLineCommentFormat = QtGui.QTextCharFormat ()
    self.singleLineCommentFormat.setForeground ( syntax_colors['comment'] )
    singleLineCommentRule = ( QtCore.QRegExp ( '//[^\n]*' ), self.singleLineCommentFormat ) 
    self.highlightingRules.append ( singleLineCommentRule )

    # multiline comment
    self.multiLineCommentFormat = QtGui.QTextCharFormat () 
    self.multiLineCommentFormat.setForeground ( syntax_colors['comment'] )
    self.commentStartExpression = QtCore.QRegExp ( "/\\*" )
    self.commentEndExpression = QtCore.QRegExp ( "\\*/" )
    
    # literal
    self.literalFormat = QtGui.QTextCharFormat ()
    self.literalFormat.setForeground ( syntax_colors['literal'] )
    literalRule_1 = ( QtCore.QRegExp ( '\"[A-Za-z0-9_]+\"' ), self.literalFormat )
    literalRule_2 = ( QtCore.QRegExp ( "\'[A-Za-z0-9_]+\'" ), self.literalFormat ) 
    self.highlightingRules.append ( literalRule_1 )
    self.highlightingRules.append ( literalRule_2 )

    # function
    self.functionFormat = QtGui.QTextCharFormat ()
    self.functionFormat.setForeground ( syntax_colors['function'] )
    functionRule = ( QtCore.QRegExp ( '\\b[A-Za-z0-9_]+(?=\\()' ), self.functionFormat ) 
    self.highlightingRules.append ( functionRule )
  #
  #
  #  
  def highlightBlock ( self, text ):
    #print "DBG: highlightBlock %s" % ( text )
    # apply rules
    for rule in self.highlightingRules:
      expression = QtCore.QRegExp ( rule[0] )
      index = expression.indexIn ( text )
      while index >= 0:
        length = expression.matchedLength ()
        self.setFormat ( index, length, rule[1] )
        index = expression.indexIn ( text, index + length )
            
    self.setCurrentBlockState ( 0 )
    
    # multiline comment handling 
    startIndex = 0;
    if self.previousBlockState() != 1:
      startIndex = self.commentStartExpression.indexIn ( text )

    while startIndex >= 0:
      endIndex = self.commentEndExpression.indexIn ( text, startIndex )
      commentLength = 0
      if endIndex == -1:
        self.setCurrentBlockState ( 1 )
        commentLength = text.length() - startIndex
      else:
        commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()
  
      self.setFormat ( startIndex, commentLength, self.multiLineCommentFormat )
      startIndex = self.commentStartExpression.indexIn ( text, startIndex + commentLength )  
      