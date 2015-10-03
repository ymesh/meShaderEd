#!/usr/bin/python
"""
 
 meShaderEd.py

 version 0.3.4b (?? Oct 2013)

 Author: Yuri Meshalkin (aka mesh) (mesh@kpp.kiev.ua)

 Initial code and data structure was based on
 ShaderLink of Libero Spagnolini (Libe)
	 http://libe.ocracy.org/shaderlink.html
	 http://code.google.com/p/shaderlink/

 And idea of open source RSL tool belongs to Alexei Puzikov (Kidd)
	 http://code.google.com/p/shaderman/

 The RenderMan Shader Editor

"""
import os, sys
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

from core.meCommon import *
from core.nodeLibrary import NodeLibrary
from core.meRendererPreset import meRendererPreset

from global_vars import app_global_vars, app_colors, DEBUG_MODE

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets

root = normPath ( sys.path [0] )

branchName = ''
version = '0.3.4' + branchName

__version__  = version

app_settings = QtCore.QSettings ( QtCore.QSettings.IniFormat,
																	QtCore.QSettings.UserScope,
																	'mesh', 'meShaderEd' + branchName )
#
# setDefaultValue
#
def setDefaultValue ( key, def_value ) :
	if not app_settings.contains ( key ):
		app_settings.setValue ( key, def_value )
	value = app_settings.value ( key )
	if usePyQt4 :
		if value.toString () == 'true' : value = True
		elif value.toString () == 'false' : value = False
		else :
			if isinstance ( def_value, QtGui.QColor ) :
				value = QtGui.QColor ( value )
			else :  
				value = str ( value.toString () )
	else :
		if value == 'true' : value = True
		elif value == 'false' : value = False
		else :
			if isinstance ( def_value, QtGui.QColor ) :
				value = QtGui.QColor ( value )
			else :  
				value = str ( value )
	return value
#
# getDefaultValue
#
def getDefaultValue ( settings, group, key, def_value = None ) :
	if group != '' : settings.beginGroup ( group )
	value = settings.value ( key )
	if group != '' : settings.endGroup ( )
	if usePyQt4 :
		if value.toString () == 'true' : value = True
		elif value.toString () == 'false' : value = False
		else :
			if def_value is not None and isinstance ( def_value, QtGui.QColor ) :
				value = QtGui.QColor ( value )
			else :  
				value = str ( value.toString () )
	else :
		if value == 'true' or value is True : value = True
		elif value == 'false' or value is False : value = False
		else :
			if def_value is not None and isinstance ( def_value, QtGui.QColor ) :
				value = QtGui.QColor ( value )
			else :  
				value = str ( value )
	return value

#
# getSettingsStrValue 
#
#def getSettingsStrValue ( settings, key ) :  
#	#
#	if  usePyQt4 :
#		return str ( settings.value ( key ).toString () )	
#	else :
#		return str ( settings.value ( key ) )	 
#
# createDefaultProject 
#  
def createDefaultProject ( settings, check_if_exist = False ) :
	#  
	project_filename = getDefaultValue ( settings, '', 'project_filename' )
	project = getDefaultValue ( settings, '', 'project' )
	project_shaders = getDefaultValue ( settings, '', 'project_shaders' )
	project_textures = getDefaultValue ( settings, '', 'project_textures' )
	shader_networks = getDefaultValue ( settings, '', 'shader_networks' )
	shader_sources = getDefaultValue ( settings,  '', 'shader_sources' )
	
	filename = normPath ( os.path.join ( project, project_filename ) )
	if check_if_exist :
		if os.path.exists ( filename ) : 
			print '>> DefaultProject %s already exists...' % filename
			return
	print '>> createDefaultProject %s' % filename
	with open ( filename , 'w') as f :
		f.write ( 'project_shaders=%s\n' % toRelativePath ( project, project_shaders ) )
		f.write ( 'project_textures=%s\n' % toRelativePath ( project, project_textures ) ) 
		f.write ( 'shader_networks=%s\n' % toRelativePath ( project, shader_networks ) )
		f.write ( 'shader_sources=%s\n' % toRelativePath ( project, shader_sources ) )  
	f.closed
