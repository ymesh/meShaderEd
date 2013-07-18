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
      if param.label != '' :
        label_text = param.label
      else :
        label_text = param.name
      self.setText ( label_text )
      if self.param.provider == 'primitive' :
        primitiveColor = QtGui.QColor ( 240, 150, 0 )
        palette = QtGui.QPalette ()
        palette.setColor ( QtGui.QPalette.WindowText, primitiveColor )
        self.setPalette ( palette )
      if self.param.detail == 'varying' :
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
    self.param.label = newLabel
    self.setText ( newLabel )
    self.editLabel.adjustSize ()
    self.adjustSize ()
    self.setVisible ( True )
    self.editLabel.setVisible ( False )
    self.param.paramChanged ()
  #
  # mouseDoubleClickEvent
  #
  def mouseDoubleClickEvent ( self, event ) :
    #
    button = event.button () 
    if button == QtCore.Qt.LeftButton :
      #if DEBUG_MODE : print ">> ParamLabel( %s ).mouseDoubleClickEvent" % self.param.name
      parentLayout = self.parent ().layout ()
      editWidth = parentLayout.columnMinimumWidth ( 0 ) - self.mapToParent ( QtCore.QPoint ( 0, 0 ) ).x () 
      self.setFixedWidth ( editWidth )
      self.editLabel.setFixedWidth ( editWidth )
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
        if DEBUG_MODE : print '* CTRL+LMB (change in shaderParam)' 
        self.param.shaderParam = not self.param.shaderParam
        self.param.paramChanged ()
        return
      elif modifiers == QtCore.Qt.AltModifier :
        if DEBUG_MODE : print '* ALT+LMB ( change detail "uniform/varying")' 
        if self.param.detail == 'varying' :
          self.param.detail = 'uniform'
        else :
          self.param.detail = 'varying' 
        self.param.paramChanged ()
        return
    elif button == QtCore.Qt.RightButton :
      if modifiers == QtCore.Qt.ControlModifier :
        if DEBUG_MODE : print '* CTRL+RMB change provider "primitive"/"internal"'
        if self.param.provider == 'primitive' :
          self.param.provider = ''
        else :
          self.param.provider = 'primitive' 
        self.param.paramChanged ()
        return
      elif modifiers == QtCore.Qt.AltModifier :
        if DEBUG_MODE : print '* ALT+RMB "enable"/"disable" parameter'
        self.param.enabled = not self.param.enabled
        self.param.paramChanged ()
    QtGui.QWidget.mousePressEvent ( self, event )    
