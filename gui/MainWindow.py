#===============================================================================
# MainWindow.py
#
# 
#
#===============================================================================
import os, sys

from PyQt4 import QtCore, QtGui

from global_vars import app_global_vars
from core.meCommon import *

from core.nodeNetwork import NodeNetwork

from meRendererSetup import meRendererSetup
from ProjectSetup import ProjectSetup
from SettingsSetup import SettingsSetup

from nodeList import NodeList

from gfx.WorkArea import WorkArea

from meShaderEd import app_settings
from meShaderEd import app_renderer
from meShaderEd import getDefaultValue 

from ui_MainWindow import Ui_MainWindow
#
# Create a class for our main window
#
class MainWindow ( QtGui.QMainWindow ):
  #
  #
  def __init__ ( self ) : 
    #
    QtGui.QMainWindow.__init__ ( self )
    
    # This is always the same
    self.ui = Ui_MainWindow ()
    self.ui.setupUi ( self )
    self.setupMenuBar ()
    self.setupPanels ()
    
    self.setWindowTitle ( "meShaderEd (" + app_renderer.getCurrentPresetName() + ")")
    
    self.activeNodeList = None
    self.workArea = None # current work area
    self.onNew () # create new document 
    
    grid_enabled = getDefaultValue( app_settings, 'WorkArea', 'grid_enabled' )
    grid_snap = getDefaultValue ( app_settings, 'WorkArea', 'grid_snap' )
    grid_size = int( getDefaultValue ( app_settings, 'WorkArea', 'grid_size' )  )
    reverse_flow = getDefaultValue ( app_settings, 'WorkArea', 'reverse_flow' )
    straight_links = getDefaultValue ( app_settings, 'WorkArea', 'straight_links' )
  
    #self.ui.workArea.gridSize = grid_size
    #self.ui.workArea.gridSnap = grid_snap
    self.workArea.drawGrid = grid_enabled
    #self.ui.workArea.reverseFlow = reverse_flow 
    #self.ui.workArea.straightLinks = straight_links
    
    self.ui.actionShowGrid.setChecked( grid_enabled )
    self.ui.actionSnapGrid.setChecked( grid_snap )
    self.ui.actionReverseFlow.setChecked( reverse_flow )
    self.ui.actionStraightLinks.setChecked( straight_links )
   
    self.ui.nodeList_ctl.setLibrary ( app_global_vars[ 'NodesPath' ] )
    self.ui.project_ctl.setLibrary ( app_global_vars[ 'ProjectNetworks' ] )
    
    QtCore.QObject.connect ( self.ui.nodeList_ctl.ui.nodeList, QtCore.SIGNAL( "setActiveNodeList" ), self.setActiveNodeList )
    QtCore.QObject.connect ( self.ui.project_ctl.ui.nodeList, QtCore.SIGNAL( "setActiveNodeList" ), self.setActiveNodeList )
    
    QtCore.QObject.connect ( self.ui.tabs, QtCore.SIGNAL( "currentChanged(int)" ), self.onTabSelected )
    QtCore.QObject.connect ( self.ui.tabs, QtCore.SIGNAL( "tabCloseRequested(int)" ), self.onTabCloseRequested )
    
    QtCore.QObject.connect ( self.ui.nodeParam_ctl, QtCore.SIGNAL( "nodeLabelChanged" ), self.onNodeLabelChanged  )
  #
  #
  def connectWorkAreaSignals ( self ) :
    if self.workArea != None :
      if self.activeNodeList != None :
        QtCore.QObject.connect ( self.activeNodeList, QtCore.SIGNAL( "addNode" ), self.workArea.insertNodeNet  ) 
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL( "selectNodes" ), self.onSelectGfxNodes  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL( "nodeParamChanged" ), self.onNodeParamChanged  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL( "gfxNodeAdded" ), self.onAddGfxNode )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL( "gfxNodeRemoved" ), self.onRemoveGfxNode )
  #
  #
  def disconnectWorkAreaSignals ( self ) :
    if self.workArea != None : 
      if self.activeNodeList != None :
        QtCore.QObject.disconnect ( self.activeNodeList, QtCore.SIGNAL( "addNode" ), self.workArea.insertNodeNet  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL( "selectNodes" ), self.onSelectGfxNodes  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL( "nodeParamChanged" ), self.onNodeParamChanged  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL( "gfxNodeAdded" ), self.onAddGfxNode )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL( "gfxNodeRemoved" ), self.onRemoveGfxNode )  
  #
  #
  def setupMenuBar ( self ) :
    # override font for menu from Designer's settings to system default
    font = QtGui.QFont ()
    if ( sys.platform == 'win32' ):
      # Runing on windows, override font sizes from Designer to default 
      font.setPointSize ( 8 )   
    elif ( sys.platform == 'darwin' ):
      font.setPointSize ( 10 )
    
    self.ui.menubar.setFont ( font )
    self.ui.menuFile.setFont ( font )
    self.ui.menuEdit.setFont ( font )
    self.ui.menuCommand.setFont ( font )
    self.ui.menuWindow.setFont ( font )
    self.ui.menuHelp.setFont ( font )
  #
  #
  def setupPanels ( self ) :
        
    self.tabifyDockWidget ( self.ui.dockGeom, self.ui.dockPreview ) 
    self.tabifyDockWidget ( self.ui.dockProject, self.ui.dockNodes ) 
    
    self.removeDockWidget ( self.ui.dockParam )
    self.addDockWidget ( QtCore.Qt.DockWidgetArea(2), self.ui.dockParam )
    self.ui.dockParam.show ()
    
  #
  #
  def onProjectSetup ( self ):

    print ">> MainWindow: onProjectSetup" 
    projectSetupDlg = ProjectSetup ( app_settings )
    projectSetupDlg.exec_()
    self.ui.project_ctl.setLibrary ( app_global_vars[ 'ProjectNetworks' ] )
  #
  #
  def onSettingsSetup ( self ):

    print ">> MainWindow: onSettingsSetup" 
    settingsSetupDlg = SettingsSetup ( app_settings )
    settingsSetupDlg.exec_()
    self.ui.nodeList_ctl.setLibrary ( app_global_vars[ 'NodesPath' ] )
  #
  #
  def onRenderSettings ( self ):

    print ">> MainWindow: onRenderSettings" 
    renderSettingsDlg = meRendererSetup ( app_renderer )
    QtCore.QObject.connect( renderSettingsDlg, QtCore.SIGNAL("presetChanged"), self.onRenderPresetChanged )
    QtCore.QObject.connect( renderSettingsDlg, QtCore.SIGNAL("savePreset"), self.onRenderSavePreset )
    renderSettingsDlg.exec_()
  #
  #
  def onRenderPresetChanged ( self ):
    #
    presetName = app_renderer.getCurrentPresetName()
    print ">> MainWindow: onRenderPresetChanged preset = %s" % presetName 
    self.setWindowTitle ( "meShaderEd (" + presetName + ")")
    app_settings.setValue ( 'defRenderer', presetName )
    
    app_global_vars[ 'Renderer' ] = app_renderer.getCurrentValue( 'renderer', 'name' )
    app_global_vars[ 'RendererFlags' ] = app_renderer.getCurrentValue( 'renderer', 'flags' ) 
    app_global_vars[ 'ShaderCompiler' ] = app_renderer.getCurrentValue( 'shader', 'compiler' ) 
    app_global_vars[ 'ShaderDefines' ] = app_renderer.getCurrentValue( 'shader', 'defines' ) 
    app_global_vars[ 'TEX' ] = app_renderer.getCurrentValue( 'texture', 'extension' )
    app_global_vars[ 'SLO' ] = app_renderer.getCurrentValue( 'shader', 'extension' )
  #
  #
  def onRenderSavePreset ( self ):
    #
    print ">> MainWindow: onRenderSavePreset  preset = %s" % app_renderer.getCurrentPresetName()
    app_renderer.saveSettings ()
  #
  #
  def onShowGrid ( self, check ):
    #
    print ">> MainWindow: onShowGrid = %d" % check
    self.workArea.drawGrid = bool( check ) 
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'grid_enabled', bool( check ) )
    app_settings.endGroup ()
      
    self.workArea.resetCachedContent()
    #self.ui.workArea.update()
  #
  #
  def onSnapGrid ( self, check ):
    #
    print ">> MainWindow: onSnapGrid = %d" % check
    self.workArea.gridSnap = bool( check ) 
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'grid_snap', bool( check ) )
    app_settings.endGroup ()
      
    #self.ui.workArea.resetCachedContent()
  #
  #
  def onReverseFlow ( self, check ):
    #
    print ">> MainWindow: onReverseFlow = %d" % check   
    self.workArea.reverseFlow = bool( check ) 
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'reverse_flow', bool( check ) )
    app_settings.endGroup ()
      
    #self.ui.workArea.resetCachedContent()
  #
  #
  def onStraightLinks ( self, check ):
    #
    print ">> MainWindow: onStraightLinks = %d" % check 
    self.workArea.straightLinks = bool( check ) 
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'straight_links', bool( check ) )
    app_settings.endGroup ()
    self.workArea.resetCachedContent () 
  #
  #
  def setActiveNodeList ( self, nodeList ) :
    print '>> MainWindow: setActiveNodeList'
    if self.activeNodeList != None :
      QtCore.QObject.disconnect ( self.activeNodeList, QtCore.SIGNAL( "addNode" ), self.workArea.insertNodeNet  )  
    self.activeNodeList = nodeList  
    QtCore.QObject.connect ( self.activeNodeList, QtCore.SIGNAL( "addNode" ), self.workArea.insertNodeNet  )
  #
  # Called by WorkArea after drag&drop event
  # Here we choose selected nodeList panel (Libray or Project)
  # for processing node request
  def onGetNode ( self, itemFilename, pos ):
    if self.activeNodeList != None :
      self.activeNodeList.onGetNode ( itemFilename, pos ) 
  #
  #
  def onAddGfxNode ( self, gfxNode ):
    #
    #print ">> MainWindow: onAddGfxNode = %s" % gfxNode.node.label
    if gfxNode.node.type == 'image' :
      
      self.ui.imageView_ctl.addViewer ( gfxNode )
      
      #if self.ui.nodeParam_ctl.receivers( QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ) ) == 0 :
      #  QtCore.QObject.connect( self.ui.nodeParam_ctl, QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self.ui.imageView_ctl.onNodeParamChanged ) 
      #else :
      #  print ">> MainWindow: nodeParam_ctl onNodeParamChanged already connected to imageView_ctl" 
  #
  #
  def onRemoveGfxNode ( self, gfxNode ):
    #
    print ">> MainWindow: onRemoveGfxNode = %s" % gfxNode.node.label
    if gfxNode.node.type == 'image' :
      self.ui.imageView_ctl.removeViewer ( gfxNode )
      #QtCore.QObject.disconnect ( self.ui.nodeParam_ctl, QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self.ui.imageView_ctl.onNodeParamChanged ) 
  #
  #
  def onDelete ( self ):
    #
    print ">> MainWindow: onDelete"
    
    selected = self.workArea.scene().selectedItems()
    if len ( selected ) :
      self.workArea.removeSelected()
    else :
      self.ui.imageView_ctl.removeAllViewers ()
      self.workArea.clear()  
      
  #
  #
  def onSelectGfxNodes ( self, gfxNodes = [], gfxLinks = [] ):
    #
    #print ">> MainWindow: onSelectGfxNodes"
    self.workArea.inspectedNode = None  
    if len( gfxNodes ) == 1 :
      self.workArea.inspectedNode = gfxNodes[ 0 ]
      
    self.ui.nodeParam_ctl.setNode ( self.workArea.inspectedNode )
  #
  #
  def onNodeLabelChanged ( self, gfxNode, newLabel ) :

    self.workArea.nodeNet.renameNodeLabel ( gfxNode.node, newLabel )
    gfxNode.updateNodeLabel()
    self.ui.imageView_ctl.onNodeLabelChanged ( gfxNode, newLabel )
    self.workArea.scene().update()
  #
  #
  def onNodeParamChanged ( self, gfxNode, param ) :
    #param.shaderParam = not gfxNode.node.isInputParamLinked ( param )
    gfxNode.updateInputParams ()
    self.ui.nodeParam_ctl.updateGui ()
  #
  #
  def onFitAll ( self ) :    
    print ">> MainWindow: onFitAll"
  #
  #
  def onFitSelected ( self ) :    
    print ">> MainWindow: onFitSelected"
  #
  #
  def onZoomReset ( self ) :    
    print ">> MainWindow: onZoomReset"
  #
  #
  def onNewParamView ( self ) :    
    print ">> MainWindow: onNewParamView"
  #
  #
  def onTabSelected ( self, idx ) :
    #
    print '>> MainWindow: onTabSelected (%d)' % idx 
    self.disconnectWorkAreaSignals () 
    
    self.ui.imageView_ctl.removeAllViewers ()
        
    self.workArea = self.ui.tabs.currentWidget ()
    
    imageNodes = self.workArea.getGfxNodesByType ( 'image' )
    # setup imageView menu for image nodes in new tab 
    for gfxNode in imageNodes :
      self.ui.imageView_ctl.addViewer ( gfxNode )
    
    self.connectWorkAreaSignals ()
    self.ui.nodeParam_ctl.setNode ( self.workArea.inspectedNode )
  #
  #
  def onTabCloseRequested ( self, idx ) :
    #
    print '>> MainWindow: onTabCloseRequested (%d)' % idx 
    if self.ui.tabs.count() > 1 :
      self.workArea.nodeNet.clear()
      self.ui.tabs.removeTab ( idx )
  #
  #
  def onNew ( self, tabName = 'untitled' ):
    #
    def tabNameExists ( self, name ):
      ret = False
      for i in range ( 0, self.ui.tabs.count() ) :
        if name == str ( self.ui.tabs.tabText ( i ) ):
          ret = True
          break
      return ret 
    
    newName = tabName
    print '->  self.ui.tabs.count() = %d ' % self.ui.tabs.count()
    
    if self.workArea != None :
      print '->  create new WorkArea widget'
      # set unique new name
      name = newName
      i = 0
      while True :
        if tabNameExists ( self, name ) :
          name = newName + str ( i )
          i += 1
          continue
        else :
          break
      newName = name
      workArea = WorkArea ()  # create new WorkArea instance
      newTab = self.ui.tabs.addTab ( workArea, newName )
    else :
      print '->  use initial WorkArea widget'
      workArea = self.ui.workArea # use initial WorkArea widget
      self.workArea = workArea
      self.connectWorkAreaSignals () 
    
    nodeNet = NodeNetwork ( newName )
    workArea.setNodeNetwork ( nodeNet )
    
    self.ui.tabs.setTabText ( self.ui.tabs.indexOf( workArea ), newName )
    self.ui.tabs.setCurrentIndex ( self.ui.tabs.indexOf( workArea ) ) 
  #
  #
  def onOpen ( self ):
    print ">> MainWindow: onOpen"
    #
    curDir = app_global_vars[ 'ProjectNetworks' ]
    typeFilter = 'Shader networks *.xml;;All files *.*;;'
    
    filename = str( QtGui.QFileDialog.getOpenFileName( self, "Open file", curDir, typeFilter ) )
    if filename != '' : 
      print "-> open file %s" %  filename 
      ( name, ext ) = os.path.splitext( os.path.basename( filename ) )
      
      self.ui.imageView_ctl.removeAllViewers ()

      self.workArea.clear ()
      self.workArea.nodeNet.name = name
      self.workArea.nodeNet.fileName = ''
      self.ui.tabs.setTabText ( self.ui.tabs.indexOf( self.workArea ), name )
      
      self.workArea.openNodeNet ( normPath ( filename ) ) 
  #
  #
  def onImport ( self ):
    print ">> MainWindow: onImport"  
    # 
    curDir = app_global_vars[ 'ProjectNetworks' ]
    typeFilter = 'Shader networks *.xml;;All files *.*;;'
    
    filename = str( QtGui.QFileDialog.getOpenFileName( self, "Import file", curDir, typeFilter ) )
    if filename != '' : 
      print "-> import file %s" %  filename 
      self.workArea.insertNodeNet ( normPath ( filename ) ) 
  #
  #
  def onSave ( self ):
    print ">> MainWindow: onSave"
    # if file is new -- use onSaveAs function
    #
    curDir = app_global_vars[ 'ProjectNetworks' ]
    if self.workArea.nodeNet.fileName == '' :
      self.onSaveAs () 
    else :
      print '-> save file %s' % self.workArea.nodeNet.fileName 
      self.workArea.nodeNet.save ()
  #
  #
  def onSaveAs ( self ):
    print ">> MainWindow: onSaveAs"
    #
    curDir = app_global_vars[ 'ProjectNetworks' ]
    saveName = os.path.join ( curDir, self.workArea.nodeNet.name + '.xml' )
    typeFilter = 'Shader networks *.xml;;All files *.*;;'

    filename = str( QtGui.QFileDialog.getSaveFileName ( self, "Save file as", saveName, typeFilter ) )
    if filename != '' :
      print '-> save file As %s' % filename
      ( name, ext ) = os.path.splitext( os.path.basename( filename ) )
      self.workArea.nodeNet.fileName = normPath ( filename )
      self.workArea.nodeNet.name = name
      self.ui.tabs.setTabText ( self.ui.tabs.indexOf( self.workArea ), name )
      
      self.workArea.nodeNet.save ()
  