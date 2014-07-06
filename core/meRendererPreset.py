"""

  meRendererPreset.py

"""
import os, sys
from PyQt4 import QtCore, QtXml
from PyQt4.QtCore import QDir, QFile, QVariant
#
# meRendererInfo
#
class meRendererInfo () :
  #
  # __init__
  #
  def __init__ ( self, presetName = None ) :
    #
    self.PresetName = presetName
    
    self.RendererName = ''
    self.RendererFlags = ''
    
    self.ShaderCompiler = ''
    self.ShaderDefines = ''
    self.ShaderInfo = ''
    self.ShaderExt = ''
    
    self.TextureMake = ''
    self.TextureInfo = ''
    self.TextureViewer = ''
    self.TextureExt = ''
  #
  # parseFromXML
  #
  def parseFromXML ( self, xml_preset ) :
    #
    self.PresetName = str ( xml_preset.attributes ().namedItem ( 'name' ).nodeValue () )
    
    renderer = xml_preset.namedItem ( 'renderer' )
    shader = xml_preset.namedItem ( 'shader' )
    texture = xml_preset.namedItem ( 'texture' )
    
    self.RendererName = str ( renderer.attributes ().namedItem ( 'name' ).nodeValue () )
    self.RendererFlags = str ( renderer.attributes ().namedItem ( 'flags' ).nodeValue () )
    
    self.ShaderCompiler = str ( shader.attributes ().namedItem ( 'compiler' ).nodeValue () )
    self.ShaderDefines = str ( shader.attributes ().namedItem ( 'defines' ).nodeValue () )
    self.ShaderInfo = str ( shader.attributes ().namedItem ( 'sloinfo' ).nodeValue () )
    self.ShaderExt = str ( shader.attributes ().namedItem ( 'extension' ).nodeValue () )
    
    self.TextureMake = str ( texture.attributes ().namedItem ( 'texmake' ).nodeValue () )
    self.TextureInfo = str ( texture.attributes ().namedItem ( 'texinfo' ).nodeValue () )
    self.TextureViewer = str ( texture.attributes ().namedItem ( 'viewer' ).nodeValue () )
    self.TextureExt = str ( texture.attributes ().namedItem ( 'extension' ).nodeValue () )
    
    print ( '* %s' % self.PresetName )
  #
  # parseToXML
  #
  def parseToXML ( self, dom ) :
    #
    xml_preset = dom.createElement ( 'preset' )
    xml_preset.setAttribute ( 'name', self.PresetName )
    
    renderer_tag = dom.createElement ( 'renderer' )
    renderer_tag.setAttribute ( 'name', self.RendererName )
    renderer_tag.setAttribute ( 'flags', self.RendererFlags )
    xml_preset.appendChild ( renderer_tag )
    
    shader_tag = dom.createElement ( 'shader' )
    shader_tag.setAttribute ( 'compiler', self.ShaderCompiler )
    shader_tag.setAttribute ( 'defines', self.ShaderDefines )
    shader_tag.setAttribute ( 'sloinfo', self.ShaderInfo )
    shader_tag.setAttribute ( 'extension', self.ShaderExt )
    xml_preset.appendChild ( shader_tag )
    
    texture_tag = dom.createElement ( 'texture' )
    texture_tag.setAttribute ( 'texmake', self.TextureMake )
    texture_tag.setAttribute ( 'texinfo', self.TextureInfo )
    texture_tag.setAttribute ( 'viewer', self.TextureViewer )
    texture_tag.setAttribute ( 'extension', self.TextureExt )
    xml_preset.appendChild ( texture_tag )
    
    return xml_preset
#
# meRendererPreset
#
class meRendererPreset () :
  #
  # __init__
  #
  def __init__ ( self, presetsFileName = None, defaultPresetName = '' ) :
    #
    self.presetsList = []
    self.currentPreset = None
    self.fileName = None
    self.setPresetFile ( presetsFileName, defaultPresetName )
  #  
  # setPresetFile
  #
  def setPresetFile ( self, presetsFileName = '', defaultPresetName = ''  ) :
    #
    self.readSettings ( presetsFileName )
    if len ( self.presetsList ) :
      print ( '>> meRenderPreset::setPresetFile defaultPresetName = %s' % defaultPresetName )
      self.currentPreset = self.getPresetByName ( defaultPresetName ) 
      if self.currentPreset is None :
        self.currentPreset = self.presetsList [ 0 ]
    print ( '>> meRenderPreset::setPresetFile defaultRenderer = %s' % self.currentPreset.PresetName )
  #
  # getPresetNames
  #
  def getPresetNames ( self ) :
    #
    #print ( '>> meRenderPreset::getPresetNames ...' )
    labels = []
    for preset in self.presetsList :
      #print ( ':: PresetName = %s' % str ( preset.PresetName ) )
      labels.append ( str ( preset.PresetName ) )
    labels.sort ()
    return labels
  #
  # getCurrentPresetName 
  #
  def getCurrentPresetName ( self ) : 
    #
    return self.currentPreset.PresetName
  #
  # setCurrentPresetName
  #
  def setCurrentPresetByName ( self, presetName ) : 
    #
    self.currentPreset = self.getPresetByName ( presetName )
  #
  # getPresetByName
  #
  def getPresetByName ( self, presetName ) : 
    #
    currentPreset = None
    for preset in self.presetsList :
      if preset.PresetName == presetName :
        currentPreset = preset
    return currentPreset
  #
  # addPreset
  #
  def addPreset ( self, presetName ) :
    #
    print ( '>> adding preset %s ...' % presetName )
    preset = meRendererInfo ( presetName )
    self.presetsList.append ( preset )
  #
  # deleteCurrentPreset
  #
  def deleteCurrentPreset ( self ) : 
    #
    print ( '>> deleting preset %s ...' % self.currentPreset.PresetName )
    self.presetsList.remove ( self.currentPreset )
  #
  # renameCurrentPreset
  #
  def renameCurrentPreset ( self, newLabel ) :
    # 
    self.currentPreset.PresetName = newLabel
  #
  # Read Settings from preset file
  #
  def readSettings ( self, fileName ) :
    #
    dom = QtXml.QDomDocument ( 'renderers' )

    file = QFile ( fileName )
    if file.open ( QtCore.QIODevice.ReadOnly ) :
      if dom.setContent ( file ) :
        self.fileName = fileName
        root = dom.documentElement ()
        if root.nodeName () == 'renderers' :
          print ( ':: Read Settings from preset file %s ...' % fileName )
          xml_presetList = root.elementsByTagName ( 'preset' )
          for i in range ( 0, xml_presetList.length () ) :
            preset = meRendererInfo ()
            preset.parseFromXML ( xml_presetList.item ( i ) )
            self.presetsList.append ( preset )
        else :
          print '!! unknown Renderer Preset XML document format'
      file.close()
  #
  # Write Settings to preset file
  # 
  def saveSettings ( self ) :
    # 
    result = False
    dom = QtXml.QDomDocument ( 'renderers' )
    root = dom.createElement ( 'renderers' )
    for preset in self.presetsList :
      xml_preset = preset.parseToXML ( dom )
      root.appendChild ( xml_preset )
    dom.appendChild ( root )
      
    file = QFile ( self.fileName )
    if file.open ( QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Text ) :
      if file.write ( dom.toByteArray () ) != -1 :
        result = True
      file.close ()
    return result