#!/usr/local/bin/python
#
#
# meShaderEd.py
#
# version 0.2.0 27 May 2012
# version 0.1.1 16 May 2012
# version 0.1.0 13 May 2012
# version 0.0.1 5 Mar 2011
#
# written by Yuri.Meshalkin (mesh@kpp.kiev.ua)
#
# Initial code and data structure was based on 
# ShaderLink of Libero Spagnolini (Libe)
#   http://libe.ocracy.org/shaderlink.html
#   http://code.google.com/p/shaderlink/
#
# And idea of open source RSL tool belongs to Alexei Puzikov (Kidd)
#   http://code.google.com/p/shaderman/
#
# The RenderMan Shader Editor
#
#
#===============================================================================

import sys
import os
#import ntpath

from PyQt4 import QtCore, QtGui

from core.meCommon import *
from core.nodeLibrary import NodeLibrary
from core.meRendererPreset import meRendererPreset

from global_vars import app_global_vars

root = normPath ( sys.path[0] )

app_settings = QtCore.QSettings( QtCore.QSettings.IniFormat, 
                                 QtCore.QSettings.UserScope,
                                 "mesh",  "meShaderEd" ) 

#
#
def setDefaultValue ( key, def_value ) :
  if not app_settings.contains( key ):
    app_settings.setValue ( key, def_value )
  
  value = app_settings.value( key )
  if value.toString() == 'true' : value = True
  elif value.toString() == 'false' : value = False
  else :
    value = str ( value.toString() )
  return value
#
#
def getDefaultValue ( settings, group, key ) :
  if group != '' : settings.beginGroup ( group )
  value = settings.value( key )
  if group != '' : settings.endGroup ( )
  if value.toString() == 'true' : value = True
  elif value.toString() == 'false' : value = False
  else :
    value = str ( value.toString() )
  return value  
#
#  
defRenderer = setDefaultValue ( 'defRenderer','3Delight' )
app_renderer = meRendererPreset ( os.path.join ( root, 'renderers.xml' ), defRenderer )  
#app_renderer.setPresetFile ( os.path.join( root, 'renderers.xml' ), defRenderer ) 
   
