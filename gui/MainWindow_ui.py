# -*- coding: utf-8 -*-

from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

if not usePyQt5 :
    QtModule = QtGui
else :
    from core.mePyQt import QtWidgets
    QtModule = QtWidgets
#
# Ui_MainWindow
#
class Ui_MainWindow ( object) :
    #
    def setupUi ( self, MainWindow ) :
        #
        MainWindow.setObjectName ( "MainWindow" )
        MainWindow.setWindowTitle ( "meShaderEd" )
        MainWindow.resize ( 1200, 900 )
        MainWindow.setDockOptions ( QtModule.QMainWindow.AllowTabbedDocks |
                                                                QtModule.QMainWindow.AnimatedDocks )
        MainWindow.setUnifiedTitleAndToolBarOnMac ( False )

        self.centralwidget = QtModule.QWidget ( MainWindow )
        self.centralwidget.setAcceptDrops ( True )
        self.centralwidget.setObjectName ( "centralwidget" )

        self.gridLayout = QtModule.QGridLayout ( self.centralwidget )
        self.gridLayout.setContentsMargins ( 0, 0, 0, 0 )
        self.gridLayout.setObjectName ( "gridLayout" )

        self.tabs = QtModule.QTabWidget ( self.centralwidget )
        self.tabs.setAcceptDrops ( True )
        self.tabs.setTabPosition ( QtModule.QTabWidget.North )
        self.tabs.setTabShape ( QtModule.QTabWidget.Rounded )
        self.tabs.setElideMode ( QtCore.Qt.ElideNone )
        self.tabs.setDocumentMode ( True )
        self.tabs.setTabsClosable ( True )
        self.tabs.setMovable ( False )

        self.workArea = WorkArea ()
        self.workArea.setAcceptDrops ( True )

        self.tabs.addTab ( self.workArea, "" )
        self.tabs.setTabText ( self.tabs.indexOf ( self.workArea), "none" )
        self.tabs.setCurrentIndex ( 0 )
        
        self.gridLayout.addWidget ( self.tabs, 0, 0, 1, 1 )

        MainWindow.setCentralWidget ( self.centralwidget )

        self.statusbar = QtModule.QStatusBar ( MainWindow )

        MainWindow.setStatusBar ( self.statusbar )

        self.dockNodes = QtModule.QDockWidget ( "Library", MainWindow )
        self.dockNodes.setMinimumSize ( QtCore.QSize ( 150, 42 ) )
        self.dockNodes.setFloating ( False )
        self.dockNodes.setAllowedAreas ( QtCore.Qt.LeftDockWidgetArea |
                                                                         QtCore.Qt.RightDockWidgetArea )
        self.nodeList_ctl = NodeLibraryView ()
        self.dockNodes.setWidget ( self.nodeList_ctl )
        
        self.dockPreview = QtModule.QDockWidget ( "Image View", MainWindow )
        self.dockPreview.setBaseSize ( QtCore.QSize ( 300, 0 ) )
        self.dockPreview.setFloating ( False )
        self.dockPreview.setFeatures ( QtModule.QDockWidget.AllDockWidgetFeatures )
        self.dockPreview.setAllowedAreas ( QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea )
        self.imageView_ctl = ImageViewWidget ()
        self.dockPreview.setWidget ( self.imageView_ctl )
        
        self.dockParam = QtModule.QDockWidget ( "Node Parameters", MainWindow )
        self.dockParam.setBaseSize ( QtCore.QSize ( 300, 0 ) )
        self.dockParam.setFeatures ( QtModule.QDockWidget.AllDockWidgetFeatures )
        self.dockParam.setAllowedAreas ( QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea )
        self.nodeParam_ctl = NodeParamView ()
        self.dockParam.setWidget ( self.nodeParam_ctl )
        
        self.dockGeom = QtModule.QDockWidget ( "Geometry View", MainWindow )
        self.geomView_ctl = GeomViewWidget ()
        self.dockGeom.setWidget ( self.geomView_ctl )
        
        self.dockProject = QtModule.QDockWidget ( "Project",  MainWindow )
        self.project_ctl = NodeLibraryView()
        self.dockProject.setWidget ( self.project_ctl )
        
        self.dockSwatch = QtModule.QDockWidget ( "Node Preview",MainWindow )
        self.swatchParam_ctl = NodeSwatchParam ()
        self.dockSwatch.setWidget ( self.swatchParam_ctl )

        MainWindow.addDockWidget ( QtCore.Qt.DockWidgetArea(1), self.dockNodes )
        MainWindow.addDockWidget ( QtCore.Qt.DockWidgetArea(2), self.dockPreview )
        MainWindow.addDockWidget ( QtCore.Qt.DockWidgetArea(2), self.dockParam )
        MainWindow.addDockWidget ( QtCore.Qt.DockWidgetArea(2), self.dockGeom )
        MainWindow.addDockWidget ( QtCore.Qt.DockWidgetArea(1), self.dockProject )
        MainWindow.addDockWidget ( QtCore.Qt.DockWidgetArea(2), self.dockSwatch )
        
        self.setupActions ( MainWindow )
        
        #
        # Setup Menu bar
        #
        self.menubar = QtModule.QMenuBar ( MainWindow )

        MainWindow.setMenuBar ( self.menubar )
        #
        # File menu
        #
        self.menuFile = QtModule.QMenu ( "File", self.menubar )
        
        self.menuFile.addAction ( self.actionNew )
        self.menuFile.addAction ( self.actionOpen )
        self.menuFile.addAction ( self.actionSave )
        self.menuFile.addAction ( self.actionSaveAs )
        self.menuFile.addAction ( self.actionSaveSelected )
        self.menuFile.addSeparator ()
        self.menuFile.addAction ( self.actionProjectSetup )
        self.menuFile.addSeparator ()
        self.menuFile.addAction ( self.actionImport )
        self.menuFile.addSeparator ()
        
        self.menuRecent_Projects = QtModule.QMenu ( "Recent Projects", self.menuFile )
        self.menuRecent_Networks = QtModule.QMenu ( "Recent Networks", self.menuFile )
        self.menuRecent_Projects.addSeparator ()
        self.menuRecent_Networks.addSeparator ()
        
        self.menuFile.addAction ( self.menuRecent_Projects.menuAction () )
        self.menuFile.addAction ( self.menuRecent_Networks.menuAction () )
        self.menuFile.addSeparator ()
        self.menuFile.addAction ( self.actionExit )
        
        self.menubar.addAction ( self.menuFile.menuAction () )
        #
        # Edit menu
        #
        self.menuEdit = QtModule.QMenu ( "Edit", self.menubar )
        
        #self.menuEdit.addAction ( self.actionUndo )
        #self.menuEdit.addAction ( self.actionRedo )
        #self.menuEdit.addSeparator ()
        self.menuEdit.addAction ( self.actionSelectAll )
        self.menuEdit.addAction ( self.actionSelectBelow )
        self.menuEdit.addAction ( self.actionSelectAbove )
        self.menuEdit.addSeparator ()
        self.menuEdit.addAction ( self.actionCopy )
        self.menuEdit.addAction ( self.actionCut )
        self.menuEdit.addAction ( self.actionPaste )
        self.menuEdit.addSeparator ()
        self.menuEdit.addAction ( self.actionDuplicate )
        self.menuEdit.addAction ( self.actionDuplicateWithLinks )
        self.menuEdit.addAction ( self.actionDelete )
        self.menuEdit.addSeparator ()
        self.menuEdit.addAction ( self.actionRendererOptions )
        self.menuEdit.addAction ( self.actionSettings )
        
        self.menubar.addAction ( self.menuEdit.menuAction () )
        #
        # Command menu
        #
        self.menuCommand = QtModule.QMenu ( "Command", self.menubar)
        
        #self.menuCreateNode = QtModule.QMenu ( "Create Node", self.menuCommand )
        #self.menuCreateNode.addSeparator ()
        
        #self.menuCommand.addAction ( self.menuCreateNode.menuAction () )
        self.menuCommand.addAction ( self.actionEditNode )
        self.menuCommand.addAction ( self.actionViewComputedCode )
        self.menuCommand.addAction ( self.actionExportShader )
        self.menuCommand.addSeparator ()
        self.menuCommand.addAction ( self.actionCompileShader )
        self.menuCommand.addAction ( self.actionRenderPreview )
        #self.menuCommand.addAction ( self.actionShowSwatch )
        #self.menuCommand.addAction ( self.actionHideSwatch )
        
        self.menubar.addAction ( self.menuCommand.menuAction () )
        #
        # View menu
        #
        self.menuView = QtModule.QMenu ( "View", self.menubar )
        
        self.menuView.addAction ( self.actionShowGrid )
        self.menuView.addAction ( self.actionSnapGrid )
        #self.menuView.addAction ( self.actionReverseFlow )
        self.menuView.addAction ( self.actionStraightLinks )
        self.menuView.addSeparator ()
        self.menuView.addAction ( self.actionFitAll )
        self.menuView.addAction ( self.actionFitSelected )
        self.menuView.addAction ( self.actionZoomReset )
        
        self.menubar.addAction ( self.menuView.menuAction () )
        #
        # Window menu
        #
        self.menuWindow = QtModule.QMenu ( "Window", self.menubar )
        
        self.menuWindow.addAction ( self.actionShowToolbar )
        self.menuWindow.addAction ( self.actionShowNodes )
        self.menuWindow.addAction ( self.actionShowParameters )
        self.menuWindow.addAction ( self.actionShowPreview )
        self.menuWindow.addAction ( self.actionShowGeometry )
        #self.menuWindow.addSeparator ()
        #self.menuWindow.addAction ( self.actionNewParamView )
        #self.menuWindow.addAction ( self.actionNewImageView )
        
        self.menubar.addAction ( self.menuWindow.menuAction () )
        #
        # Help menu
        #
        self.menuHelp = QtModule.QMenu ( "Help", self.menubar )
        
        self.menuHelp.addAction ( self.actionAbout )
        self.menuHelp.addAction ( self.actionHelp )
        
        self.menubar.addAction ( self.menuHelp.menuAction () )
        #
        # Setup Toolbar
        #
        self.toolBar = QtModule.QToolBar ( "ToolBar", MainWindow )
        self.toolBar.setToolTip ( "Enter to Help Mode" )
        self.toolBar.setMinimumSize ( QtCore.QSize ( 0, 0 ) )
        self.toolBar.setBaseSize ( QtCore.QSize ( 0, 0 ) )
        self.toolBar.setAllowedAreas ( QtCore.Qt.LeftToolBarArea | QtCore.Qt.TopToolBarArea )
        self.toolBar.setIconSize ( QtCore.QSize ( 24, 24 ) )

        MainWindow.addToolBar ( QtCore.Qt.TopToolBarArea, self.toolBar )
        
        self.toolBar.addAction ( self.actionNew )
        self.toolBar.addAction ( self.actionOpen )
        self.toolBar.addAction ( self.actionSave )
        self.toolBar.addSeparator ()
        self.toolBar.addAction ( self.actionCopy )
        self.toolBar.addAction ( self.actionCut )
        self.toolBar.addAction ( self.actionPaste )
        self.toolBar.addAction ( self.actionDelete )
        self.toolBar.addSeparator ()
        self.toolBar.addAction ( self.actionFitAll )
        self.toolBar.addAction ( self.actionFitSelected )
        self.toolBar.addAction ( self.actionZoomReset )
        self.toolBar.addAction ( self.actionShowGrid )
        self.toolBar.addAction ( self.actionSnapGrid )
        self.toolBar.addAction ( self.actionStraightLinks )
        #self.toolBar.addAction ( self.actionReverseFlow )
        
        #
        # setup WhatsThis help action
        #
        self.actionHelpMode = QtModule.QWhatsThis.createAction ( )
        self.actionHelpMode.setToolTip ( 'Enter "WhatsThis" help mode' )
        self.menuHelp.addAction ( self.actionHelpMode )
        self.toolBar.addSeparator()
        self.toolBar.addAction ( self.actionHelpMode )

        QtCore.QMetaObject.connectSlotsByName ( MainWindow )
    
    def triggered ( self, action, command ) :
        #
        if usePyQt4 :
            QtCore.QObject.connect( action, QtCore.SIGNAL( "triggered()" ),  command )
        else :
            action.triggered.connect( command  )
            
    def toggled ( self, action, command ) :
        #
        if usePyQt4 :
            QtCore.QObject.connect( action, QtCore.SIGNAL( "toggled(bool)" ),  command )
        else :
            action.toggled.connect( command  )		

    def setupActions ( self, MainWindow ) :
        #
        # File Menu actions
        #
        self.actionNew = QtModule.QAction ( "&New", MainWindow )
        icon = QtGui.QIcon ()
        icon.addPixmap ( QtGui.QPixmap ( ":/file_icons/resources/new.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionNew.setIcon ( icon )
        self.actionNew.setToolTip ( "New Project" )
        self.actionNew.setStatusTip ( "Create a new project" )
        self.actionNew.setWhatsThis ( "Click this option to create a new project" )
        self.actionNew.setShortcut ( "Ctrl+N" )
        self.triggered ( self.actionNew, MainWindow.onNew )

        self.actionOpen = QtModule.QAction ( "&Open", MainWindow )
        icon1 = QtGui.QIcon ()
        icon1.addPixmap ( QtGui.QPixmap ( ":/file_icons/resources/open.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionOpen.setIcon ( icon1 )
        self.actionOpen.setStatusTip ( "Open existing project" )
        self.actionOpen.setShortcut ( "Ctrl+O" )
        self.triggered ( self.actionOpen, MainWindow.onOpen )
        
        self.actionSave = QtModule.QAction ( "&Save", MainWindow )
        icon2 = QtGui.QIcon ()
        icon2.addPixmap ( QtGui.QPixmap ( ":/file_icons/resources/save.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionSave.setIcon ( icon2 )
        self.actionSave.setShortcut ( "Ctrl+S" )
        self.triggered ( self.actionSave, MainWindow.onSave )
        
        self.actionSaveAs = QtModule.QAction ( "Save As ...", MainWindow )
        self.triggered ( self.actionSaveAs, MainWindow.onSaveAs )
        
        self.actionSaveSelected = QtModule.QAction ( "Save Selected As ...", MainWindow )
        self.actionSaveSelected.setToolTip ( "Save selected nodes" )
        self.actionSaveSelected.setEnabled ( False )
        self.triggered ( self.actionSaveSelected, MainWindow.onSaveSelected )
        
        self.actionProjectSetup = QtModule.QAction ( "Project Setup ...", MainWindow )
        self.triggered ( self.actionProjectSetup, MainWindow.onProjectSetup )
        
        self.actionImport = QtModule.QAction (  "Import", MainWindow )
        self.triggered ( self.actionImport, MainWindow.onImport )
        
        self.actionExit = QtModule.QAction ( "Quit", MainWindow )
        self.actionExit.setShortcut ( "Ctrl+Q" )
        self.triggered ( self.actionExit, MainWindow.close )
        #
        # Edit Menu actions
        #
        
        # Undo/Redo
        self.actionUndo = QtModule.QAction ( "Undo", MainWindow )
        self.actionUndo.setEnabled ( False )
        icon6 = QtGui.QIcon ()
        icon6.addPixmap ( QtGui.QPixmap ( ":/edit_icons/resources/undo.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionUndo.setIcon ( icon6 )
        
        self.actionRedo = QtModule.QAction ( "Redo", MainWindow )
        self.actionRedo.setEnabled ( False )
        icon7 = QtGui.QIcon ()
        icon7.addPixmap ( QtGui.QPixmap ( ":/edit_icons/resources/redo.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionRedo.setIcon ( icon7 )
        # Select
        self.actionSelectAll = QtModule.QAction ( "Select All", MainWindow )
        self.actionSelectAll.setShortcut ( "Ctrl+A" )
        self.triggered ( self.actionSelectAll, MainWindow.onSelectAll )
        
        self.actionSelectBelow = QtModule.QAction ( "Select below", MainWindow )
        self.actionSelectBelow.setToolTip ( "Select hierarchy below" )
        self.actionSelectBelow.setShortcut ( "Ctrl+Down" )
        self.triggered ( self.actionSelectBelow, MainWindow.onSelectBelow )
        
        self.actionSelectAbove = QtModule.QAction ( "Select above", MainWindow )
        self.actionSelectAbove.setToolTip ( "Select hierarchy above" )
        self.actionSelectAbove.setShortcut ( "Ctrl+Up" )
        self.triggered ( self.actionSelectAbove, MainWindow.onSelectAbove )
        # Clippboard
        self.actionCopy = QtModule.QAction ( "Copy", MainWindow )
        self.actionCopy.setShortcut ( "Ctrl+C" )
        self.actionCopy.setEnabled ( False )
        icon3 = QtGui.QIcon ()
        icon3.addPixmap ( QtGui.QPixmap ( ":/edit_icons/resources/copy.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionCopy.setIcon ( icon3 )
        self.triggered ( self.actionCopy, MainWindow.onCopy )
        
        self.actionCut = QtModule.QAction ( "Cut", MainWindow )
        self.actionCut.setShortcut ( "Ctrl+X" )
        self.actionCut.setEnabled ( False )
        icon4 = QtGui.QIcon ()
        icon4.addPixmap ( QtGui.QPixmap ( ":/edit_icons/resources/editcut1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionCut.setIcon ( icon4 )
        self.triggered ( self.actionCut, MainWindow.onCut )
        
        self.actionPaste = QtModule.QAction ( "Paste", MainWindow )
        self.actionPaste.setShortcut ( "Ctrl+V" )
        self.actionPaste.setEnabled ( False )
        icon5 = QtGui.QIcon ()
        icon5.addPixmap ( QtGui.QPixmap ( ":/edit_icons/resources/paste.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionPaste.setIcon ( icon5 )
        self.triggered ( self.actionPaste, MainWindow.onPaste )
        # Duplicate 
        self.actionDuplicate = QtModule.QAction ( "Duplicate", MainWindow )
        self.actionDuplicate.setShortcut( "Ctrl+D" )
        self.triggered ( self.actionDuplicate, MainWindow.onDuplicate )
        
        self.actionDuplicateWithLinks = QtModule.QAction ( "Duplicate with links", MainWindow )
        self.actionDuplicateWithLinks.setShortcut ( "Ctrl+Shift+D" )
        self.triggered ( self.actionDuplicateWithLinks, MainWindow.onDuplicateWithLinks )
        
        self.actionDelete = QtModule.QAction (  "Delete", MainWindow )
        self.actionDelete.setShortcut ( "Del" )
        icon9 = QtGui.QIcon()
        icon9.addPixmap ( QtGui.QPixmap ( ":/edit_icons/resources/delete.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionDelete.setIcon ( icon9 )
        self.triggered ( self.actionDelete, MainWindow.onDelete )
        # Settings
        self.actionRendererOptions = QtModule.QAction ( "Renderer ...", MainWindow )
        self.actionRendererOptions.setToolTip ( "Renderer Options" )
        self.triggered ( self.actionRendererOptions, MainWindow.onRenderSettings )
        
        self.actionSettings = QtModule.QAction ( "Settings ...", MainWindow )
        self.triggered ( self.actionSettings, MainWindow.onSettingsSetup )
        #
        # Command actions
        #
        self.actionEditNode = QtModule.QAction ( "Edit Node ...", MainWindow )
        self.actionEditNode.setShortcut ( "Ctrl+E" )
        self.actionEditNode.setEnabled ( True )
        self.triggered ( self.actionEditNode, MainWindow.onEditNode )
        
        self.actionViewComputedCode = QtModule.QAction ( "View Computed Code ...", MainWindow )
        self.actionViewComputedCode.setShortcut ( "Ctrl+Alt+V" )
        self.triggered ( self.actionViewComputedCode, MainWindow.onViewComputedCode )
        
        self.actionExportShader = QtModule.QAction ( "Export As Shader ...", MainWindow )
        self.actionExportShader.setShortcut ( "Ctrl+T" )
        self.triggered ( self.actionExportShader, MainWindow.onExportShader )

        self.actionCompileShader = QtModule.QAction ( "Compile Shader", MainWindow )
        self.actionCompileShader.setShortcut ( "Ctrl+L" )
        self.triggered ( self.actionCompileShader, MainWindow.onCompileShader )
        
        self.actionRenderPreview = QtModule.QAction ( "Render Preview", MainWindow )
        self.actionRenderPreview.setShortcut ( "Ctrl+R" )
        self.actionRenderPreview.setEnabled ( True )
        self.triggered ( self.actionRenderPreview, MainWindow.onRenderPreview )
        
        self.actionShowSwatch = QtModule.QAction ( "Show Swatch", MainWindow )
        self.actionShowSwatch.setShortcut ( "Ctrl+Shift+S" )
        self.triggered ( self.actionShowSwatch, MainWindow.onShowSwatch )

        self.actionHideSwatch = QtModule.QAction ( "Hide Swatch", MainWindow )
        self.actionHideSwatch.setShortcut ( "Ctrl+Shift+H" )
        self.triggered ( self.actionHideSwatch, MainWindow.onHideSwatch )
        #
        # View Menu actions
        #
        self.actionShowGrid = QtModule.QAction ( "Show grid", MainWindow )
        self.actionShowGrid.setToolTip ( "Show grid" )
        self.actionShowGrid.setCheckable ( True )
        icon8 = QtGui.QIcon ()
        icon8.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/grid_off.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        icon8.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/grid_on.png" ), QtGui.QIcon.Normal, QtGui.QIcon.On )
        self.actionShowGrid.setIcon ( icon8 )
        self.toggled ( self.actionShowGrid, MainWindow.onShowGrid )
        
        self.actionSnapGrid = QtModule.QAction ( "Snap To Grid", MainWindow )
        self.actionSnapGrid.setToolTip ( "Snap to grid" )
        self.actionSnapGrid.setCheckable ( True )
        icon12 = QtGui.QIcon ()
        icon12.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/snap_off.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        icon12.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/snap_on.png" ), QtGui.QIcon.Normal, QtGui.QIcon.On )
        self.actionSnapGrid.setIcon ( icon12 )
        self.toggled ( self.actionSnapGrid, MainWindow.onSnapGrid )
        
        self.actionReverseFlow = QtModule.QAction ( "Reverse Flow", MainWindow )
        self.actionReverseFlow.setCheckable ( True )
        self.actionReverseFlow.setEnabled ( False )
        icon10 = QtGui.QIcon()
        icon10.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/ledoff.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        icon10.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/ledon.png" ), QtGui.QIcon.Normal, QtGui.QIcon.On )
        self.actionReverseFlow.setIcon ( icon10 )
        self.toggled ( self.actionReverseFlow, MainWindow.onReverseFlow )
        
        self.actionStraightLinks = QtModule.QAction ( "Staright Links", MainWindow )
        self.actionStraightLinks.setToolTip ( "Draw Straight Links" )
        self.actionStraightLinks.setCheckable ( True )
        icon11 = QtGui.QIcon()
        icon11.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/straight_off.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        icon11.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/straight_on.png" ), QtGui.QIcon.Normal, QtGui.QIcon.On )
        self.actionStraightLinks.setIcon ( icon11 )
        self.toggled ( self.actionStraightLinks, MainWindow.onStraightLinks )
        # Zoom
        self.actionFitAll = QtModule.QAction ( "Fit All", MainWindow )
        self.actionFitAll.setShortcut ( "F" )
        icon13 = QtGui.QIcon ()
        icon13.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/fit_all.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionFitAll.setIcon ( icon13 )
        self.triggered ( self.actionFitAll, MainWindow.onFitAll )

        self.actionFitSelected = QtModule.QAction ( "Fit Selected", MainWindow )
        self.actionFitSelected.setShortcut ( "Shift+F" )
        icon14 = QtGui.QIcon ()
        icon14.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/fit_selected.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionFitSelected.setIcon ( icon14 )
        self.triggered ( self.actionFitSelected, MainWindow.onFitSelected )

        self.actionZoomReset = QtModule.QAction ( "Reset Zoom", MainWindow )
        self.actionZoomReset.setToolTip ( "Reset Zoom" )
        icon15 = QtGui.QIcon ()
        icon15.addPixmap ( QtGui.QPixmap ( ":/show_icons/resources/zoom_reset.png" ), QtGui.QIcon.Normal, QtGui.QIcon.Off )
        self.actionZoomReset.setIcon ( icon15 )
        self.triggered ( self.actionZoomReset, MainWindow.onZoomReset )
        #
        # Window Menu actions
        #
        self.actionShowToolbar = QtModule.QAction ( "Toolbar", MainWindow )
        self.actionShowToolbar.setCheckable ( True )
        self.actionShowToolbar.setChecked ( True )
        
        self.actionShowNodes = QtModule.QAction ( "Nodes Library", MainWindow )
        self.actionShowNodes.setToolTip ( "Show Nodes" )
        self.actionShowNodes.setCheckable ( True )
        self.actionShowNodes.setChecked ( True )

        self.actionShowParameters = QtModule.QAction ( "Node Parameters", MainWindow )
        self.actionShowParameters.setToolTip ( "Show Parameters" )
        self.actionShowParameters.setCheckable ( True )
        self.actionShowParameters.setChecked ( True )
        
        self.actionShowPreview = QtModule.QAction ( "Image View", MainWindow )
        self.actionShowPreview.setToolTip ( "Show Preview" )
        self.actionShowPreview.setCheckable ( True )
        self.actionShowPreview.setChecked ( True )
        
        self.actionShowGeometry = QtModule.QAction ( "Geometry View", MainWindow )
        self.actionShowGeometry.setCheckable ( True )
        self.actionShowGeometry.setChecked ( True )

        self.actionNewParamView = QtModule.QAction ( "New Parameter View", MainWindow )
        self.triggered ( self.actionNewParamView, MainWindow.onNewParamView )
        
        self.actionNewImageView = QtModule.QAction ( "New Image View", MainWindow )
        
        self.actionHelpMode = QtModule.QAction ( "Help", MainWindow )
        self.actionHelpMode.setShortcut ( "Shift+F1" )
        self.actionHelpMode.setCheckable ( True )
        #
        # Help Menu actions
        #
        self.actionAbout = QtModule.QAction ( "About", MainWindow )
        self.actionHelp = QtModule.QAction ( "Help", MainWindow )
        #
        # Misc. actions
        #
        self.actionPreviewOptions = QtModule.QAction ( "Preview ...", MainWindow )
        self.actionPreviewOptions.setToolTip ( "Preview Options" )
        

from nodeLibraryView import NodeLibraryView
from imageViewWidget import ImageViewWidget
from nodeSwatchParam import NodeSwatchParam
from nodeParamView import NodeParamView
from gfx.WorkArea import WorkArea
from geomViewWidget import GeomViewWidget
import resources_rc
