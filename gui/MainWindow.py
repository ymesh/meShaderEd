#===============================================================================
# MainWindow.py
#
#
#
#===============================================================================
import os, sys

from PyQt4 import QtCore, QtGui, QtXml

from global_vars import app_global_vars, DEBUG_MODE
from core.meCommon import *

from gfx.gfxNode import GfxNode
from core.nodeNetwork import *

from meRendererSetup import meRendererSetup
from ProjectSetup import ProjectSetup
from SettingsSetup import SettingsSetup
from NodeEditorPanel import NodeEditorPanel

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

    self.setWindowTitle ( 'meShaderEd %s (%s)' % ( app_global_vars [ 'version' ], app_renderer.getCurrentPresetName() ) )

    self.activeNodeList = None
    self.workArea = None # current work area
    self.onNew () # create new document

    grid_enabled = getDefaultValue ( app_settings, 'WorkArea', 'grid_enabled' )
    grid_snap = getDefaultValue ( app_settings, 'WorkArea', 'grid_snap' )
    grid_size = int( getDefaultValue ( app_settings, 'WorkArea', 'grid_size' )  )
    reverse_flow = getDefaultValue ( app_settings, 'WorkArea', 'reverse_flow' )
    straight_links = getDefaultValue ( app_settings, 'WorkArea', 'straight_links' )

    #self.ui.workArea.gridSize = grid_size
    #self.ui.workArea.gridSnap = grid_snap
    self.workArea.drawGrid = grid_enabled
    #self.ui.workArea.reverseFlow = reverse_flow
    #self.ui.workArea.straightLinks = straight_links

    self.ui.actionShowGrid.setChecked ( grid_enabled )
    self.ui.actionSnapGrid.setChecked ( grid_snap )
    self.ui.actionReverseFlow.setChecked ( reverse_flow )
    self.ui.actionStraightLinks.setChecked ( straight_links )

    self.ui.nodeList_ctl.setLibrary ( app_global_vars [ 'NodesPath' ] )
    self.ui.project_ctl.setLibrary ( app_global_vars [ 'ProjectNetworks' ] )

    QtCore.QObject.connect ( self.ui.nodeList_ctl.ui.nodeList, QtCore.SIGNAL ( 'setActiveNodeList' ), self.setActiveNodeList )
    QtCore.QObject.connect ( self.ui.project_ctl.ui.nodeList, QtCore.SIGNAL ( 'setActiveNodeList' ), self.setActiveNodeList )

    QtCore.QObject.connect ( self.ui.tabs, QtCore.SIGNAL ( 'currentChanged(int)' ), self.onTabSelected )
    QtCore.QObject.connect ( self.ui.tabs, QtCore.SIGNAL ( 'tabCloseRequested(int)' ), self.onTabCloseRequested )

    QtCore.QObject.connect ( self.ui.nodeParam_ctl, QtCore.SIGNAL ( 'nodeLabelChanged' ), self.onNodeLabelChanged  )
    QtCore.QObject.connect ( self.ui.nodeParam_ctl, QtCore.SIGNAL ( 'nodeParamChanged' ), self.onNodeParamChanged  )
    
    self.setupActions ()
    
  #
  # connectWorkAreaSignals
  #
  def connectWorkAreaSignals ( self ) :
    if self.workArea != None :
      if self.activeNodeList != None :
        QtCore.QObject.connect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'selectNodes' ), self.onSelectGfxNodes  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'nodeConnectionChanged' ), self.onNodeParamChanged  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeAdded' ), self.onAddGfxNode )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeRemoved' ), self.onRemoveGfxNode )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'editGfxNode' ), self.onEditGfxNode )
  #
  # disconnectWorkAreaSignals
  #
  def disconnectWorkAreaSignals ( self ) :
    if self.workArea != None :
      if self.activeNodeList != None :
        QtCore.QObject.disconnect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'selectNodes' ), self.onSelectGfxNodes  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'nodeConnectionChanged' ), self.onNodeParamChanged  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeAdded' ), self.onAddGfxNode )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeRemoved' ), self.onRemoveGfxNode )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'editGfxNode' ), self.onEditGfxNode )
  #
  # setupMenuBar
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
  # setupPanels
  #
  def setupPanels ( self ) :
    #
    self.tabifyDockWidget ( self.ui.dockGeom, self.ui.dockPreview )
    self.tabifyDockWidget ( self.ui.dockProject, self.ui.dockNodes )

    self.removeDockWidget ( self.ui.dockParam )
    self.addDockWidget ( QtCore.Qt.DockWidgetArea ( 2 ), self.ui.dockParam )
    self.ui.dockParam.show ()
  #
  # setupActions
  #
  def setupActions ( self ) :
    enableForNodes = False
    enableForLinks = False
    if self.workArea is not None :
      if len ( self.workArea.selectedNodes ) > 0 : enableForNodes = True
      if len ( self.workArea.selectedLinks ) > 0 : enableForLinks = True
    
    self.ui.actionDuplicate.setEnabled ( enableForNodes )
    self.ui.actionDuplicateWithLinks.setEnabled ( enableForNodes )
    self.ui.actionDelete.setEnabled ( enableForNodes or enableForLinks )
      
  #
  # onProjectSetup
  #
  def onProjectSetup ( self ):
    #
    if DEBUG_MODE : print ">> MainWindow: onProjectSetup"
    projectSetupDlg = ProjectSetup ( app_settings )
    projectSetupDlg.exec_()
    self.ui.project_ctl.setLibrary ( app_global_vars [ 'ProjectNetworks' ] )
  #
  # onSettingsSetup
  #
  def onSettingsSetup ( self ):
    #
    if DEBUG_MODE : print '>> MainWindow: onSettingsSetup'
    settingsSetupDlg = SettingsSetup ( app_settings )
    settingsSetupDlg.exec_()
    self.ui.nodeList_ctl.setLibrary ( app_global_vars [ 'NodesPath' ] )
  #
  # onRenderSettings
  #
  def onRenderSettings ( self ):
    #
    if DEBUG_MODE : print '>> MainWindow: onRenderSettings'
    renderSettingsDlg = meRendererSetup ( app_renderer )
    QtCore.QObject.connect ( renderSettingsDlg, QtCore.SIGNAL ( 'presetChanged' ), self.onRenderPresetChanged )
    QtCore.QObject.connect ( renderSettingsDlg, QtCore.SIGNAL ( 'savePreset' ), self.onRenderSavePreset )
    renderSettingsDlg.exec_ ()
  #
  # onRenderPresetChanged
  #
  def onRenderPresetChanged ( self ):
    #
    presetName = app_renderer.getCurrentPresetName()
    if DEBUG_MODE : print '>> MainWindow: onRenderPresetChanged preset = %s' % presetName
    self.setWindowTitle ( 'meShaderEd %s (%s)' % ( app_global_vars [ 'version' ], presetName ) )
    app_settings.setValue ( 'defRenderer', presetName )

    app_global_vars [ 'Renderer' ] = app_renderer.getCurrentValue ( 'renderer', 'name' )
    app_global_vars [ 'RendererFlags' ] = app_renderer.getCurrentValue ( 'renderer', 'flags' )
    app_global_vars [ 'ShaderCompiler' ] = app_renderer.getCurrentValue ( 'shader', 'compiler' )
    app_global_vars [ 'ShaderDefines' ] = app_renderer.getCurrentValue ( 'shader', 'defines' )
    app_global_vars [ 'TEX' ] = app_renderer.getCurrentValue ( 'texture', 'extension' )
    app_global_vars [ 'SLO' ] = app_renderer.getCurrentValue ( 'shader', 'extension' )
  #
  # onRenderSavePreset
  #
  def onRenderSavePreset ( self ):
    #
    if DEBUG_MODE : print '>> MainWindow: onRenderSavePreset  preset = %s' % app_renderer.getCurrentPresetName()
    app_renderer.saveSettings ()
  #
  # onShowGrid 
  #
  def onShowGrid ( self, check ):
    #
    if DEBUG_MODE : print '>> MainWindow: onShowGrid = %d' % check
    self.workArea.drawGrid = bool ( check )
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'grid_enabled', bool ( check ) )
    app_settings.endGroup ()

    self.workArea.resetCachedContent ()
    #self.ui.workArea.update()
  #
  # onSnapGrid
  #
  def onSnapGrid ( self, check ):
    #
    if DEBUG_MODE : print '>> MainWindow: onSnapGrid = %d' % check
    self.workArea.gridSnap = bool ( check )
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'grid_snap', bool ( check ) )
    app_settings.endGroup ()

    #self.ui.workArea.resetCachedContent()
  #
  # onReverseFlow
  #
  def onReverseFlow ( self, check ):
    #
    if DEBUG_MODE : print '>> MainWindow: onReverseFlow = %d' % check
    self.workArea.reverseFlow = bool ( check )
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'reverse_flow', bool ( check ) )
    app_settings.endGroup ()

    #self.ui.workArea.resetCachedContent()
  #
  # onStraightLinks
  #
  def onStraightLinks ( self, check ):
    #
    if DEBUG_MODE : print '>> MainWindow: onStraightLinks = %d' % check
    self.workArea.straightLinks = bool ( check )
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'straight_links', bool ( check ) )
    app_settings.endGroup ()
    self.workArea.resetCachedContent ()
    self.workArea.adjustLinks ()
  #
  # setActiveNodeList
  #
  def setActiveNodeList ( self, nodeList ) :
    if DEBUG_MODE : print '>> MainWindow: setActiveNodeList'
    if self.activeNodeList != None :
      QtCore.QObject.disconnect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
    self.activeNodeList = nodeList
    QtCore.QObject.connect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
  #
  # onGetNode
  #
  # Called by WorkArea after drag&drop event
  # Here we choose selected nodeList panel (Libray or Project)
  # for processing node request
  def onGetNode ( self, itemFilename, pos ) :
    #
    if self.activeNodeList != None : self.activeNodeList.onGetNode ( itemFilename, pos )
  #
  # onAddGfxNode
  #
  def onAddGfxNode ( self, gfxNode ):
    #
    #print ">> MainWindow: onAddGfxNode = %s" % gfxNode.node.label
    if gfxNode.node.type == 'image' : self.ui.imageView_ctl.addViewer ( gfxNode )

      #if self.ui.nodeParam_ctl.receivers( QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ) ) == 0 :
      #  QtCore.QObject.connect( self.ui.nodeParam_ctl, QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self.ui.imageView_ctl.onNodeParamChanged )
      #else :
      #  print ">> MainWindow: nodeParam_ctl onNodeParamChanged already connected to imageView_ctl"
  #
  # onRemoveGfxNode
  #
  def onRemoveGfxNode ( self, gfxNode ):
    #
    if DEBUG_MODE : print '>> MainWindow: onRemoveGfxNode = %s' % gfxNode.node.label
    if gfxNode.node.type == 'image' :
      self.ui.imageView_ctl.removeViewer ( gfxNode )
      #QtCore.QObject.disconnect ( self.ui.nodeParam_ctl, QtCore.SIGNAL ( 'onNodeParamChanged(QObject,QObject)' ), self.ui.imageView_ctl.onNodeParamChanged )
  #
  # onEditGfxNode
  #
  def onEditGfxNode ( self, gfxNode ):
    if DEBUG_MODE : print ">> MainWindow: onEditGfxNode"
    #import copy

    # reindex input params
    for i in range ( 0, len( gfxNode.node.inputParams ) ) : gfxNode.node.inputParams[ i ].id = i

    # reindex output params
    for i in range ( 0, len( gfxNode.node.outputParams ) ) : gfxNode.node.outputParams[ i ].id = i

    save_inputParams = gfxNode.node.inputParams
    save_outputParams = gfxNode.node.outputParams
    save_inputLinks = gfxNode.node.inputLinks
    save_outputLinks = gfxNode.node.outputLinks

    editNode = gfxNode.node.copy()

    #dom = QtXml.QDomDocument ( gfxNode.node.name )
    #xml_node = gfxNode.node.parseToXML ( dom )
    #createNodeFromXML ( xml_node )

    nodeEditDlg = NodeEditorPanel ( editNode )
    if ( nodeEditDlg.exec_() == QtGui.QDialog.Accepted ) :
      if DEBUG_MODE : print '>> MainWindow: onEditGfxNode Accepted'
      # 
      #
      return
      
      if gfxNode.node.label != editNode.label : self.ui.imageView_ctl.onNodeLabelChanged ( gfxNode, editNode.label )
      editNode.copySetup ( gfxNode.node )

      for i in save_inputParams: print i.label

      gfxNode.updateNode ()
      #self.ui.nodeParam_ctl.setNode ( gfxNode )
      #gfxNode.update ()
      #gfxNode.adjustLinks ()
      self.ui.nodeParam_ctl.updateGui ()
      self.workArea.resetCachedContent ()
      #self.workArea.adjustLinks ()
      self.workArea.scene().update()
  #
  # onDelete
  #
  def onDelete ( self ):
    #
    if DEBUG_MODE : print '>> MainWindow: onDelete'

    selected = self.workArea.scene ().selectedItems ()
    if len ( selected ) : 
      self.workArea.removeSelected ()
    else :
      self.ui.imageView_ctl.removeAllViewers ()
      self.workArea.clear()
  #
  # onDuplicateNode
  #
  def onDuplicateNode ( self, preserveLinks = False ):
    if DEBUG_MODE : print '>> MainWindow: onDuplicateNode ( preserveLinks = %s )'  % str ( preserveLinks )
    
    for gfxNode in self.workArea.selectedNodes :
      newNode = gfxNode.node.copy ()
      
      
  #
  # onDuplicate
  #
  def onDuplicate ( self ):
    if DEBUG_MODE : print '>> MainWindow: onDuplicate '
    self.onDuplicateNode ( False )  
  #
  # onDuplicateWithLinks
  #
  def onDuplicateWithLinks ( self ):
    if DEBUG_MODE : print '>> MainWindow: onDuplicateWithLinks' 
    self.onDuplicateNode ( True ) 
  #
  # onSelectGfxNodes
  #
  def onSelectGfxNodes ( self, gfxNodes = [], gfxLinks = [] ):
    #
    #print ">> MainWindow: onSelectGfxNodes"
    self.setupActions ()
    self.workArea.inspectedNode = None
    if len ( gfxNodes ) == 1 : self.workArea.inspectedNode = gfxNodes[ 0 ]

    self.ui.nodeParam_ctl.setNode ( self.workArea.inspectedNode )
  #
  # onNodeLabelChanged
  #
  def onNodeLabelChanged ( self, gfxNode, newLabel ) :
    #
    self.workArea.nodeNet.renameNodeLabel ( gfxNode.node, newLabel )
    gfxNode.updateNodeLabel ()
    self.ui.imageView_ctl.onNodeLabelChanged ( gfxNode, newLabel )
    self.workArea.scene ().update ()
  #
  # onNodeParamChanged
  #
  def onNodeParamChanged ( self, node, param ) :
    if DEBUG_MODE : print ">> MainWindow: onNodeParamChanged"
    #param.shaderParam = not gfxNode.node.isInputParamLinked ( param )

    # from WorkArea we have GfxNode in signal nodeConnectionChanged
    # hence need to update nodeParam_ctl
    if isinstance ( node, GfxNode ) :
      if DEBUG_MODE : print "* update nodeView"
      node.updateInputParams ()
      self.ui.nodeParam_ctl.updateGui ()

    if self.ui.imageView_ctl.autoUpdate () :
      if DEBUG_MODE : print "* auto update"
      self.ui.imageView_ctl.updateViewer()
  #
  # onFitAll
  #
  def onFitAll ( self ) :
    if DEBUG_MODE : print ">> MainWindow: onFitAll"
  #
  # onFitSelected
  #
  def onFitSelected ( self ) :
    if DEBUG_MODE : print ">> MainWindow: onFitSelected"
  #
  # onZoomReset
  #
  def onZoomReset ( self ) : self.workArea.resetZoom ()
  #
  # onNewParamView
  #
  def onNewParamView ( self ) :
    if DEBUG_MODE : print ">> MainWindow: onNewParamView"
  #
  # onTabSelected
  #
  def onTabSelected ( self, idx ) :
    #
    if DEBUG_MODE : print '>> MainWindow: onTabSelected (%d)' % idx
    self.disconnectWorkAreaSignals ()
    self.ui.imageView_ctl.removeAllViewers ()
    self.workArea = self.ui.tabs.currentWidget ()

    imageNodes = self.workArea.getGfxNodesByType ( 'image' )
    # setup imageView menu for image nodes in new tab
    for gfxNode in imageNodes : self.ui.imageView_ctl.addViewer ( gfxNode )

    self.connectWorkAreaSignals ()
    self.ui.nodeParam_ctl.setNode ( self.workArea.inspectedNode )
    self.workArea.adjustLinks ()
  #
  # onTabCloseRequested
  #
  def onTabCloseRequested ( self, idx ) :
    #
    if DEBUG_MODE : print '>> MainWindow: onTabCloseRequested (%d)' % idx
    if self.ui.tabs.count() > 1 :
      self.workArea.nodeNet.clear ()
      self.ui.tabs.removeTab ( idx )
  #
  # onNew
  #
  def onNew ( self, tabName = 'untitled' ):
    #
    def tabNameExists ( self, name ):
      ret = False
      for i in range ( 0, self.ui.tabs.count () ) :
        if name == str ( self.ui.tabs.tabText ( i ) ):
          ret = True
          break
      return ret

    newName = tabName
    if DEBUG_MODE : print '->  self.ui.tabs.count() = %d ' % self.ui.tabs.count ()

    if self.workArea != None :
      if DEBUG_MODE : print '->  create new WorkArea widget'
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
      if DEBUG_MODE : print '->  use initial WorkArea widget'
      workArea = self.ui.workArea # use initial WorkArea widget
      self.workArea = workArea
      self.connectWorkAreaSignals ()

    nodeNet = NodeNetwork ( newName )
    workArea.setNodeNetwork ( nodeNet )

    self.ui.tabs.setTabText ( self.ui.tabs.indexOf( workArea ), newName )
    self.ui.tabs.setCurrentIndex ( self.ui.tabs.indexOf ( workArea ) )
  #
  # onOpen
  #
  def onOpen ( self ):
    if DEBUG_MODE : print ">> MainWindow: onOpen"
    #
    curDir = app_global_vars [ 'ProjectNetworks' ]
    typeFilter = 'Shader networks *.xml;;All files *.*;;'

    filename = str( QtGui.QFileDialog.getOpenFileName ( self, "Open file", curDir, typeFilter ) )
    if filename != '' :
      if DEBUG_MODE : print "-> open file %s" %  filename
      ( name, ext ) = os.path.splitext( os.path.basename ( filename ) )

      self.ui.imageView_ctl.removeAllViewers ()

      self.workArea.clear ()
      self.workArea.nodeNet.name = name
      self.workArea.nodeNet.fileName = ''
      self.ui.tabs.setTabText ( self.ui.tabs.indexOf ( self.workArea ), name )

      self.workArea.openNodeNet ( normPath ( filename ) )
  #
  # onImport
  #
  def onImport ( self ):
    if DEBUG_MODE : print ">> MainWindow: onImport"
    #
    curDir = app_global_vars [ 'ProjectNetworks' ]
    typeFilter = 'Shader networks *.xml;;All files *.*;;'

    filename = str ( QtGui.QFileDialog.getOpenFileName ( self, "Import file", curDir, typeFilter ) )
    if filename != '' :
      if DEBUG_MODE : print "-> import file %s" %  filename
      self.workArea.insertNodeNet ( normPath ( filename ) )
  #
  # onSave
  #
  def onSave ( self ):
    if DEBUG_MODE : print ">> MainWindow: onSave"
    # if file is new -- use onSaveAs function
    #
    curDir = app_global_vars [ 'ProjectNetworks' ]
    if self.workArea.nodeNet.fileName == '' :
      self.onSaveAs ()
    else :
      if DEBUG_MODE : print '-> save file %s' % self.workArea.nodeNet.fileName
      self.workArea.nodeNet.save ()
  #
  # onSaveAs
  #
  def onSaveAs ( self ):
    if DEBUG_MODE : print ">> MainWindow: onSaveAs"
    #
    curDir = app_global_vars [ 'ProjectNetworks' ]
    saveName = os.path.join ( curDir, self.workArea.nodeNet.name + '.xml' )
    typeFilter = 'Shader networks *.xml;;All files *.*;;'

    filename = str( QtGui.QFileDialog.getSaveFileName ( self, "Save file as", saveName, typeFilter ) )
    if filename != '' :
      if DEBUG_MODE : print '-> save file As %s' % filename
      ( name, ext ) = os.path.splitext ( os.path.basename ( filename ) )
      self.workArea.nodeNet.fileName = normPath ( filename )
      self.workArea.nodeNet.name = name
      self.ui.tabs.setTabText ( self.ui.tabs.indexOf ( self.workArea ), name )

      self.workArea.nodeNet.save ()
      self.ui.project_ctl.onReload ()

