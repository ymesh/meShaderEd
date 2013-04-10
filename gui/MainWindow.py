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
from core.nodeNetwork import *

from gfx.gfxNode import GfxNode
from gfx.gfxNote import GfxNote

from meRendererSetup import meRendererSetup
from ProjectSetup import ProjectSetup
from SettingsSetup import SettingsSetup
from NodeEditorPanel import NodeEditorPanel
from ExportShaderPanel import ExportShaderPanel

from nodeList import NodeList

from gfx.WorkArea import WorkArea

from meShaderEd import app_settings
from meShaderEd import app_renderer
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

    # This is always the same
    self.ui = Ui_MainWindow ()

    self.ui.setupUi ( self )

    self.recentProjects = app_settings.value ( 'RecentProjects' ).toStringList ()
    self.recentNetworks = app_settings.value ( 'RecentNetworks' ).toStringList ()

    self.addRecentProject ( app_global_vars [ 'ProjectPath' ] )

    self.setupMenuBar ()
    self.setupPanels ()

    self.clipboard = None
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
    if self.workArea != None :
      if self.activeNodeList != None :
        QtCore.QObject.connect ( self.activeNodeList, QtCore.SIGNAL ( 'addNode' ), self.workArea.insertNodeNet  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'selectNodes' ), self.onSelectGfxNodes  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'nodeConnectionChanged' ), self.onNodeParamChanged  )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeAdded' ), self.onAddGfxNode )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'gfxNodeRemoved' ), self.onRemoveGfxNode )
      QtCore.QObject.connect ( self.workArea, QtCore.SIGNAL ( 'editGfxNode' ), self.editGfxNode )
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
      QtCore.QObject.disconnect ( self.workArea, QtCore.SIGNAL ( 'editGfxNode' ), self.editGfxNode )
  #
  #
  #
  def setupWindowTitle ( self ) :
    self.setWindowTitle ( 'meShaderEd %s (%s) %s' % ( app_global_vars [ 'version' ], app_renderer.getCurrentPresetName(), app_global_vars [ 'ProjectPath' ]  ) )
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
    self.tabifyDockWidget ( self.ui.dockGeom, self.ui.dockPreview )
    self.tabifyDockWidget ( self.ui.dockProject, self.ui.dockNodes )

    self.removeDockWidget ( self.ui.dockParam )
    self.addDockWidget ( QtCore.Qt.DockWidgetArea ( 2 ), self.ui.dockParam )
    self.ui.dockParam.show ()
  #
  # addRecentProject
  #
  def addRecentProject ( self, project ) :
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
    enableForNodes = False
    enableForLinks = False
    enableForPaste = False
    enableSelectAll = False
    if self.clipboard is not None : enableForPaste = True
    if self.workArea is not None :
      enableSelectAll = True
      if len ( self.workArea.selectedNodes ) > 0 : enableForNodes = True
      if len ( self.workArea.selectedLinks ) > 0 : enableForLinks = True

    self.ui.actionSelectAll.setEnabled ( enableSelectAll )
    self.ui.actionSelectAbove.setEnabled ( len ( self.workArea.selectedNodes ) == 1 )
    self.ui.actionSelectBelow.setEnabled ( len ( self.workArea.selectedNodes ) == 1 )

    self.ui.actionDuplicate.setEnabled ( enableForNodes )
    self.ui.actionDuplicateWithLinks.setEnabled ( enableForNodes )
    self.ui.actionDelete.setEnabled ( enableForNodes or enableForLinks )

    self.ui.actionCut.setEnabled ( enableForNodes )
    self.ui.actionCopy.setEnabled ( enableForNodes )
    self.ui.actionPaste.setEnabled ( enableForPaste )
  #
  # onProjectSetup
  #
  def onProjectSetup ( self ) :
    #
    if DEBUG_MODE : print ">> MainWindow: onProjectSetup"
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
    if DEBUG_MODE : print '>> MainWindow: onSettingsSetup'
    settingsSetupDlg = SettingsSetup ( app_settings )
    settingsSetupDlg.exec_()
    self.ui.nodeList_ctl.setLibrary ( app_global_vars [ 'NodesPath' ] )

  #
  # onRenderSettings
  #
  def onRenderSettings ( self ) :
    #
    if DEBUG_MODE : print '>> MainWindow: onRenderSettings'
    renderSettingsDlg = meRendererSetup ( app_renderer )
    QtCore.QObject.connect ( renderSettingsDlg, QtCore.SIGNAL ( 'presetChanged' ), self.onRenderPresetChanged )
    QtCore.QObject.connect ( renderSettingsDlg, QtCore.SIGNAL ( 'savePreset' ), self.onRenderSavePreset )
    renderSettingsDlg.exec_ ()
  #
  # onRenderPresetChanged
  #
  def onRenderPresetChanged ( self ) :
    #
    presetName = app_renderer.getCurrentPresetName()
    if DEBUG_MODE : print '>> MainWindow: onRenderPresetChanged preset = %s' % presetName
    #self.setWindowTitle ( 'meShaderEd %s (%s) %s' % ( app_global_vars [ 'version' ], presetName, app_global_vars [ 'ProjectNetworks' ] ) )
    app_settings.setValue ( 'defRenderer', presetName )

    app_global_vars [ 'Renderer' ] = app_renderer.getCurrentValue ( 'renderer', 'name' )
    app_global_vars [ 'RendererFlags' ] = app_renderer.getCurrentValue ( 'renderer', 'flags' )
    app_global_vars [ 'ShaderCompiler' ] = app_renderer.getCurrentValue ( 'shader', 'compiler' )
    app_global_vars [ 'ShaderDefines' ] = app_renderer.getCurrentValue ( 'shader', 'defines' )
    app_global_vars [ 'TEX' ] = app_renderer.getCurrentValue ( 'texture', 'extension' )
    app_global_vars [ 'SLO' ] = app_renderer.getCurrentValue ( 'shader', 'extension' )
    self.setupWindowTitle ()
  #
  # onRenderSavePreset
  #
  def onRenderSavePreset ( self ) :
    #
    if DEBUG_MODE : print '>> MainWindow: onRenderSavePreset  preset = %s' % app_renderer.getCurrentPresetName()
    app_renderer.saveSettings ()
  #
  # onShowGrid
  #
  def onShowGrid ( self, check ) :
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
  def onSnapGrid ( self, check ) :
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
  def onReverseFlow ( self, check ) :
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
  def onStraightLinks ( self, check ) :
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
  # Here we choose selected nodeList panel (Library or Project)
  # for processing node request
  def onGetNode ( self, itemFilename, pos ) :
    #
    if self.activeNodeList != None : self.activeNodeList.onGetNode ( itemFilename, pos )
  #
  # onAddGfxNode
  #
  def onAddGfxNode ( self, gfxNode ) :
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
  def onRemoveGfxNode ( self, gfxNode ) :
    #
    if DEBUG_MODE : print '>> MainWindow: onRemoveGfxNode = %s' % gfxNode.node.label
    if gfxNode.node.type == 'image' :
      self.ui.imageView_ctl.removeViewer ( gfxNode )
      #QtCore.QObject.disconnect ( self.ui.nodeParam_ctl, QtCore.SIGNAL ( 'onNodeParamChanged(QObject,QObject)' ), self.ui.imageView_ctl.onNodeParamChanged )
  #
  # getSelectedNode
  #
  def getSelectedNode ( self ) : return self.workArea.selectedNodes [0]
  #
  # onCreateNode
  #
  def onCreateNode ( self ) : print ">> MainWindow::onCreateNode (not implemented yet...)"
  #
  # onEditNode
  #
  def onEditNode ( self ) : self.editGfxNode ( self.getSelectedNode () )
  #
  # onExportShader
  #
  def onExportShader ( self ) : self.exportShader ( self.getSelectedNode () )
  #
  # exportShader
  #
  def exportShader ( self, gfxNode ) :
    #
    if DEBUG_MODE : print ">> MainWindow::exportShader (not implemented yet...)"
    gfxNode = self.getSelectedNode ()
    
    exportShaderDlg = ExportShaderPanel ()
    if exportShaderDlg.exec_ () == QtGui.QDialog.Accepted :
      if DEBUG_MODE : print '>> MainWindow::exportShaderDlg Accepted'
      #
      #
      return  
  #
  # editGfxNode
  #
  def editGfxNode ( self, gfxNode ) :
    #
    if DEBUG_MODE : print ">> MainWindow::editGfxNode"

    # reindex input params
    #for i in range ( 0, len( gfxNode.node.inputParams ) ) : gfxNode.node.inputParams[ i ].id = i

    # reindex output params
    #for i in range ( 0, len( gfxNode.node.outputParams ) ) : gfxNode.node.outputParams[ i ].id = i
    
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
      
    nodeEditDlg = NodeEditorPanel ( editNode )
    
    if nodeEditDlg.exec_ () == QtGui.QDialog.Accepted :
      #
      if DEBUG_MODE : print '>> MainWindow::nodeEditDlg Accepted'
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
      gfxNode.updateNode ()
      for link in editNode.getInputLinks ()  : self.workArea.addGfxLink ( link  )  
      for link in editNode.getOutputLinks () : self.workArea.addGfxLink ( link  )  
      #self.ui.nodeParam_ctl.setNode ( gfxNode )
      #gfxNode.update ()
      #gfxNode.adjustLinks ()
      self.ui.nodeParam_ctl.updateGui ()
      #self.workArea.resetCachedContent ()
      #self.workArea.adjustLinks ()
      self.workArea.scene().update ()
      
    else :
      # remove duplicate node network     
      dupNodeNet.clear ()
  #
  # onDelete
  #
  def onDelete ( self ) :
    #
    if DEBUG_MODE : print '>> MainWindow::onDelete'

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
  def onCopy ( self ) : print '>> MainWindow::onCopy'
  #
  # onCut
  #
  def onCut ( self ) : print '>> MainWindow::onCut'
  #
  # onPaste
  #
  def onPaste ( self ): print '>> MainWindow::onPaste'
  #
  # onDuplicate
  #
  def onDuplicate ( self ): self.workArea.duplicateNode ( preserveLinks = False )
  #
  # onDuplicateWithLinks
  #
  def onDuplicateWithLinks ( self ): print '!! MainWindow::onDuplicateWithLinks is not implemented yet ...'
    # self.workArea.dDuplicateNode ( preserveLinks = True )
  #
  # onSelectGfxNodes
  #
  def onSelectGfxNodes ( self, gfxNodes = [], gfxLinks = [] ) :
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
    #if DEBUG_MODE : print ">> MainWindow: onNodeParamChanged"
    #param.shaderParam = not gfxNode.node.isInputParamLinked ( param )

    # from WorkArea we have GfxNode in signal nodeConnectionChanged
    # hence need to update nodeParam_ctl
    if isinstance ( node, GfxNode )  :
      #if DEBUG_MODE : print "* update nodeView"
      node.updateInputParams ()
      self.ui.nodeParam_ctl.updateGui ()
    elif isinstance ( node, GfxNote ) :
      #if DEBUG_MODE : print "* update GfxNote"
      node.updateNode ()
      #node.update ()
      self.workArea.scene ().update ()

    if self.ui.imageView_ctl.autoUpdate () :
      #if DEBUG_MODE : print "* auto update"
      self.ui.imageView_ctl.updateViewer()
  #
  # onFitAll
  #
  def onFitAll ( self ) : print ">> MainWindow: onFitAll"
  #
  # onFitSelected
  #
  def onFitSelected ( self ) : print ">> MainWindow: onFitSelected"
  #
  # onZoomReset
  #
  def onZoomReset ( self ) : self.workArea.resetZoom ()
  #
  # onNewParamView
  #
  def onNewParamView ( self ) : print ">> MainWindow: onNewParamView"
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
  def onNew ( self, tabName = 'untitled' ) :
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
  def onOpen ( self ) :
    #
    if DEBUG_MODE : print ">> MainWindow: onOpen"
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
      ( name, ext ) = os.path.splitext( os.path.basename ( filename ) )

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
  def onSave ( self ) :
    #
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
  def onSaveAs ( self ) :
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
      self.addRecentNetwork ( normPath ( filename ) )
      self.buildRecentNetworksMenu ()
      self.ui.project_ctl.onReload ()

