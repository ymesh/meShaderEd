#===============================================================================
# meRendererPreset.py
#
# 
#
#===============================================================================
import os, sys
from PyQt4 import QtCore
#
#
#
class meRendererPreset ():
  #
  #
  def __init__ ( self, presetsFileName = None, defaultPresetName = '' ):
        
    self.presets = {}
    
    self.key_list = {}
    self.key_list[ 'renderer' ] = [ 'name', 'flags' ]
    self.key_list[ 'shader' ] = [ 'compiler', 'sloinfo', 'defines', 'extension'  ]
    self.key_list[ 'texture' ] = [ 'texmake', 'texinfo', 'viewer', 'extension'  ]
    
    self.presetName = ''
    self.file = None
    
    self.setPresetFile ( presetsFileName, defaultPresetName )
    
  #  
  #
  def setPresetFile ( self, presetsFileName = '', defaultPresetName = ''  ) :
    #
    if presetsFileName != '' :
      self.file = QtCore.QFile ( presetsFileName )
      if self.file.exists() :
        print ">> meRenderPreset:: preset file = %s" % self.file.fileName() 
        self.readSettings()
      else :
        # create preset file
        if self.file.open( QtCore.QIODevice.ReadWrite | QtCore.QIODevice.Text  ) :
          self.file.close()
        else :
          print ">> meRenderPreset:: Error can't create preset file = %s" % self.file.fileName() 
          
      #labels = self.getLabels()
      if len ( self.presets ) :
        if defaultPresetName not in self.presets.keys() :
          self.presetName = self.getLabels()[0]
        else :
          self.presetName = defaultPresetName
      
      print ">> meRenderPreset:: defaultRenderer = %s" % self.presetName 
  #   
  #
  def getCurrentValue ( self, section, name ):
    #print self.presetName
    return str( self.getValue( self.presetName, section, name ) )
  #
  #
  def setCurrentValue ( self, section, name, value ):
    return str( self.setValue( self.presetName, section, name, value ) )
  #
  #  
  def getValue ( self, label, section, name ):
    #print self.presets.keys()
    return self.presets[label][section].get( name, '' ) 
  #
  #  
  def setValue ( self, label, section, name, value ):
    #print self.presets.keys()
    self.presets[label][section][name] = value
  #
  #  
  def size( self ): return len ( self.presets )
  #
  #  
  def getLabels ( self ):
    labels = self.presets.keys()
    labels.sort()
    #print labels
    return labels
  #
  #  
  def getPreset ( self, label ): return self.presets[ label ].copy()
  #
  #  
  def getSections ( self ): return self.key_list.keys() 
  #
  #  
  def getNames ( self, section ): return self.key_list[section]
  #
  #  
  def getCurrentPresetName ( self ): return self.presetName
  #
  #
  def setCurrentPresetName ( self, presetName ): self.presetName = presetName
  #
  #  
  def addPreset( self, presetName ):
    self.presetName = presetName
    self.presets[ presetName ] = { 'renderer':{}, 'shader':{}, 'texture':{} } 
  #
  #  
  def deleteCurrentPreset ( self ): self.presets.pop( self.presetName )
  #
  #  
  def renameCurrentPreset ( self, newLabel ):
    # remove and store data for current key
    preset = self.presets.pop( self.presetName )
    # replace current key with new label
    self.presets.setdefault( newLabel, preset )
    self.presetName = newLabel
  #
  # Read Settings from preset file
  #
  def readSettings ( self ):
    # read XML by QXmlStreamReader 
    # fix changed locations between versions
    try:
      from PyQt4.QtCore import QXmlStreamReader 
    except:
      from PyQt4.QtXml import QXmlStreamReader 
      
    from PyQt4.QtCore import QXmlStreamReader 
      
    if ( self.file.open( QtCore.QIODevice.ReadWrite | QtCore.QIODevice.Text ) ) : 
      xml = QXmlStreamReader( self.file ) 
      label = ''
      while not xml.atEnd():
        token = xml.readNext()
        if token == QXmlStreamReader.StartElement:
          name = xml.name()
          attr = xml.attributes()
          if name == 'preset' :
            label = str( "%s" % attr.value('name').toString() ) 
            #print "label = %s" % label
            self.presets[ label ] = {}
          elif name in self.key_list.keys() :
            section = str( name.toString() )
            #print "section = %s" % section
            item_list = {}
            for key in self.key_list[ section ] :
              value = str( "%s" % attr.value( key ).toString() )
              item_list[key] = value
              #print "%s = %s" % (key, value)
            
            self.presets[ label ].setdefault( section, item_list.copy() )  
         
      self.file.close()
  #
  # Write Settings to preset file
  # 
  def saveSettings ( self ):
    # write XML by QXmlStreamWriter 
    # fix changed locations between versions
    
    try:
      from PyQt4.QtCore import QXmlStreamWriter
    except:
      from PyQt4.QtXml import QXmlStreamWriter
      
    #from PyQt4.QtCore import QXmlStreamWriter
    #from PyQt4.QtXml import QXmlStreamWriter
    
    if ( self.file.open ( QtCore.QIODevice.ReadWrite | QtCore.QIODevice.Text ) ) :
    #if self.file.exists() :
      print ">> meRenderPreset:: saveSettings to %s ...." % self.file.fileName() 
      xml = QXmlStreamWriter ( self.file ) 
      xml.setAutoFormatting( True )
      xml.writeStartDocument()
      xml.writeStartElement( 'renderers' )
      
      for label in self.presets.keys() :
        xml.writeStartElement( "preset" )
        xml.writeAttribute( "name", label )
        preset = self.presets[ label ] 
        
        for section in self.key_list.keys() :
          xml.writeStartElement( section )
          item_list = preset[ section ]
          
          for key in item_list.keys() :
            xml.writeAttribute( key, item_list[key] )
          xml.writeEndElement() 
          
        xml.writeEndElement() 
        
      xml.writeEndElement() 
      xml.writeEndDocument()
      self.file.close()
      print ">> meRenderPreset:: saveSettings finished" 
      
