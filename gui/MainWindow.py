"""

  MainWindow.py

"""
import os, sys

from PyQt4 import QtCore, QtGui, QtXml 
#from PyQt4.QtGui import QWhatsThis 
from global_vars import app_global_vars, DEBUG_MODE, VALID_RIB_NODE_TYPES, VALID_RSL_NODE_TYPES, VALID_RSL_SHADER_TYPES
from core.meCommon import *
from core.nodeNetwork import *

from gfx.gfxNode import GfxNode
from gfx.gfxNote import GfxNote
from gfx.gfxSwatchNode import GfxSwatchNode

from meRendererSetup import meRendererSetup
from ProjectSetup import ProjectSetup
from SettingsSetup import SettingsSetup
from nodeEditor.NodeEditorDialog import NodeEditorDialog
from exportShader.ExportShaderDialog import ExportShaderDialog
from ViewComputedCodeDialog import ViewComputedCodeDialog

from nodeList import NodeList

from gfx.WorkArea import WorkArea

from meShaderEd import app_settings
#from meShaderEd import app_renderer
from meShaderEd import getDefaultValue

from ui_MainWindow import Ui_MainWindow
#
# Create a class for our main window
#
class MainWindow ( QtGui.QMainWindow ) :
  #
  # __init__
  #
  def __init__ ( self ) :
    #
    QtGui.QMainWindow.__init__ ( self )

    self.ui = Ui_MainWindow ()
    self.ui.setupUi ( self )
    #
    # setup WhatsThis help action
    #
    self.ui.actionHelpMode = QtGui.QWhatsThis.createAction ( )
    self.ui.actionHelpMode.setToolTip ( 'Enter "WhatsThis" help mode' )
    self.ui.menuHelp.addAction ( self.ui.actionHelpMode )
    self.ui.toolBar.addSeparator()
    self.ui.toolBar.addAction ( self.ui.actionHelpMode )
    QtCore.QObject.connect ( self.ui.actionHelpMode, QtCore.SIGNAL ( 'toggled(bool)' ), self.onHelpMode )
    
    self.clipboard = QtGui.QApplication.clipboard ()

    self.recentProjects = app_settings.value ( 'RecentProjects' ).toStringList ()
    self.recentNetworks = app_settings.value ( 'RecentNetworks' ).toStringList ()

    self.addRecentProject ( app_global_vars [ 'ProjectPath' ] )

    self.setupMenuBar ()
    self.setupPanels ()

    self.activeNodeList = None
    self.workArea = None # current work area
    self.onNew () # create new document

    grid_enabled = getDefaultValue ( app_settings, 'WorkArea', 'grid_enabled' )
    grid_snap = getDefaultValue ( app_settings, 'WorkArea', 'grid_snap' )
    grid_size = int ( getDefaultValue ( app_settings, 'WorkArea', 'grid_size' )  )
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

    #self.ui.dockNodes.setWindowTitle ( 'Library: %s' % app_global_vars [ 'NodesPath' ] )
    #self.ui.dockProject.setWindowTitle ( 'Project: %s' % app_global_vars [ 'ProjectNetworks' ] )

    QtCore.QObject.connect ( self.ui.nodeList_ctl.ui.nodeList, QtCore.SIGNAL ( 'setActiveNodeList' ), self.setActiveNodeList )
    QtCore.QObject.connect ( self.ui.project_ctl.ui.nodeList, QtCore.SIGNAL ( 'setActiveNodeList' ), self.setActiveNodeList )

    QtCore.QObject.connect ( self.ui.tabs, QtCore.SIGNAL ( 'currentChanged(int)' ), self.onTabSelected )
    QtCore.QObject.connect ( self.ui.tabs, QtCore.SIGNAL ( 'tabCloseRequested(int)' ), self.onTabCloseRequested )

    QtCore.QObject.connect ( self.ui.nodeParam_ctl, QtCore.SIGNAL ( 'nodeLabelChanged' ), self.onNodeLabelChanged  )
    QtCore.QObject.connect ( self.ui.nodeParam_ctl, QtCore.SIGNAL ( 'nodeParamChanged' ), self.onNodeParamChanged  )

    self.setupActions ()
    self.setupWindowTitle ()
  #
  # connectWorkAreaSignals
  #
  def connectWorkAreaSignals ( self ) :
    #
    if self.workArea != None :
      if self.activeNodeList != None :
        QtCore.QObject.connect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'selectNodes' ), self.onSelectGfxNodes  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'nodeConnectionChanged' ), self.onGfxNodeParamChanged  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeAdded' ), self.onAddGfxNode )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeRemoved' ), self.onRemoveGfxNode )
      #QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'editGfxNode' ), self.editGfxNode )
      QtCore.QObject.connect ( self.workArea.scene(), QtCore.SIGNAL ( 'nodeUpdated' ), self.updateNodeParamView )
      QtCore.QObject.connect ( self.workArea.scene(), QtCore.SIGNAL ( 'gfxNodeParamChanged' ), self.onGfxNodeParamChanged  )
  #
  # disconnectWorkAreaSignals
  #
  def disconnectWorkAreaSignals ( self ) :
    #
    if self.workArea != None :
      if self.activeNodeList != None :
        QtCore.QObject.disconnect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'selectNodes' ), self.onSelectGfxNodes  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'nodeConnectionChanged' ), self.onGfxNodeParamChanged  )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeAdded' ), self.onAddGfxNode )
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeRemoved' ), self.onRemoveGfxNode )
      #QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'editGfxNode' ), self.editGfxNode )
      QtCore.QObject.disconnect ( self.workArea.scene(), QtCore.SIGNAL ( 'nodeUpdated' ), self.updateNodeParamView )
      QtCore.QObject.disconnect ( self.workArea.scene(), QtCore.SIGNAL ( 'gfxNodeParamChanged' ), self.onGfxNodeParamChanged  )
  #
  # setupWindowTitle
  #
  def setupWindowTitle ( self ) :
    #
    self.setWindowTitle ( 'meShaderEd %s (%s) %s' % ( app_global_vars [ 'version' ], app_global_vars [ 'RendererPreset' ].getCurrentPresetName (), app_global_vars [ 'ProjectPath' ]  ) )
    self.ui.dockNodes.setToolTip ( app_global_vars [ 'NodesPath' ] )
    self.ui.dockNodes.setStatusTip ( app_global_vars [ 'NodesPath' ] )
    self.ui.dockProject.setToolTip ( app_global_vars [ 'ProjectNetworks' ] )
    self.ui.dockProject.setStatusTip ( app_global_vars [ 'ProjectNetworks' ] )
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

    self.buildRecentProjectsMenu ()
    self.buildRecentNetworksMenu ()
  #
  # buildRecentProjectsMenu
  #
  def buildRecentProjectsMenu ( self ) :
    #self.recentProjects = app_settings.value ( 'RecentProjects' ).toStringList ()
    #self.recentNetworks = app_settings.value ( 'RecentNetworks' ).toStringList ()
    self.ui.menuRecent_Projects.clear ()

    if len ( self.recentProjects ) :
      icon =  QtGui.QIcon.fromTheme ( 'folder', QtGui.QIcon ( ':/file_icons/resources/open.png' ) )
      # QtGui.QIcon ( ':/file_icons/resources/recentFile.png' ) 'folder'
      for i, fname in enumerate ( self.recentProjects ) :
        # QtCore.QFileInfo ( fname ).fileName ()
        action = QtGui.QAction ( icon, '&%d %s' % ( i + 1, fname ), self )
        action.setData ( QtCore.QVariant ( fname ) )
        self.connect ( action, QtCore.SIGNAL ( 'triggered()' ), self.onOpenRecentProject )
        self.ui.menuRecent_Projects.addAction ( action )
  #
  # buildRecentNetworksMenu
  #
  def buildRecentNetworksMenu ( self ) :
    #
    self.ui.menuRecent_Networks.clear ()

    if len ( self.recentNetworks ) :
      for i, fname in enumerate ( self.recentNetworks ) :
        icon =  QtGui.QIcon.fromTheme ( 'document-new', QtGui.QIcon ( ':/file_icons/resources/new.png' ) )
        # QtCore.QFileInfo ( fname ).fileName ()
        action = QtGui.QAction ( icon, '&%d %s' % ( i + 1, fname ), self )
        action.setData ( QtCore.QVariant ( fname ) )
        self.connect ( action, QtCore.SIGNAL ( 'triggered()' ), self.onOpenRecentNetwork )
        self.ui.menuRecent_Networks.addAction ( action )
  #
  # setupPanels
  #
  def setupPanels ( self ) :
    #
    self.tabifyDockWidget ( self.ui.dockNodes, self.ui.dockProject )

    self.tabifyDockWidget ( self.ui.dockPreview, self.ui.dockGeom  )
    self.tabifyDockWidget ( self.ui.dockParam, self.ui.dockSwatch )

    # temporary hide unused panels
    #self.removeDockWidget ( self.ui.dockGeom )
    #self.removeDockWidget ( self.ui.dockSwatch )
    self.ui.dockGeom.hide ()
    self.ui.dockSwatch.hide ()

    self.ui.dockNodes.raise_ ()
    self.ui.dockPreview.raise_ ()
    self.ui.dockParam.raise_ ()

    #self.addDockWidget ( QtCore.Qt.DockWidgetArea ( 2 ), self.ui.dockParam )
    #self.ui.dockParam.show ()
  #
  # addRecentProject
  #
  def addRecentProject ( self, project ) :
    #
    if project is not None :
      recent_projects_max = getDefaultValue ( app_settings, '', 'recent_projects_max' )

      if not self.recentProjects.contains ( project ) :
        self.recentProjects.prepend ( QtCore.QString ( project ) )

      while self.recentProjects.count () > recent_projects_max :
        self.recentProjects.takeLast ()

      recentProjects = QtCore.QVariant ( self.recentProjects ) if self.recentProjects else QtCore.QVariant ()
      app_settings.setValue ( 'RecentProjects', recentProjects )
  #
  # addRecentNetwork
  #
  def addRecentNetwork ( self, network ) :
    #
    if network is not None :
      recent_networks_max = getDefaultValue ( app_settings, '', 'recent_networks_max' )

      if not self.recentNetworks.contains ( network ) :
        self.recentNetworks.prepend ( QtCore.QString ( network ) )

      while self.recentNetworks.count () > recent_networks_max :
        self.recentNetworks.takeLast ()

      recentNetworks = QtCore.QVariant ( self.recentNetworks ) if self.recentNetworks else QtCore.QVariant ()
      app_settings.setValue ( 'RecentNetworks', recentNetworks )
  #
  # setupActions
  #
  def setupActions ( self ) :
    #
    #if DEBUG_MODE : print '>> MainWindow.setupActions'
    numNodes = 0
    numSelectedNodes = 0
    numSelectedLinks = 0
    selectedNodeType = None
    if self.workArea is not None :
      numNodes = len ( self.workArea.getAllGfxNodes () )
      numSelectedNodes = len ( self.workArea.selectedNodes )
      numSelectedLinks = len ( self.workArea.selectedLinks )
      if numSelectedNodes == 1 :
        selectedNodeType = self.getSelectedNode ().node.type
    enableForPaste = False

    if self.clipboard.ownsClipboard () or (sys.platform == 'darwin'):
      if DEBUG_MODE : print '** self.clipboard.ownsClipboard'
      data = self.clipboard.mimeData ()
      if data is not None :
        if data.hasText () :
          enableForPaste = True
          
    self.ui.actionExportShader.setEnabled ( selectedNodeType in VALID_RSL_SHADER_TYPES )
    self.ui.actionViewComputedCode.setEnabled ( selectedNodeType in VALID_RSL_NODE_TYPES or selectedNodeType in VALID_RIB_NODE_TYPES )
    self.ui.actionSaveSelected.setEnabled ( numSelectedNodes > 0 )
    self.ui.actionSelectAll.setEnabled ( numNodes > 0 )
    self.ui.actionSelectAbove.setEnabled ( numSelectedNodes == 1 )
    self.ui.actionSelectBelow.setEnabled ( numSelectedNodes == 1 )
    self.ui.actionDuplicate.setEnabled ( numSelectedNodes > 0 )
    self.ui.actionDuplicateWithLinks.setEnabled ( numSelectedNodes > 0 )
    self.ui.actionDelete.setEnabled ( ( numSelectedNodes > 0 ) or ( numSelectedLinks > 0 ) )
    self.ui.actionCut.setEnabled ( numSelectedNodes > 0 )
    self.ui.actionCopy.setEnabled ( numSelectedNodes > 0 )
    self.ui.actionPaste.setEnabled ( enableForPaste )
    self.ui.actionFitAll.setEnabled ( numNodes > 0 )
    self.ui.actionFitSelected.setEnabled ( numSelectedNodes > 0 )
  #
  # onProjectSetup
  #
  def onProjectSetup ( self ) :
    #
    if DEBUG_MODE : print ">> MainWindow.onProjectSetup"
    projectSetupDlg = ProjectSetup ( app_settings )
    projectSetupDlg.exec_()
    self.ui.project_ctl.setLibrary ( app_global_vars [ 'ProjectNetworks' ] )
    createDefaultProject ( app_settings )
    self.setupWindowTitle ()
    self.addRecentProject ( app_global_vars [ 'ProjectPath' ] )
    self.buildRecentProjectsMenu ()
  #
  # onSettingsSetup
  #
  def onSettingsSetup ( self ) :
    #
    if DEBUG_MODE : print '>> MainWindow.onSettingsSetup'
    settingsSetupDlg = SettingsSetup ( app_settings )
    settingsSetupDlg.exec_()
    self.ui.nodeList_ctl.setLibrary ( app_global_vars [ 'NodesPath' ] )
  #
  # onRenderSettings
  #
  def onRenderSettings ( self ) :
    #
    if DEBUG_MODE : print ( '>> MainWindow::onRenderSettings' )
    import copy
    self.RendererPreset = copy.deepcopy ( app_global_vars [ 'RendererPreset' ] )
    renderSettingsDlg = meRendererSetup ( self.RendererPreset )
    QtCore.QObject.connect ( renderSettingsDlg, QtCore.SIGNAL ( 'presetChanged' ), self.onRenderPresetChanged )
    QtCore.QObject.connect ( renderSettingsDlg, QtCore.SIGNAL ( 'savePreset' ), self.onRenderPresetSave )
    renderSettingsDlg.exec_ ()
  #
  # onRenderPresetChanged
  #
  def onRenderPresetChanged ( self ) :
    #
    if DEBUG_MODE : print ( '>> MainWindow::onRenderPresetChanged preset = %s' % self.RendererPreset.getCurrentPresetName () )
    app_settings.setValue ( 'defRenderer', self.RendererPreset.getCurrentPresetName () )
 
    app_global_vars [ 'RendererName' ]   = self.RendererPreset.currentPreset.RendererName
    app_global_vars [ 'RendererFlags' ]  = self.RendererPreset.currentPreset.RendererFlags
    app_global_vars [ 'ShaderCompiler' ] = self.RendererPreset.currentPreset.ShaderCompiler
    app_global_vars [ 'ShaderDefines' ]  = self.RendererPreset.currentPreset.ShaderDefines
    app_global_vars [ 'ShaderInfo' ]     = self.RendererPreset.currentPreset.ShaderInfo
    app_global_vars [ 'SLO' ]            = self.RendererPreset.currentPreset.ShaderExt
    app_global_vars [ 'TextureMake' ]    = self.RendererPreset.currentPreset.TextureMake
    app_global_vars [ 'TextureInfo' ]    = self.RendererPreset.currentPreset.TextureInfo
    app_global_vars [ 'TextureViewer' ]  = self.RendererPreset.currentPreset.TextureViewer
    app_global_vars [ 'TEX' ]            = self.RendererPreset.currentPreset.TextureExt
    app_global_vars [ 'RendererPreset' ] = self.RendererPreset
    self.setupWindowTitle ()
  #
  # onRenderPresetSave
  #
  def onRenderPresetSave ( self ) :
    #
    if DEBUG_MODE : print ( '>> MainWindow::onRenderPresetSave  preset = %s' % self.RendererPreset.getCurrentPresetName () )
    self.RendererPreset.saveSettings ()
    app_global_vars [ 'RendererPreset' ] = self.RendererPreset 
  #
  # onShowGrid
  #
  def onShowGrid ( self, check ) :
    #
    self.workArea.drawGrid = bool ( check )
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'grid_enabled', bool ( check ) )
    app_settings.endGroup ()

    self.workArea.resetCachedContent ()
    #self.ui.workArea.update()
  #
  # onSnapGrid
  #
  def onSnapGrid ( self, check ) :
    #
    self.workArea.gridSnap = bool ( check )
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'grid_snap', bool ( check ) )
    app_settings.endGroup ()
  #
  # onReverseFlow
  #
  def onReverseFlow ( self, check ) :
    #
    self.workArea.reverseFlow = bool ( check )
    app_settings.beginGroup ( 'WorkArea' )
    app_settings.setValue ( 'reverse_flow', bool ( check ) )
    app_settings.endGroup ()

    #self.ui.workArea.resetCachedContent()
  #
  # onStraightLinks
  #
  def onStraightLinks ( self, check ) :
    #
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
    #
    if DEBUG_MODE : print '>> MainWindow.setActiveNodeList'
    if self.activeNodeList != None :
      QtCore.QObject.disconnect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
    self.activeNodeList = nodeList
    QtCore.QObject.connect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
  #
  # onGetNode
  #
  # Called by WorkArea after drag&drop event
  # Here we choose selected nodeList panel (Library or Project)
  # for processing node request
  #
  def onGetNode ( self, itemFilename, pos ) :
    #
    if self.activeNodeList != None : self.activeNodeList.onGetNode ( itemFilename, pos )
  #
  # onAddGfxNode
  #
  def onAddGfxNode ( self, gfxNode ) :
    #
    #print ">> MainWindow: onAddGfxNode = %s" % gfxNode.node.label
    if gfxNode.node.format == 'image' : self.ui.imageView_ctl.addViewer ( gfxNode )

      #if self.ui.nodeParam_ctl.receivers( QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ) ) == 0 :
      #  QtCore.QObject.connect( self.ui.nodeParam_ctl, QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self.ui.imageView_ctl.onNodeParamChanged )
      #else :
      #  print ">> MainWindow: nodeParam_ctl onNodeParamChanged already connected to imageView_ctl"
  #
  # onRemoveGfxNode
  #
  def onRemoveGfxNode ( self, gfxNode ) :
    #
    if DEBUG_MODE : print '>> MainWindow.onRemoveGfxNode = %s' % gfxNode.node.label
    if gfxNode.node.format == 'image' :
      self.ui.imageView_ctl.removeViewer ( gfxNode )
      #QtCore.QObject.disconnect ( self.ui.nodeParam_ctl, QtCore.SIGNAL ( 'onNodeParamChanged(QObject,QObject)' ), self.ui.imageView_ctl.onNodeParamChanged )
  #
  # getSelectedNode
  #
  def getSelectedNode ( self ) : return self.workArea.selectedNodes [0]
  #
  # onRenderPreview
  #
  def onRenderPreview ( self ) : print ">> MainWindow.onRenderPreview (not implemented yet...)"
  #
  # onShowSwatch
  #
  def onShowSwatch ( self ) : print ">> MainWindow.onShowSwatch (not implemented yet...)"
  #
  # onHideSwatch
  #
  def onHideSwatch ( self ) : print ">> MainWindow.onHideSwatch (not implemented yet...)"
  #
  # onCreateNode
  #
  def onCreateNode ( self ) : print ">> MainWindow.onCreateNode (not implemented yet...)"
  #
  # onExportShader
  #
  def onExportShader ( self ) : 
    #
    if DEBUG_MODE : print ">> MainWindow.onExportShader"
    gfxNode = self.getSelectedNode ()
    exportShaderDlg = ExportShaderDialog ( gfxNode.node )
    exportShaderDlg.exec_ ()
    if exportShaderDlg.ui.chk_save_changes.isChecked () :
      if DEBUG_MODE : print '>> MainWindow.exportShaderDlg save changes'
      gfxNode.updateGfxNode ( removeLinks = False )
      self.workArea.updateBelow ( gfxNode )
      self.updateNodeParamView ()
      self.workArea.scene().update ()
  #
  # onViewComputedCode
  #
  def onViewComputedCode ( self ) : ViewComputedCodeDialog ( self.getSelectedNode ().node ).exec_ ()
    
  #
  # onEditNode
  #
  def onEditNode ( self ) : 
    #
    if DEBUG_MODE : print ">> MainWindow.onEditNode"

    gfxNode = self.getSelectedNode ()
    editNode = gfxNode.node.copy ()

    dupNodeNet = NodeNetwork ( 'duplicate' )
    dupNodeNet.addNode ( editNode )
    #
    # copy input links to new node
    #
    if DEBUG_MODE : print '** duplicate input links ...'
    for link in gfxNode.node.getInputLinks () :
      newLink = link.copy ()
      newParam = editNode.getInputParamByName ( link.dstParam.name )
      newLink.setDst ( editNode, newParam )
      dupNodeNet.addLink ( newLink )

      newLink.printInfo ()
    #
    # copy output links to new node
    #
    if DEBUG_MODE : print '** duplicate output links ...'
    for link in gfxNode.node.getOutputLinks () :
      newLink = link.copy ()
      newParam = editNode.getOutputParamByName ( link.srcParam.name )
      newLink.setSrc ( editNode, newParam )
      dupNodeNet.addLink ( newLink )

      newLink.printInfo ()

    nodeEditDlg = NodeEditorDialog ( editNode )

    if nodeEditDlg.exec_ () == QtGui.QDialog.Accepted :
      #
      if DEBUG_MODE : print '>> MainWindow.nodeEditDlg Accepted'
      #
      # remove original node with links
      ( inputLinksToRemove, outputLinksToRemove ) = self.workArea.nodeNet.removeNode ( gfxNode.node )

      for link in inputLinksToRemove  : self.workArea.nodeNet.removeLink ( link  )
      for link in outputLinksToRemove : self.workArea.nodeNet.removeLink ( link  )

      # add duplicate network to current node net
      self.workArea.nodeNet.add ( dupNodeNet )

      if gfxNode.node.label != editNode.label :
        self.ui.imageView_ctl.onNodeLabelChanged ( gfxNode, editNode.label )

      # set new node to gfxNode.node
      gfxNode.node = editNode
      gfxNode.updateGfxNode ()
      for link in editNode.getInputLinks ()  : self.workArea.addGfxLink ( link  )
      for link in editNode.getOutputLinks () : self.workArea.addGfxLink ( link  )
      self.updateNodeParamView ()
      self.workArea.scene().update ()

    else :
      # remove duplicate node network
      dupNodeNet.clear ()
  #
  # onDelete
  #
  def onDelete ( self ) :
    #
    selected = self.workArea.scene ().selectedItems ()
    if len ( selected ) :
      self.workArea.removeSelected ()
    else :
      self.ui.imageView_ctl.removeAllViewers ()
      self.workArea.clear()
  #
  # onSelectAll
  #
  def onSelectAll ( self ) : self.workArea.selectAllNodes ()
  #
  # onSelectAbove
  #
  def onSelectAbove ( self ) : self.workArea.selectAbove ( self.getSelectedNode () )
  #
  # onSelectBelow
  #
  def onSelectBelow ( self ) : self.workArea.selectBelow ( self.getSelectedNode () )
  #
  # onCopy
  #
  def onCopy ( self ) :
    if DEBUG_MODE : print '>> MainWindow.onCopy'
    self.workArea.copyNodes ( self.clipboard, cutNodes = False )
    self.setupActions ()
  #
  # onCut
  #
  def onCut ( self ) :
     if DEBUG_MODE : print '>> MainWindow.onCut'
     self.workArea.copyNodes ( self.clipboard, cutNodes = True )
     self.setupActions ()
  #
  # onPaste
  #
  def onPaste ( self ) :
    if DEBUG_MODE : print '>> MainWindow.onPaste'
    self.workArea.pasteNodes ( self.clipboard )
  #
  # onDuplicate
  #
  def onDuplicate ( self ) : self.workArea.duplicateNodes ( preserveLinks = False )
  #
  # onDuplicateWithLinks
  #
  def onDuplicateWithLinks ( self ) : self.workArea.duplicateNodes ( preserveLinks = True )
  #
  # onSelectGfxNodes
  #
  def onSelectGfxNodes ( self, gfxNodes = [], gfxLinks = [] ) :
    #
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
  def onNodeParamChanged ( self, gfxNode, param ) :
    #
    if DEBUG_MODE : print ">> MainWindow.onNodeParamChanged"
    #param.shaderParam = not gfxNode.node.isInputParamLinked ( param )

    # from WorkArea we have GfxNode in signal nodeConnectionChanged
    # hence need to update nodeParam_ctl
    if isinstance ( gfxNode, GfxNote ) :
      #if DEBUG_MODE : print "* update GfxNote"
      gfxNode.updateGfxNode ()
      #node.update ()
      self.workArea.scene ().update ()
    elif isinstance ( gfxNode, GfxSwatchNode ) :
      if DEBUG_MODE : print "* update GfxSwatchNode"
      gfxNode.setupSwatchParams ()
      gfxNode.setupGeometry ()
      gfxNode.adjustLinks ()
      self.workArea.scene ().update ()
    elif isinstance ( gfxNode, GfxNode ) :
      if DEBUG_MODE : print "* update GfxNode"
      gfxNode.updateGfxNode ( removeLinks = False )
      self.updateNodeParamView ()

    if self.ui.imageView_ctl.autoUpdate () : self.ui.imageView_ctl.updateViewer()
  #
  # onGxNodeParamChanged
  #
  def onGfxNodeParamChanged ( self, gfxNode, param = None ) :
    #
    if DEBUG_MODE : print ">> MainWindow.onGxNodeParamChanged" 
    
    # from WorkArea we have GfxNode in signal nodeConnectionChanged
    # hence need to update nodeParam_ctl
    if isinstance ( gfxNode, GfxNode ) or isinstance ( gfxNode, GfxSwatchNode ) :
      #if DEBUG_MODE : print "* update nodeView"
      # gfxNode.updateInputParams ()
      self.updateNodeParamView ()
      self.workArea.scene ().update ()

    if self.ui.imageView_ctl.autoUpdate () : self.ui.imageView_ctl.updateViewer()
  #
  # updateNodeParamView
  #
  def updateNodeParamView ( self, gfxNode = None ) :
    #
    if DEBUG_MODE : 
      print '>> MainWindow.updateNodeParamView'
      if gfxNode is not None :
        print '** gfxNode = "%s"' % gfxNode.node.label
    self.ui.nodeParam_ctl.disconnectParamSignals ()
    self.ui.nodeParam_ctl.connectParamSignals ()
    self.ui.nodeParam_ctl.updateGui ()
  #
  # onFitAll
  #
  def onFitAll ( self ) : self.workArea.fitGfxNodesInView ( self.workArea.getAllGfxNodes () )
  #
  # onFitSelected
  #
  def onFitSelected ( self ) : self.workArea.fitGfxNodesInView ( self.workArea.selectedNodes )
  #
  # onZoomReset
  #
  def onZoomReset ( self ) : self.workArea.resetZoom ()
  #
  # onNewParamView
  #
  def onNewParamView ( self ) : print ">> MainWindow.onNewParamView (not implemented yet...)"
  #
  # onTabSelected
  #
  def onTabSelected ( self, idx ) :
    #
    if DEBUG_MODE : print '>> MainWindow.onTabSelected (%d)' % idx
    self.disconnectWorkAreaSignals ()
    self.ui.imageView_ctl.removeAllViewers ()
    self.workArea = self.ui.tabs.currentWidget ()

    imageNodes = self.workArea.getGfxNodesByFormat ( 'image' )
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
    if self.ui.tabs.count () > 1 :
      self.workArea.nodeNet.clear ()
      self.ui.tabs.removeTab ( idx )
  #
  # onNew
  #
  def onNew ( self, tabName = 'untitled' ) :
    #
    def tabNameExists ( self, name ) :
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

    self.ui.tabs.setTabText ( self.ui.tabs.indexOf ( workArea ), newName )
    self.ui.tabs.setCurrentIndex ( self.ui.tabs.indexOf ( workArea ) )
  #
  # onOpen
  #
  def onOpen ( self ) :
    #
    if DEBUG_MODE : print ">> MainWindow.onOpen"
    #
    curDir = app_global_vars [ 'ProjectNetworks' ]
    typeFilter = 'Shader networks *.xml;;All files *.*;;'

    filename = str ( QtGui.QFileDialog.getOpenFileName ( self, "Open file", curDir, typeFilter ) )
    if filename != '' :
      if self.openNetwork ( filename ) :
        self.addRecentNetwork ( normPath ( filename ) )
        self.buildRecentNetworksMenu ()
  #
  # openNetwork
  #
  def openNetwork ( self, filename ) :
    #
    ret = True
    if DEBUG_MODE : print "-> open file %s" %  filename
    if QtCore.QFile.exists ( filename ) :
      ( name, ext ) = os.path.splitext ( os.path.basename ( filename ) )

      self.ui.imageView_ctl.removeAllViewers ()

      self.workArea.clear ()
      self.workArea.nodeNet.name = name
      self.workArea.nodeNet.fileName = ''
      self.ui.tabs.setTabText ( self.ui.tabs.indexOf ( self.workArea ), name )

      self.workArea.openNodeNet ( normPath ( filename ) )
    else :
      print "ERROR! filename %s doesn't exist" %  filename
      ret = False
    return ret
  #
  # onOpenRecentNetwork
  #
  def onOpenRecentNetwork ( self ) :
    #
    action = self.sender ()
    if isinstance ( action, QtGui.QAction ):
      network = unicode ( action.data ().toString () )
      if network is not None :
        if DEBUG_MODE : print '>> onOpenRecentNetwork : %s' % network
        if not self.openNetwork ( network ) :
          # TODO!!! remove network from rescentNetworks
          pass
  #
  # onOpenRecentProject
  #
  def onOpenRecentProject ( self ) :
    #
    action = self.sender ()
    if isinstance ( action, QtGui.QAction ):
      project = unicode ( action.data ().toString () )
      if project is not None :
        print '>> onOpenRecentProject : %s' % project
        if openDefaultProject ( app_settings, app_global_vars, project ) :
          # very strange... app_settings doesn't update inside meCommon.openDefaultProject...
          # though app_global_vars does
          # have to duplicate this action here...
          app_settings.setValue ( 'project', app_global_vars [ 'ProjectPath' ] )
          app_settings.setValue ( 'project_shaders', app_global_vars [ 'ProjectShaders' ] )
          app_settings.setValue ( 'project_textures', app_global_vars [ 'ProjectTextures' ] )
          app_settings.setValue ( 'shader_networks', app_global_vars [ 'ProjectNetworks' ] )
          app_settings.setValue ( 'shader_sources', app_global_vars [ 'ProjectSources' ] )

          self.ui.project_ctl.setLibrary ( app_global_vars [ 'ProjectNetworks' ] )
          self.setupWindowTitle ()
        else :
          print "ERROR! project %s doesn't exist" %  project
          # TODO!!! remove project from rescentProjects
  #
  # onImport
  #
  def onImport ( self ) :
    #
    if DEBUG_MODE : print ">> MainWindow.onImport"
    #
    curDir = app_global_vars [ 'ProjectNetworks' ]
    typeFilter = 'Shader networks *.xml;;All files *.*;;'

    filename = str ( QtGui.QFileDialog.getOpenFileName ( self, "Import file", curDir, typeFilter ) )
    if filename != '' :
      if DEBUG_MODE : print "-> import file %s" %  filename
      self.workArea.insertNodeNet ( normPath ( filename ) )
  #
  # onSaveSelected
  #
  def onSaveSelected ( self ) :  
    #
    if DEBUG_MODE : print ">> MainWindow.onSaveSelected"
    singleNode = ( len ( self.workArea.selectedNodes ) == 1 )
    curDir = app_global_vars [ 'ProjectNetworks' ]
    saveName = os.path.join ( curDir, self.workArea.nodeNet.name + '.xml' )
    typeFilter = 'Shader networks *.xml;;All files *.*;;'

    filename = str( QtGui.QFileDialog.getSaveFileName ( self, "Save file as", saveName, typeFilter ) )
    if filename != '' :
      if DEBUG_MODE : print '-> save file As %s' % filename
      ( name, ext ) = os.path.splitext ( os.path.basename ( filename ) )
      if singleNode :
      # save single node
        print '*** save as single Node'
        gfxNode =  self.getSelectedNode ()
        saveNode = gfxNode.node.copy ()
        saveNode.name = name
        saveNode.master = normPath ( filename )
        saveNode.save ()
      else :
      # save selected as network
        print '*** save as nodenet'
        saveNodeNet = self.workArea.nodeNetFromSelected ( name )
        saveNodeNet.fileName = normPath ( filename ) 
        saveNodeNet.save ()
  #
  # onSave
  #
  def onSave ( self ) :
    #
    if DEBUG_MODE : print ">> MainWindow.onSave"
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
  def onSaveAs ( self ) :
    #
    if DEBUG_MODE : print ">> MainWindow.onSaveAs"
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
      self.addRecentNetwork ( normPath ( filename ) )
      self.buildRecentNetworksMenu ()
      self.ui.project_ctl.onReload ()
  #
  # onHelpNode
  #
  def onHelpMode ( self, showWhatsThis ) :
    #
    #if showWhatsThis :
    QtGui.QWhatsThis.enterWhatsThisMode ()
    #else :
    #  QtGui.QWhatsThis.leaveWhatsThisMode ()