#
# openDefaultProject 
#  
def openDefaultProject ( settings, global_vars, project, project_filename ) : 
	#
	ret = False
	if os.path.exists ( project ) : 
		#
		filename = normPath ( os.path.join ( project, project_filename ) )
		project_dir = normPath ( project )
		# setup default setting
		project_shaders = normPath ( os.path.join ( project_dir,'shaders' ) ) 
		project_textures = normPath ( os.path.join ( project_dir,'textures' ) ) 
		shader_networks_dir = normPath ( os.path.join ( project_shaders,'shn' ) )
		shader_sources_dir = normPath ( os.path.join ( project_shaders,'src' ) ) 
		if os.path.exists ( filename ) :
			# read settings from existing project file
			f = open ( filename, 'r' )
			for line in f :
				( key, value ) = line.split ( '=' )
				name = key.strip()
				if name in [ 'project_shaders', 'project_textures', 'shader_networks', 'shader_sources' ] :
					print 'name = %s value = %s' % ( name, fromRelativePath ( project_dir, value.strip() ) )
					settings.setValue ( name, fromRelativePath ( project_dir, value.strip() ) ) 
			f.close ()
		else :
			# setup default settings and create default file
			settings.setValue ( 'project', project_dir )
			settings.setValue ( 'project_shaders', project_shaders )
			settings.setValue ( 'project_textures', project_textures )
			settings.setValue ( 'shader_networks', shader_networks_dir )
			settings.setValue ( 'shader_sources', shader_sources_dir )
			
			createDefaultProject ( settings )
			
		global_vars [ 'ProjectPath' ] = project_dir
	
		global_vars [ 'ProjectShaders' ] = project_shaders
		global_vars [ 'ProjectTextures' ] = project_textures
		
		global_vars [ 'ProjectNetworks' ] = shader_networks_dir
		global_vars [ 'ProjectSources' ] = shader_sources_dir
		
		global_vars [ 'ProjectSearchPath' ] = sanitizeSearchPath ( project_dir )
		global_vars [ 'ProjectSearchShaders' ] = sanitizeSearchPath ( project_shaders )
		global_vars [ 'ProjectSearchTextures' ] = sanitizeSearchPath ( project_textures )
		
		createMissingDirs ( [ project_shaders, project_textures, shader_networks_dir, shader_sources_dir ] )
			
		ret = True

	return ret