#
#
#
def main ():
  
  #global root
  
  app = QtGui.QApplication ( sys.argv )
  
  app_settings.setValue ( 'root', normPath ( root ) )
  
  temp_dir = setDefaultValue ( 'temp', normPath ( os.path.join ( root, 'tmp' ) ) )
  
  project_dir = setDefaultValue ( 'project', normPath ( os.path.join ( root, 'samples' ) ) )
  project_shaders = setDefaultValue ( 'project_shaders', normPath ( os.path.join ( project_dir,'shaders' ) ) )
  project_textures = setDefaultValue ( 'project_textures',normPath ( os.path.join ( project_dir,'textures' ) ) )
  
  shader_networks_dir = setDefaultValue ( 'shader_networks', normPath ( os.path.join ( project_shaders,'shn' ) ) )
  shader_sources_dir = setDefaultValue ( 'shader_sources', normPath ( os.path.join ( project_shaders,'src' ) ) )
  shader_output_dir = project_shaders
  
  lib_dir = setDefaultValue ( 'lib', normPath ( os.path.join ( root, 'lib' ) ) ) 
  node_dir = setDefaultValue ( 'nodes', normPath ( os.path.join ( lib_dir, 'nodes' ) ) )
  texture_dir = setDefaultValue ('texture', normPath ( os.path.join ( lib_dir, 'textures' ) ) )
  shaders_dir = setDefaultValue ('shaders', normPath ( os.path.join ( lib_dir, 'shaders' ) ) )
  include_dir = setDefaultValue ('include', normPath ( os.path.join ( root, 'include' ) ) )
  
  createMissingDirs ( [temp_dir, lib_dir, project_dir, project_shaders, project_textures] )
  createMissingDirs ( [shader_networks_dir, shader_sources_dir] )
  createMissingDirs ( [node_dir, texture_dir, shaders_dir, include_dir] )
  
  #  path(), filePath(), absolutePath(), and absoluteFilePath().
  
  #print 'root = %s' % ( root )
  #print 'lib_dir = %s' % ( lib_dir )
  #print 'node_dir = %s' % ( node_dir )
  #
  # setup globals
  #
  app_global_vars[ 'RootPath' ] = root
  app_global_vars[ 'TempPath' ] = temp_dir
  app_global_vars[ 'ProjectPath' ] = project_dir
  app_global_vars[ 'ProjectShaders' ] = project_shaders
  app_global_vars[ 'ProjectTextures' ] = project_textures
  
  app_global_vars[ 'ProjectNetworks' ] = shader_networks_dir
  app_global_vars[ 'ProjectSources' ] = shader_sources_dir
  
  app_global_vars[ 'LibPath' ] = lib_dir
  app_global_vars[ 'NodesPath' ] = node_dir
  app_global_vars[ 'TexturePath' ] = texture_dir
  app_global_vars[ 'ShaderPath' ] = shaders_dir 
  app_global_vars[ 'IncludePath' ] = include_dir 
  
  app_global_vars[ 'TextureSearchPath' ] = sanitizeSearchPath ( texture_dir )
  app_global_vars[ 'ShaderSearchPath' ] = sanitizeSearchPath ( shaders_dir )
  
  app_global_vars[ 'ProjectSearchPath' ] = sanitizeSearchPath ( project_dir )
  app_global_vars[ 'ProjectSearchShaders' ] = sanitizeSearchPath ( project_shaders )
  app_global_vars[ 'ProjectSearchTextures' ] = sanitizeSearchPath ( project_textures )
  
  app_global_vars[ 'Renderer' ] = app_renderer.getCurrentValue( 'renderer', 'name' ) 
  app_global_vars[ 'RendererFlags' ] = app_renderer.getCurrentValue( 'renderer', 'flags' ) 
  app_global_vars[ 'ShaderCompiler' ] = app_renderer.getCurrentValue( 'shader', 'compiler' )
  app_global_vars[ 'ShaderDefines' ] = app_renderer.getCurrentValue( 'shader', 'defines' )
  app_global_vars[ 'TEX' ] = app_renderer.getCurrentValue( 'texture', 'extension' )
  app_global_vars[ 'SLO' ] = app_renderer.getCurrentValue( 'shader', 'extension' )
  
  print 'TextureSearchPath = %s' % app_global_vars[ 'TextureSearchPath' ]
  print 'ShaderSearchPath = %s' % app_global_vars[ 'ShaderSearchPath' ]
  print 'Renderer = %s' % app_global_vars[ 'Renderer' ]
  
  #app_global_vars[ 'RibPath' ] = ''
  #app_global_vars[ 'DisplayPath' ] = ''
  
    
  app_settings.beginGroup( 'WorkArea' )
  
  #grid_enabled = bool( setDefaultValue( 'grid_enabled', True ).toString() )
  grid_enabled = setDefaultValue ( 'grid_enabled', True )
  grid_size = int( setDefaultValue ( 'grid_size', 10 ) )
  grid_snap = setDefaultValue ( 'grid_snap', True )
  reverse_flow = setDefaultValue ( 'reverse_flow', False )
  straight_links = setDefaultValue ( 'straight_links', True )
  
  app_settings.endGroup( )
  
  from gui.MainWindow import MainWindow
   
  window = MainWindow () #, rendererPreset )
  window.show ()
  
  # It's exec_ because exec is a reserved word in Python
  sys.exit ( app.exec_ () )
#
#
#

if __name__ == "__main__":
  #safeEffects = QtCore.QT_VERSION >= 0x40600 and QtCore.PYQT_VERSION > 0x40704
  print sys.version
  print ( "QT_VERSION = %0X" ) % QtCore.QT_VERSION
  print ( "PYQT_VERSION = %0X" ) % QtCore.PYQT_VERSION
  
  if ( sys.platform == 'win32' ) :  
    #pass
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create ( "Cleanlooks" ) )
    QtGui.QApplication.setPalette( QtGui.QApplication.style().standardPalette() )
  
  main()
