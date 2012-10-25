#===============================================================================
# ProjectSetup.py
#
# ver. 1.0.0
# Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
# 
# Dialog for managing project directories
# 
#===============================================================================

import os, sys
from PyQt4 import QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars

from ui_projectSetup import Ui_ProjectSetup
#
#
#
class ProjectSetup( QtGui.QDialog ):
  #
  #
  def __init__( self, app_settings ):
    QtGui.QDialog.__init__(self)

    self.app_settings = app_settings
    self.rootDir = str( self.app_settings.value('project').toString() )      
    #self.debugPrint()
    self.buildGui ()
  #
  #
  def buildGui ( self ):
    # build the gui created with QtDesigner
    self.ui = Ui_ProjectSetup( )
    self.ui.setupUi( self )
    
    ##font = QtGui.QFont()
    ##if( sys.platform == 'win32' ) :
      # Runing on windows, override font sizes from Designer to default 
    ##  font.setPointSize(8)
    ##else :
    ##  font.setPointSize(10)
    
    self.ui.lineEdit_project.setText( self.rootDir )

    self.ui.lineEdit_network.setText( toRelativePath( self.rootDir, str( self.app_settings.value('shader_networks').toString() ) ) )
    self.ui.lineEdit_sources.setText( toRelativePath( self.rootDir, str( self.app_settings.value('shader_sources').toString() ) ) )
    self.ui.lineEdit_shaders.setText( toRelativePath( self.rootDir, str( self.app_settings.value('project_shaders').toString() ) ) )
    self.ui.lineEdit_textures.setText( toRelativePath( self.rootDir, str( self.app_settings.value('project_textures').toString() ) ) )
  #
  #
  #
  def setupProject ( self ) :
    #
    project_shaders = normPath ( fromRelativePath( self.rootDir, str( self.ui.lineEdit_shaders.text() ) ) )
    project_textures = normPath ( fromRelativePath( self.rootDir, str( self.ui.lineEdit_textures.text() ) ) )
    
    shader_networks_dir = normPath ( fromRelativePath( self.rootDir, str( self.ui.lineEdit_network.text() ) ) )
    shader_sources_dir = normPath ( fromRelativePath( self.rootDir, str( self.ui.lineEdit_sources.text() ) ) )
    
    createMissingDirs ( [self.rootDir, project_shaders, project_textures, shader_networks_dir, shader_sources_dir] )
    
    return ( project_shaders, project_textures, shader_networks_dir, shader_sources_dir )
  #
  #  
  def onBrowseProjectDir ( self ):
    curDir = self.ui.lineEdit_project.text()
    newDir = QtGui.QFileDialog.getExistingDirectory( self, "Select Project Directory", curDir )
    if newDir != '' : 
      self.rootDir = normPath( newDir )
      self.ui.lineEdit_project.setText( self.rootDir )
      self.setupProject ()
  #
  #  
  def onBrowseNetworksDir ( self ):
    curDir = fromRelativePath( self.rootDir, str( self.ui.lineEdit_network.text() ) )
    newDir = QtGui.QFileDialog.getExistingDirectory( self, "Select Shader Networks Directory", curDir )
    if newDir != '' : 
      self.ui.lineEdit_network.setText( toRelativePath( self.rootDir, normPath( newDir ) ) )
  #
  #  
  def onBrowseSourcesDir ( self ):
    curDir = fromRelativePath( self.rootDir, str( self.ui.lineEdit_sources.text() ) )
    newDir = QtGui.QFileDialog.getExistingDirectory( self, "Select Shader Sources Directory", curDir )
    if newDir != '' : 
      self.ui.lineEdit_sources.setText( toRelativePath( self.rootDir, normPath( newDir ) ) )
  #
  #  
  def onBrowseShadersDir ( self ):
    curDir = fromRelativePath( self.rootDir, str( self.ui.lineEdit_shaders.text() ) )
    newDir = QtGui.QFileDialog.getExistingDirectory( self, "Select Compiled Shaders Directory", curDir )
    if newDir != '' : 
      self.ui.lineEdit_shaders.setText( toRelativePath( self.rootDir, normPath( newDir ) ) )
  #
  #  
  def onBrowseTexturesDir ( self ):
    curDir = fromRelativePath( self.rootDir, str( self.ui.lineEdit_textures.text() ) )
    newDir = QtGui.QFileDialog.getExistingDirectory( self, "Select Textures Directory", curDir )
    if newDir != '' : 
      self.ui.lineEdit_textures.setText( toRelativePath( self.rootDir, normPath( newDir ) ) )
  #
  #  
  def reject ( self ):
    #print ">> ProjectSetup: reject"
    #self.emit( QtCore.SIGNAL( "rejected()" ) )
    self.done( 0 ) 
  #  
  #  
  def accept ( self ):
    #print ">> ProjectSetup: accept"

    #project_dir = normPath ( self.ui.lineEdit_project.text() )
    ( project_shaders, project_textures, shader_networks_dir, shader_sources_dir ) = self.setupProject ()
    
    #project_shaders = normPath ( fromRelativePath( self.rootDir, str( self.ui.lineEdit_shaders.text() ) ) )
    #project_textures = normPath ( fromRelativePath( self.rootDir, str( self.ui.lineEdit_textures.text() ) ) )
    
    #shader_networks_dir = normPath ( fromRelativePath( self.rootDir, str( self.ui.lineEdit_network.text() ) ) )
    #shader_sources_dir = normPath ( fromRelativePath( self.rootDir, str( self.ui.lineEdit_sources.text() ) ) )
    
    self.app_settings.setValue( 'project', self.rootDir )

    self.app_settings.setValue( 'shader_networks', shader_networks_dir )
    self.app_settings.setValue( 'shader_sources', shader_sources_dir )
    self.app_settings.setValue( 'project_shaders', project_shaders )
    self.app_settings.setValue( 'project_textures', project_textures )
    
    app_global_vars[ 'ProjectPath' ] = self.rootDir
    
    app_global_vars[ 'ProjectShaders' ] = project_shaders
    app_global_vars[ 'ProjectTextures' ] = project_textures
    
    app_global_vars[ 'ProjectNetworks' ] = shader_networks_dir
    app_global_vars[ 'ProjectSources' ] = shader_sources_dir
    
    app_global_vars[ 'ProjectSearchPath' ] = sanitizeSearchPath ( self.rootDir )
    app_global_vars[ 'ProjectSearchShaders' ] = sanitizeSearchPath ( project_shaders )
    app_global_vars[ 'ProjectSearchTextures' ] = sanitizeSearchPath ( project_textures )
    
    #createMissingDirs ( [self.rootDir, project_shaders, project_textures, shader_networks_dir, shader_sources_dir] )
    
    #self.emit( QtCore.SIGNAL( "accepted()" ) )
    self.done( 0 ) 