#
# main routine
#
def main () :
	# 
	app = QtModule.QApplication ( sys.argv )
	
	app_settings.setValue ( 'version', version )
	app_settings.setValue ( 'root', normPath ( root ) )
	project_filename = setDefaultValue ( 'project_filename', 'meshadered.prj' )

	temp_dir = setDefaultValue ( 'temp', normPath ( os.path.join ( root, 'tmp' ) ) )

	project_dir = setDefaultValue ( 'project', normPath ( os.path.join ( root, 'samples' ) ) )
	project_shaders = setDefaultValue ( 'project_shaders', normPath ( os.path.join ( project_dir,'shaders' ) ) )
	project_textures = setDefaultValue ( 'project_textures',normPath ( os.path.join ( project_dir,'textures' ) ) )

	shader_networks_dir = setDefaultValue ( 'shader_networks', normPath ( os.path.join ( project_shaders,'shn' ) ) )
	shader_sources_dir = setDefaultValue ( 'shader_sources', normPath ( os.path.join ( project_shaders,'src' ) ) )
	shader_output_dir = project_shaders

	lib_dir = setDefaultValue ( 'lib', normPath ( os.path.join ( root, 'lib' ) ) )
	node_dir = setDefaultValue ( 'nodes', normPath ( os.path.join ( lib_dir, 'nodes' ) ) )
	texture_dir = setDefaultValue ( 'texture', normPath ( os.path.join ( lib_dir, 'textures' ) ) )
	shaders_dir = setDefaultValue ( 'shaders', normPath ( os.path.join ( lib_dir, 'shaders' ) ) )
	archive_dir = setDefaultValue ( 'archive', normPath ( os.path.join ( lib_dir, 'archives' ) ) )

	include_dir = setDefaultValue ( 'include', normPath ( os.path.join ( root, 'include' ) ) )

	createMissingDirs ( [ temp_dir, lib_dir, project_dir, project_shaders, project_textures ] )
	createMissingDirs ( [ shader_networks_dir, shader_sources_dir ] )
	createMissingDirs ( [ node_dir, texture_dir, shaders_dir, archive_dir ] ) # include_dir supposed to be a list
	#
	# Recent projects/networks
	#
	setDefaultValue ( 'recent_projects_max', 10 )
	setDefaultValue ( 'recent_networks_max', 10 )
	#
	# setup globals
	#
	app_global_vars [ 'version' ] = getDefaultValue ( app_settings, '', 'version' )
	app_global_vars [ 'RootPath' ]        = root
	app_global_vars [ 'TempPath' ]        = temp_dir
	app_global_vars [ 'ProjectPath' ]     = project_dir
	app_global_vars [ 'ProjectShaders' ]  = project_shaders
	app_global_vars [ 'ProjectTextures' ] = project_textures

	app_global_vars [ 'ProjectNetworks' ] = shader_networks_dir
	app_global_vars [ 'ProjectSources' ]  = shader_sources_dir

	app_global_vars [ 'LibPath' ]     = lib_dir
	app_global_vars [ 'NodesPath' ]   = node_dir
	app_global_vars [ 'TexturePath' ] = texture_dir
	app_global_vars [ 'ShaderPath' ]  = shaders_dir
	app_global_vars [ 'IncludePath' ] = include_dir

	app_global_vars [ 'TextureSearchPath' ] = sanitizeSearchPath ( texture_dir )
	app_global_vars [ 'ShaderSearchPath' ]  = sanitizeSearchPath ( shaders_dir )
	app_global_vars [ 'ArchiveSearchPath' ] = sanitizeSearchPath ( archive_dir )

	app_global_vars [ 'ProjectSearchPath' ]     = sanitizeSearchPath ( project_dir )
	app_global_vars [ 'ProjectSearchShaders' ]  = sanitizeSearchPath ( project_shaders )
	app_global_vars [ 'ProjectSearchTextures' ] = sanitizeSearchPath ( project_textures )

	#
	# Setup current renderer preset
	#
	defRenderer = setDefaultValue ( 'defRenderer', '3Delight' )
	preset = meRendererPreset ( os.path.join ( root, 'renderers.xml' ), defRenderer )
	app_global_vars [ 'RendererPreset' ] = preset
	app_global_vars [ 'RendererName' ]   = preset.currentPreset.RendererName
	app_global_vars [ 'RendererFlags' ]  = preset.currentPreset.RendererFlags
	app_global_vars [ 'ShaderCompiler' ] = preset.currentPreset.ShaderCompiler
	app_global_vars [ 'ShaderDefines' ]  = preset.currentPreset.ShaderDefines
	app_global_vars [ 'ShaderInfo' ]     = preset.currentPreset.ShaderInfo
	app_global_vars [ 'SLO' ]            = preset.currentPreset.ShaderExt
	app_global_vars [ 'TextureMake' ]    = preset.currentPreset.TextureMake
	app_global_vars [ 'TextureInfo' ]    = preset.currentPreset.TextureInfo
	app_global_vars [ 'TextureViewer' ]  = preset.currentPreset.TextureViewer
	app_global_vars [ 'TEX' ]            = preset.currentPreset.TextureExt

	createDefaultProject ( app_settings, True ) # check_if_exist = True

	if DEBUG_MODE :
		print 'TextureSearchPath = %s' % app_global_vars [ 'TextureSearchPath' ]
		print 'ShaderSearchPath = %s' % app_global_vars [ 'ShaderSearchPath' ]
		print 'ArchiveSearchPath = %s' % app_global_vars [ 'ArchiveSearchPath' ]
		print 'Renderer = %s' % app_global_vars [ 'RendererName' ]

	#app_global_vars[ 'RibPath' ] = ''
	#app_global_vars[ 'DisplayPath' ] = ''
	app_settings.beginGroup ( 'WorkArea' )
	#grid_enabled = bool( setDefaultValue( 'grid_enabled', True ).toString() )
	grid_enabled   = setDefaultValue ( 'grid_enabled', True )
	grid_size      = int ( setDefaultValue ( 'grid_size', 10 ) )
	grid_snap      = setDefaultValue ( 'grid_snap', True )
	reverse_flow   = setDefaultValue ( 'reverse_flow', False )
	straight_links = setDefaultValue ( 'straight_links', True )

	app_settings.endGroup ()

	app_settings.beginGroup ( 'Colors' )
	app_colors [ 'rsl_node_bg' ] = setDefaultValue ( 'rsl_node_bg', app_colors [ 'rsl_node_bg' ] )
	app_colors [ 'rib_node_bg' ] = setDefaultValue ( 'rib_node_bg', app_colors [ 'rib_node_bg' ] )
	app_colors [ 'image_node_bg' ] = setDefaultValue ( 'image_node_bg', app_colors [ 'image_node_bg' ] )
	app_colors [ 'group_node_bg' ] = setDefaultValue ( 'group_node_bg', app_colors [ 'group_node_bg' ] )
	app_settings.endGroup ()
	
	from gui.MainWindow import MainWindow

	window = MainWindow ()
	window.show ()

	# It's exec_ because exec is a reserved word in Python
	sys.exit ( app.exec_ () )
#
# 
#
if __name__ == "__main__":
	#
	print '* meShaderEd version %s' % version

	if len( sys.argv ) > 1 :
		if sys.argv [ 1 ].lower () == '-debug' or sys.argv [ 1 ].lower () == '-d':
			print '>> Running in DEBUG mode ...'
			DEBUG_MODE = True

	if DEBUG_MODE :
		#safeEffects = QtCore.QT_VERSION >= 0x40600 and QtCore.PYQT_VERSION > 0x40704
		print '* Python %s' % sys.version
		if not usePySide :
			print '* QT_VERSION = %0X' % QtCore.QT_VERSION
			print '* PYQT_VERSION = %0X' % QtCore.PYQT_VERSION
		else :
			print '* PySide Version = %s' % QtCore.__version__

	if sys.platform.startswith ( 'win') :
		if not usePyQt5 :
			pass
			#QtModule.QApplication.setStyle ( QtModule.QStyleFactory.create ( 'Cleanlooks' ) )
			#QtModule.QApplication.setPalette ( QtModule.QApplication.style ().standardPalette () )
	
	main ()
