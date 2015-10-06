"""

 nodeParamView.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui
from core.signal import Signal

from core.node import Node
from core.nodeLibrary import NodeLibrary
from gui.nodeParamList import NodeParamListTab, NodeParamList

import gui.ui_settings as UI
from global_vars import DEBUG_MODE
if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# NodeParamView
#
class NodeParamView ( QtModule.QWidget ) :
	#
	# __init__
	#
	def __init__ ( self ) :
		#
		QtModule.QWidget.__init__ ( self )
		#
		# Define signals for PyQt5
		#
		if usePySide or usePyQt5 :
			#
			self.nodeParamChangedSignal = Signal ()
			self.nodeLabelChangedSignal = Signal ()
			#
		self.gfxNode = None
		
		self.inputParamListTab = None
		self.outputParamListTab = None
		
		self.showConnected = False
		self.buildGui ()
		self.updateGui ()
		self.connectSignals ()
	#
	# setNode
	#
	def setNode ( self, gfxNode ) :
		#
		#if DEBUG_MODE : print ">> NodeParamView.setNode"
		self.disconnectParamSignals ()
		self.gfxNode = gfxNode
		self.inputParamListTab.setNode ( gfxNode )
		self.outputParamListTab.setNode ( gfxNode )
		self.nameEdit.setEnabled ( self.gfxNode is not None )
		self.updateGui ()
		self.connectParamSignals ()
	#
	# connectSignals
	#
	def connectSignals ( self ) :
		#
		if usePyQt4 :
			self.connect ( self.nameEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.nodeLabelChanged )
			self.connect ( self.showConnectButton, QtCore.SIGNAL ( 'toggled(bool)' ), self.showConnections )
		else :
			self.nameEdit.editingFinished.connect ( self.nodeLabelChanged )
			self.showConnectButton.toggled.connect ( self.showConnections )
	#
	# disconnectSignals
	#
	def disconnectSignals ( self ) :
		#
		if usePyQt4 :
			self.disconnect ( self.nameEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.nodeLabelChanged )
			self.disconnect ( self.showConnectButton, QtCore.SIGNAL ( 'toggled(bool)' ), self.showConnections )
		else :
			self.nameEdit.editingFinished.disconnect ( self.nodeLabelChanged )
			self.showConnectButton.toggled.disconnect ( self.showConnections )
	#
	# connectParamSignals
	#
	def connectParamSignals ( self ) :
		#print ">> NodeParamView.connectParamSignals"
		if self.gfxNode is not None :
			for inputParam in self.gfxNode.node.inputParams :
				if usePyQt4 :
					self.connect ( inputParam, QtCore.SIGNAL ( 'paramChangedSignal(QObject)' ), self.onParamChanged )
				else :
					inputParam.paramChangedSignal.connect ( self.onParamChanged )
			for outputParam in self.gfxNode.node.outputParams :
				if usePyQt4 :
					self.connect ( outputParam, QtCore.SIGNAL ( 'paramChangedSignal(QObject)' ), self.onParamChanged )
				else :
					outputParam.paramChangedSignal.connect ( self.onParamChanged )
	#
	# disconnectParamSignals
	#
	def disconnectParamSignals ( self ) :
		#print ">> NodeParamView.disconnectParamSignals"
		if self.gfxNode is not None :
			for inputParam in self.gfxNode.node.inputParams :
				if usePyQt4 :
					self.disconnect ( inputParam, QtCore.SIGNAL ( 'paramChangedSignal(QObject)' ), self.onParamChanged )
				else :
					inputParam.paramChangedSignal.disconnect ( self.onParamChanged )
			for outputParam in self.gfxNode.node.outputParams :
				if usePyQt4 :
					self.disconnect ( outputParam, QtCore.SIGNAL ( 'paramChangedSignal(QObject)' ), self.onParamChanged )
				else :
					outputParam.paramChangedSignal.disconnect ( self.onParamChanged )
	#
	# showConnections
	#
	def showConnections ( self, show ) :
		#
		print ">> NodeParamView.showConnections %s" % show
		self.showConnected = show
		self.inputParamListTab.showConnected = show
		self.outputParamListTab.showConnected = show
		self.inputParamListTab.updateGui ()
		self.outputParamListTab.updateGui ()
	#
	# onParamChanged
	#
	def onParamChanged ( self, param ) :
		#
		if DEBUG_MODE : print ( ">> NodeParamView.onParamChanged node = %s param = %s" % ( self.gfxNode.node.label, param.name ) )
		if usePyQt4 :
			self.emit ( QtCore.SIGNAL ( 'nodeParamChangedSignal' ), self.gfxNode, param ) # .node
		else :
			self.nodeParamChangedSignal.emit ( self.gfxNode, param ) # .node
	#
	# nodeLabelChanged
	#
	def nodeLabelChanged ( self ) :
		#
		#if DEBUG_MODE : print ">> NodeParamView.nodeLabelChanged"
		if self.gfxNode is not None :
			from core.meCommon import getParsedLabel
			newLabel = getParsedLabel ( self.nameEdit.text () )
			#if DEBUG_MODE : print "** newLabel = %s" % newLabel
			if newLabel != '' :
				# update label only if realy changed
				if newLabel != self.gfxNode.node.label :
					# rename node label if same name exists in NodeNet
					if usePyQt4 :
						self.emit ( QtCore.SIGNAL ( 'nodeLabelChangedSignal' ), self.gfxNode, newLabel )
					else :
						self.nodeLabelChangedSignal.emit ( self.gfxNode, newLabel )
					self.nameEdit.clear ()
			self.nameEdit.setText ( self.gfxNode.node.label )
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		label = QtModule.QLabel ()
		label.setMinimumSize ( QtCore.QSize ( UI.NODE_LABEL_WIDTH, UI.HEIGHT ) )
		label.setMaximumSize ( QtCore.QSize ( UI.NODE_LABEL_WIDTH, UI.HEIGHT ) )

		font = QtGui.QFont ()
		label.setFont ( font )
		#label.setAlignment(QtCore.Qt.AlignCenter)
		label.setText ( 'Label' )

		self.nameEdit = QtModule.QLineEdit ()
		self.nameEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
		self.nameEdit.setEnabled ( False )
		
		self.showConnectButton = QtModule.QToolButton ( self )
		sizePolicy = QtModule.QSizePolicy ( QtModule.QSizePolicy.Fixed, QtModule.QSizePolicy.Fixed )
		sizePolicy.setHorizontalStretch ( 20 )
		sizePolicy.setVerticalStretch ( 20 )
		sizePolicy.setHeightForWidth ( self.showConnectButton.sizePolicy().hasHeightForWidth() )
		self.showConnectButton.setSizePolicy ( sizePolicy )
		self.showConnectButton.setMaximumSize ( QtCore.QSize ( 20, 20 ) )
		icon = QtGui.QIcon ()
		icon.addPixmap ( QtGui.QPixmap ( ':/show_icons/resources/show_connect.png' ), QtGui.QIcon.Normal, QtGui.QIcon.On )
		self.showConnectButton.setIcon ( icon )
		self.showConnectButton.setAutoRaise ( False )
		self.showConnectButton.setCheckable ( True )
		self.showConnectButton.setChecked ( self.showConnected ) 
		self.showConnectButton.setToolTip ( 'Show connected parameters' )
		#self.showConnectButton.setIconSize ( QtCore.QSize ( 16, 16 ) )
		self.showConnectButton.setObjectName ( 'showConnectButton' )

		headerLayout = QtModule.QHBoxLayout ()
		headerLayout.setSpacing ( UI.SPACING )
		headerLayout.setContentsMargins ( UI.SPACING, UI.SPACING, UI.SPACING, UI.SPACING )
		headerLayout.setStretch ( 1, 1 )

		headerLayout.addWidget ( label )
		headerLayout.addWidget ( self.nameEdit )
		headerLayout.addWidget ( self.showConnectButton )

		mainLayout = QtModule.QVBoxLayout ()
		mainLayout.addLayout ( headerLayout )
		
		self.params_tabs = QtModule.QTabWidget ( self )
		
		self.inputParamListTab = NodeParamListTab ( self, self.gfxNode, isInput = True, showConnected = self.showConnected )
		self.params_tabs.addTab ( self.inputParamListTab, 'Input' )
		
		self.outputParamListTab = NodeParamListTab ( self, self.gfxNode, isInput = False, showConnected = self.showConnected )
		self.params_tabs.addTab ( self.outputParamListTab, 'Output' )
		
		self.params_tabs.setCurrentIndex ( 0 )
		
		mainLayout.addWidget ( self.params_tabs )
		
		self.setLayout ( mainLayout )
	#
	# updateGui
	#
	def updateGui ( self ) :
		#
		#if DEBUG_MODE : print '>> NodeParamView.updateGui'
			
		self.nameEdit.clear ()
		if self.gfxNode is not None :
			self.nameEdit.setText ( self.gfxNode.node.label )
		
		self.inputParamListTab.updateGui ()
		self.outputParamListTab.updateGui ()
		