#===============================================================================
# meRendererSetup.py
#
# ver. 1.0.0
# Wed Jun 16 14:45:19 EEST 2010 @531 /Internet Time/
# Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
# 
# Dialog for managing renderer presets
# 
# Presets are stored in xml file 
#
# app_settings['rendererPresets'] 
# app_settings['defRenderer'] 
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui, QtXml

from ui_meRendererSetup import Ui_meRendererSetup

class meRendererSetup ( QtGui.QDialog ):
  def __init__ ( self, rendererPreset ):
    QtGui.QDialog.__init__(self)

    self.rendererPreset = rendererPreset
    self.labelsReady = False
          
    #self.debugPrint()
    self.buildGui()

  def buildGui( self ):
    # build the gui created with QtDesigner
    self.ui=Ui_meRendererSetup( )
    self.ui.setupUi( self )
    
    font = QtGui.QFont()
    if( sys.platform == 'win32' ) :
      # Runing on windows, override font sizes from Designer to default 
      font.setPointSize(8)
    else :
      font.setPointSize(10)
    self.ui.labelPreset.setFont(font)
    self.ui.listPreset.setFont(font)
    self.ui.newButton.setFont(font)
    self.ui.deleteButton.setFont(font)
    self.ui.cancelButton.setFont(font)
    self.ui.okButton.setFont(font)
    self.ui.saveButton.setFont(font)
    self.ui.tabs.setFont(font)
    self.ui.labelName.setFont(font)
    self.ui.labelCmd.setFont(font)
    self.ui.labelFlags.setFont(font)
    self.ui.labelCompiler.setFont(font)
    self.ui.labelShaderInfo.setFont(font)
    self.ui.labelDefines.setFont(font)
    self.ui.labelShaderExt.setFont(font)
    self.ui.labelShaderExt.setFont(font)
    self.ui.labelTexMake.setFont(font)
    self.ui.labelTexInfo.setFont(font)
    self.ui.labelTexViewer.setFont(font)
    self.ui.labelTexExt.setFont(font)

    self.labelsReady = False

    for label in self.rendererPreset.getLabels():
      #print ">> buildGui:: adding label %s (%s)" % ( label, self.current_renderer )
      self.ui.listPreset.addItem( label )
    
    self.labelsReady = True
    
    index = self.ui.listPreset.findText( self.rendererPreset.getCurrentPresetName() ) 
    #print ">> buildGui:: set current renderer to: %s (%d)" % ( self.current_renderer, index )
    self.ui.listPreset.setCurrentIndex( -1 )
    self.ui.listPreset.setCurrentIndex( index ) 
    
    #self.ui.listPreset.setCurrentIndex( len(self.presets) - 1 ) 
    
  def getDataFromGui( self ):
    # ckeck if current_renderer still exists after deleting preset
    #print ">> getDataFromGui:: current renderer to: %s" % self.rendererPreset.getCurrentPresetName() 
      
    self.rendererPreset.setCurrentValue( 'renderer','name',self.ui.lineCmd.text() )
    self.rendererPreset.setCurrentValue( 'renderer','flags', self.ui.lineFlags.text() )
    self.rendererPreset.setCurrentValue( 'shader','compiler', self.ui.lineCompiler.text() )
    self.rendererPreset.setCurrentValue( 'shader','sloinfo', self.ui.lineShaderInfo.text() )
    self.rendererPreset.setCurrentValue( 'shader','defines', self.ui.lineDefines.text() )
    self.rendererPreset.setCurrentValue( 'shader','extension', self.ui.lineShaderExt.text() )
    self.rendererPreset.setCurrentValue( 'texture','texmake', self.ui.lineTexMake.text() )
    self.rendererPreset.setCurrentValue( 'texture','texinfo', self.ui.lineTexInfo.text() )
    self.rendererPreset.setCurrentValue( 'texture','viewer', self.ui.lineTexViewer.text() )
    self.rendererPreset.setCurrentValue( 'texture','extension', self.ui.lineTexExt.text() )
      
  def onIndexChanged( self, name ): 
    #print ">> onIndexChanged:: self.labelsReady == %d" % self.labelsReady
    if ( self.labelsReady and name != '' ):
      # change current renderer
      self.rendererPreset.setCurrentPresetName( str( name ) )
      self.updateGui()
    
  def updateGui( self ):
    # redraw gui elements
    #print ">> updateGui:: current renderer: %s" % self.rendererPreset.getCurrentPresetName() 
    if self.rendererPreset.size() > 0:
      self.ui.lineName.setText( self.rendererPreset.getCurrentPresetName() )
      self.ui.lineCmd.setText( self.rendererPreset.getCurrentValue( 'renderer','name' ) )
      self.ui.lineFlags.setText( self.rendererPreset.getCurrentValue( 'renderer','flags') )
      self.ui.lineCompiler.setText( self.rendererPreset.getCurrentValue( 'shader','compiler') )
      self.ui.lineShaderInfo.setText( self.rendererPreset.getCurrentValue( 'shader','sloinfo') )
      self.ui.lineDefines.setText( self.rendererPreset.getCurrentValue( 'shader','defines') )
      self.ui.lineShaderExt.setText( self.rendererPreset.getCurrentValue( 'shader','extension') )
      self.ui.lineTexMake.setText( self.rendererPreset.getCurrentValue( 'texture','texmake') )
      self.ui.lineTexInfo.setText( self.rendererPreset.getCurrentValue( 'texture','texinfo') )
      self.ui.lineTexViewer.setText( self.rendererPreset.getCurrentValue( 'texture','viewer') )
      self.ui.lineTexExt.setText( self.rendererPreset.getCurrentValue( 'texture','extension') )
      self.ui.deleteButton.setEnabled( True )
      self.ui.tab1.setEnabled( True )
      self.ui.tab2.setEnabled( True)
      self.ui.tab3.setEnabled( True )
    else:
      self.ui.deleteButton.setEnabled( False )
      self.ui.tab1.setEnabled( False )
      self.ui.tab2.setEnabled( False )
      self.ui.tab3.setEnabled( False )
      self.ui.lineName.clear()
      self.ui.lineCmd.clear()
      self.ui.lineFlags.clear()
      self.ui.lineCompiler.clear()
      self.ui.lineShaderInfo.clear()
      self.ui.lineDefines.clear()
      self.ui.lineShaderExt.clear()
      self.ui.lineTexMake.clear()
      self.ui.lineTexInfo.clear()
      self.ui.lineTexViewer.clear()
      self.ui.lineTexExt.clear()
  
  def onNewPreset( self ):
    # create new empty preset
    title = 'Untitled' 
    newLabel = title
    i = 0
    while True :
      if newLabel in self.rendererPreset.getLabels() :
        newLabel = title + str(i)
        i += 1
        continue
      else :
        break;
    self.rendererPreset.addPreset( newLabel )
    self.updateGui()
    self.ui.listPreset.addItem( newLabel ) 
    self.ui.listPreset.setCurrentIndex( self.rendererPreset.size() - 1 ) 
    
    
  def onDeletePreset( self ):
    # delete existing preset
    if self.rendererPreset.size() > 0 :
      msgBox = QtGui.QMessageBox()
      ret = msgBox.warning( self, 'Warning', "Do you really want to delete this preset?", 
      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,  QtGui.QMessageBox.No )
      
      if ret ==  QtGui.QMessageBox.Yes :
        self.rendererPreset.deleteCurrentPreset()
        i = self.ui.listPreset.currentIndex()
        self.ui.listPreset.removeItem(i)
        self.rendererPreset.setCurrentPresetName( str( self.ui.listPreset.currentText() ) )
      
  def onEditLabel( self ):
    # edit label
    newLabel = str( self.ui.lineName.text() )
    if ( self.rendererPreset.getCurrentPresetName() != newLabel ) :
      if newLabel not in self.rendererPreset.getLabels() :
        self.rendererPreset.renameCurrentPreset( newLabel )
        # rename current preset ComboBox item to new label
        i = self.ui.listPreset.currentIndex()
        self.ui.listPreset.setItemText( i, newLabel )
      else :
        # this label already exists, so restore to previose
        self.ui.lineName.setText( self.rendererPreset.getCurrentPresetName() )
    
  def onSave( self ):
    # get data from Gui for current renderer before saving
    self.getDataFromGui()
    self.emit( QtCore.SIGNAL( "presetChanged" ) )
    self.emit( QtCore.SIGNAL( "savePreset" ) )
    
    #self.rendererPreset.saveSettings ()

    self.done( 0 ) 
    
  def onSelect( self ):
    # get data from Gui for current renderer before saving
    self.getDataFromGui()
    self.emit( QtCore.SIGNAL( "presetChanged" ) )
    self.done( 0 ) 
  
  def debugPrint( self ): 
    # print data structure for debug purpose
    print "current_renderer = %s" % self.rendererPreset.getCurrentPresetName()

    for label in self.rendererPreset.getLabels():
      print "> Preset name = %s" % label
      for section in self.rendererPreset.getSections() :
        print "\"%s\":" % section
        for name in self.rendererPreset.getNames( section ) :
          print "%s = %s" %  (name, self.rendererPreset.getValue( label, section, name ) )
  
