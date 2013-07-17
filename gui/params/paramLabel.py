"""

 paramLabel.py

"""
from PyQt4 import QtGui, QtCore

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI
#
# ParamLabel -- editable parameter label
#
class ParamLabel ( QtGui.QLabel ) :
  #
  # __init__
  #
  def __init__ ( self, parent, param = None ) :
    #
    super ( QtGui.QLabel, self ).__init__ ( parent )
    self.widget = parent
    self.param = param
    if param is not None :
      self.setText ( param.label )
      if self.param.provider == "primitive" :
        primitiveColor = QtGui.QColor ( 240, 150, 0 )
        palette = QtGui.QPalette ()
        palette.setColor ( QtGui.QPalette.WindowText, primitiveColor )
        self.setPalette ( palette )
      if self.param.detail == "varying" :
        font = QtGui.QFont ()
        font.setItalic ( True )
        self.setFont ( font )
    #self.setScaledContents ( True )
    #self.setMouseTracking ( True ) 
    self.buildGui ()
    self.updateGui ()
    self.connectSignals ()
  #
  #  __del__
  #
  def __del__ ( self ) :
    #
    self.disconnectSignals ()
  #
  # buildGui
  #
  def buildGui ( self ) :
    #
    self.editLabel = QtGui.QLineEdit ( self )
    self.editLabel.setText ( self.text () )
    self.editLabel.setVisible ( False )
  #
  # updateGui
  #
  def updateGui ( self ) :
    #
    pass
  #
  # connectSignals
  #
  def connectSignals ( self ) :
    #
    self.connect ( self.editLabel, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditingFinished )
  #
  # disconnectSignals
  #
  def disconnectSignals ( self ) :
    #
    self.disconnect ( self.editLabel, QtCore.SIGNAL ( 'editingFinished()' ), self.onEditingFinished )
  """
  #
  # mouseMoveEvent  
  #
  def mouseMoveEvent ( self, event ) :
    #
    if DEBUG_MODE : print ">> ParamLabel( %s ).mouseMoveEvent" % self.param.name
    QtGui.QWidget.mouseMoveEvent ( self, event )
  """
  #
  # onEditingFinished
  #
  def onEditingFinished ( self ) :
    #
    if DEBUG_MODE : print ">> ParamLabel( %s ).onEditingFinished" % self.param.name
    newLabel = str ( self.editLabel.text () ).strip ()
    if newLabel == '' : newLabel = self.param.name
    print ( '*** newLabel = %s' % newLabel )
    self.param.label = newLabel
    self.setText ( newLabel )
    print '*** self.size = %d %d' % ( self.rect ().width (), self.rect ().height () )
    self.editLabel.adjustSize ()
    self.adjustSize ()
    print '*** self.size = %d %d' % ( self.rect ().width (), self.rect ().height () )
    self.setVisible ( True )
    self.editLabel.setVisible ( False )
    self.param.paramChanged ()
    #self.emit ( QtCore.SIGNAL ( 'nodeParamChanged' ), self.widget.gfxNode, self.param )
  #
  # mouseDoubleClickEvent
  #
  def mouseDoubleClickEvent ( self, event ) :
    #
    button = event.button () 
    if button == QtCore.Qt.LeftButton :
      if DEBUG_MODE : print ">> ParamLabel( %s ).mouseDoubleClickEvent" % self.param.name
      if DEBUG_MODE : print ">> ParamLabel width %d" % self.width ()
      if DEBUG_MODE : print ">> ParamLabel.parentWidget width %d" % self.parentWidget ().width () 
      if DEBUG_MODE : print ">> ParamLabel.parent %s" % self.parent ()
      parentLayout = self.parent ().layout ()
      if DEBUG_MODE : print ">> ParamLabel.parent layout %s (%d)" % ( parentLayout, parentLayout.columnMinimumWidth ( 0 ) )
      print self.rect ().x (), self.rect ().y (), self.rect ().width (), self.rect ().height ()
      print self.mapToParent ( QtCore.QPoint ( 0, 0 ) ).x () 
      
      editWidth = parentLayout.columnMinimumWidth ( 0 ) - self.mapToParent ( QtCore.QPoint ( 0, 0 ) ).x () 
      self.setFixedWidth ( editWidth )
      self.editLabel.setFixedWidth ( editWidth )
      #self.setVisible ( False )
      self.editLabel.setVisible ( True )
      
      return
    QtGui.QWidget.mouseDoubleClickEvent ( self, event )
  #
  # mousePressEvent
  #
  def mousePressEvent ( self, event ) :
    #
    #if DEBUG_MODE : print ">> ParamLabel( %s ).mousePressEvent" % self.param.name
    button = event.button () 
    modifiers =event.modifiers ()
    if button == QtCore.Qt.LeftButton :
      if modifiers == QtCore.Qt.ControlModifier :
        print '* CTRL+LMB (change in shaderParam)' 
        self.param.shaderParam = not self.param.shaderParam
        self.param.paramChanged ()
        return
      elif modifiers == QtCore.Qt.AltModifier :
        print '* ALT+LMB ( change detail "uniform/varying")' 
        if self.param.detail == 'varying' :
          self.param.detail = 'uniform'
        else :
          self.param.detail = 'varying' 
        self.param.paramChanged ()
        return
    elif button == QtCore.Qt.RightButton :
      if modifiers == QtCore.Qt.ControlModifier :
        print '* CTRL+RMB change provider "primitive"/"internal"'
        if self.param.provider == 'primitive' :
          self.param.provider = ''
        else :
          self.param.provider = 'primitive' 
        self.param.paramChanged ()
        return
    QtGui.QWidget.mousePressEvent ( self, event )    
