"""
 NodeEditorDialog.py

 ver. 1.0.0
 Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)

 Dialog for managing node code and parameters

"""
from core.mePyQt import Qt, QtCore, QtGui, QtXml
from core.signal import Signal

from core.meCommon import *
from global_vars import app_global_vars, DEBUG_MODE, VALID_PARAM_TYPES, VALID_RIB_NODE_TYPES
import gui.ui_settings as UI

from core.nodeNetwork import *

from nodePropertiesEditor import NodePropertiesEditor
from nodeNamesEditor import NodeNamesEditor
from nodeParamEditor import NodeParamEditor
from nodeLinkEditor import NodeLinkEditor
from nodeCodeEditor import NodeCodeEditor

from ui_nodeEditorDialog import Ui_NodeEditorDialog

IDX_INTERNALS  = 0
IDX_PARAM = 1
IDX_HANDLERS  = 2
IDX_LINKS = 3

TAB_NODE  = 0
TAB_NODE_CODE = 1
TAB_CONTROL_CODE  = 2
TAB_EVENT_CODE = 3
TAB_PARAM_CODE = 4
TAB_PARAM = 5
TAB_LINK_INFO = 6

if QtCore.QT_VERSION < 50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# NodeEditorDialog
#
class NodeEditorDialog ( QtModule.QDialog ) :
	#
	# __init__
	#
	def __init__ ( self, node = None ):
		#
		QtModule.QDialog.__init__ ( self )

		self.editNode = node

		# self.removedLinks = []

		self.nodePropertiesEditor = None
		self.nodeParamEditor = None
		self.nodeLinkEditor = None

		self.nodeCodeEditor = None
		self.controlCodeEditor = None
		self.eventCodeEditor = None
		self.paramCodeEditor = None

		#self.setEditNode ( node )
		self.buildGui ()
		self.connectSignals ()

		self.ui.btn_save.setDefault ( False )
		self.ui.btn_close.setDefault ( True )
		self.updateGui ()
	#
	# connectSignals
	#
	def connectSignals ( self ) :
		#
		if QtCore.QT_VERSION < 50000 :
			QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL ( 'selectionChanged' ), self.updateGui ) # onInputParamSelectionChanged )
			QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL ( 'selectionChanged' ), self.updateGui ) # onOutputParamSelectionChanged  )
	
			QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL ( 'addItem' ), self.onAddParam )
			QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL ( 'addItem' ), self.onAddParam )
			QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL ( 'renameItem' ), self.onRenameParam )
			QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL ( 'renameItem' ), self.onRenameParam )
			QtCore.QObject.connect ( self.ui.input_list, QtCore.SIGNAL ( 'removeItem' ), self.onRemoveParam )
			QtCore.QObject.connect ( self.ui.output_list, QtCore.SIGNAL ( 'removeItem' ), self.onRemoveParam )
	
			QtCore.QObject.connect ( self.ui.tabs_param_list, QtCore.SIGNAL ( 'currentChanged(int)' ), self.updateGui )
	
			if self.nodeParamEditor is not None :
				QtCore.QObject.connect ( self.nodeParamEditor, QtCore.SIGNAL ( 'changeParamName' ), self.onRenameParam )
				QtCore.QObject.connect ( self.nodeParamEditor, QtCore.SIGNAL ( 'changeParamLabel' ), self.onRenameParamLabel )
	
			if self.nodeCodeEditor is not None :
				QtCore.QObject.connect ( self.nodeCodeEditor.ui.textEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditCode )
	
			if self.controlCodeEditor is not None :
				QtCore.QObject.connect ( self.controlCodeEditor.ui.textEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditControlCode )
				
			if self.paramCodeEditor is not None :
				QtCore.QObject.connect ( self.paramCodeEditor.ui.textEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditParamCode )
				
			if self.eventCodeEditor is not None :
				QtCore.QObject.connect ( self.eventCodeEditor.ui.textEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditEventCode )
	
			QtCore.QObject.connect ( self.ui.internals_list, QtCore.SIGNAL ( 'addItem' ), self.onAddInternal )
			QtCore.QObject.connect ( self.ui.includes_list, QtCore.SIGNAL ( 'addItem' ), self.onAddInclude )
	
			QtCore.QObject.connect ( self.ui.internals_list, QtCore.SIGNAL ( 'renameItem' ), self.onRenameInternal )
			QtCore.QObject.connect ( self.ui.includes_list, QtCore.SIGNAL ( 'renameItem' ), self.onRenameInclude )
	
			QtCore.QObject.connect ( self.ui.internals_list, QtCore.SIGNAL ( 'removeItem' ), self.onRemoveInternal )
			QtCore.QObject.connect ( self.ui.includes_list, QtCore.SIGNAL ( 'removeItem' ), self.onRemoveInclude )
			
			QtCore.QObject.connect ( self.ui.handlers_list, QtCore.SIGNAL ( 'selectionChanged' ), self.updateGui )

	#
	# disconnectSignals
	#
	def disconnectSignals ( self ) :
		#
		if QtCore.QT_VERSION < 50000 :
			QtCore.QObject.disconnect ( self.ui.input_list, QtCore.SIGNAL ( 'selectionChanged' ), self.updateGui ) # onInputParamSelectionChanged )
			QtCore.QObject.disconnect ( self.ui.output_list, QtCore.SIGNAL ( 'selectionChanged' ), self.updateGui ) # onOutputParamSelectionChanged  )
	
			QtCore.QObject.disconnect ( self.ui.input_list, QtCore.SIGNAL ( 'addItem' ), self.onAddParam )
			QtCore.QObject.disconnect ( self.ui.output_list, QtCore.SIGNAL ( 'addItem' ), self.onAddParam )
			QtCore.QObject.disconnect ( self.ui.input_list, QtCore.SIGNAL ( 'renameItem' ), self.onRenameParam )
			QtCore.QObject.disconnect ( self.ui.output_list, QtCore.SIGNAL ( 'renameItem' ), self.onRenameParam )
			QtCore.QObject.disconnect ( self.ui.input_list, QtCore.SIGNAL ( 'removeItem' ), self.onRemoveParam )
			QtCore.QObject.disconnect ( self.ui.output_list, QtCore.SIGNAL ( 'removeItem' ), self.onRemoveParam )
	
			QtCore.QObject.disconnect ( self.ui.tabs_param_list, QtCore.SIGNAL ( "currentChanged(int)" ), self.updateGui )
	
			if self.nodeParamEditor is not None :
				QtCore.QObject.disconnect ( self.nodeParamEditor, QtCore.SIGNAL ( 'changeParamName' ), self.onRenameParam )
				QtCore.QObject.disconnect ( self.nodeParamEditor, QtCore.SIGNAL ( 'changeParamLabel' ), self.onRenameParamLabel )
	
			if self.nodeCodeEditor is not None :
				QtCore.QObject.disconnect ( self.nodeCodeEditor.ui.textEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditCode )
	
			if self.controlCodeEditor is not None :
				QtCore.QObject.disconnect ( self.controlCodeEditor.ui.textEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditControlCode)
	
			if self.paramCodeEditor is not None :
				QtCore.QObject.disconnect ( self.paramCodeEditor.ui.textEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditParamCode )
			
			if self.eventCodeEditor is not None :
				QtCore.QObject.disconnect ( self.eventCodeEditor.ui.textEdit, QtCore.SIGNAL ( 'textChanged()' ), self.onEditEventCode )
	
			QtCore.QObject.disconnect ( self.ui.internals_list, QtCore.SIGNAL ( 'addItem' ), self.onAddInternal )
			QtCore.QObject.disconnect ( self.ui.includes_list, QtCore.SIGNAL ( 'addItem' ), self.onAddInclude )
	
			QtCore.QObject.disconnect ( self.ui.internals_list, QtCore.SIGNAL ( 'renameItem' ), self.onRenameInternal )
			QtCore.QObject.disconnect ( self.ui.includes_list, QtCore.SIGNAL ( 'renameItem' ), self.onRenameInclude )
	
			QtCore.QObject.disconnect ( self.ui.internals_list, QtCore.SIGNAL ( 'removeItem' ), self.onRemoveInternal )
			QtCore.QObject.disconnect ( self.ui.includes_list, QtCore.SIGNAL ( 'removeItem' ), self.onRemoveInclude )
			
			QtCore.QObject.disconnect ( self.ui.handlers_list, QtCore.SIGNAL ( 'selectionChanged' ), self.updateGui )

	#
	# setEditNode
	#
	def setEditNode ( self, editNode ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog: setEditNode'
		self.editNode = editNode
	#
	#  buildGui
	#
	def buildGui ( self ) :
		# build the gui created with QtDesigner
		self.ui = Ui_NodeEditorDialog ()
		self.ui.setupUi ( self )

		if self.editNode is not None :
			#
			self.setWindowTitle ( 'NodeEditor: %s (%s)' % ( self.editNode.label, self.editNode.name ) )
			
			linkedFont = QtGui.QFont ()
			linkedFont.setItalic ( True )
			linkedBrush = QtGui.QBrush ()
			linkedBrush.setColor ( QtCore.Qt.blue )
			
			# setup loacal variables list
			for name in self.editNode.internals :
				item = QtModule.QListWidgetItem ( name )
				self.ui.internals_list.ui.listWidget.addItem ( item )
			
			# setup includes list
			for name in self.editNode.includes :
				item = QtModule.QListWidgetItem ( name )
				self.ui.includes_list.ui.listWidget.addItem ( item )
			
			# setup input params list
			for param in self.editNode.inputParams :
				item = QtModule.QListWidgetItem ( param.name )
				if self.editNode.isInputParamLinked ( param ) :
					item.setFont ( linkedFont )
					item.setForeground ( linkedBrush )
				self.ui.input_list.ui.listWidget.addItem ( item )
	
			# setup output params list
			for param in self.editNode.outputParams :
				item = QtModule.QListWidgetItem ( param.name )
				if self.editNode.isOutputParamLinked ( param ) :
					item.setFont ( linkedFont )
					item.setForeground ( linkedBrush )
				self.ui.output_list.ui.listWidget.addItem ( item )
	
			# setup input links list
			for link in self.editNode.getInputLinks () :
				item = QtModule.QListWidgetItem ( 'id=%d' % link.id  )
				item.setData ( QtCore.Qt.UserRole, QVariant ( int ( link.id ) ) )
				self.ui.input_links_listWidget.addItem ( item )
	
			# setup output links list
			for link in self.editNode.getOutputLinks () :
				item = QtModule.QListWidgetItem ( 'id=%d' % link.id  )
				item.setData ( QtCore.Qt.UserRole, QVariant ( int ( link.id ) ) )
				self.ui.output_links_listWidget.addItem ( item )
				
			# setup event handlers list
			if self.editNode.event_code :
				for handler in self.editNode.event_code.keys () :
					item = QtModule.QListWidgetItem ( handler )
					self.ui.handlers_list.ui.listWidget.addItem ( item )
	
			self.nodeCodeEditor = self.ui.node_code
			self.nodeCodeEditor.setNodeCode ( self.editNode.code, 'SL' )
			
			self.controlCodeEditor = self.ui.control_code
			self.controlCodeEditor.setNodeCode ( self.editNode.control_code, 'python' )
			
			self.eventCodeEditor = self.ui.event_code
			#self.eventCodeEditor.setNodeCode ( self.editNode.event_code, 'python' )
			
			self.paramCodeEditor = self.ui.param_code
			#self.paramCodeEditor.setNodeCode ( self.editNode.param_code, 'python' )

			
			self.nodePropertiesEditor = self.ui.node
			self.nodePropertiesEditor.setNode ( self.editNode )
			
			self.nodeParamEditor = self.ui.param
			
			self.nodeLinkEditor = self.ui.link

			self.ui.tabWidget.setCurrentIndex ( TAB_NODE_CODE )
			self.ui.toolBox.setCurrentIndex ( IDX_INTERNALS )
			self.ui.tabs_param_list.setCurrentIndex ( 0 ) # input param tab

	#
	# updateGui
	#
	def updateGui ( self ) :
		#
		if self.editNode is not None :
			if DEBUG_MODE : print '>> NodeEditorDialog::updateGui'
				
			self.disconnectSignals ()
			
			self.eventCodeEditor.setNodeCode ( None, 'python' )
			self.paramCodeEditor.setNodeCode ( None, 'python' )
			
			idx = self.ui.toolBox.currentIndex ()
			
			if idx == IDX_PARAM :
				# Parameters
				tab_idx = self.ui.tabs_param_list.currentIndex ()
				param = None

				if tab_idx == 0 :
					# input parameters
					list_item = self.ui.input_list.ui.listWidget.currentItem ()

					if list_item is not None :
						param = self.editNode.getInputParamByName ( str ( list_item.text () ) )

				elif tab_idx == 1 :
					# output parametrs
					list_item = self.ui.output_list.ui.listWidget.currentItem ()

					if list_item is not None :
						param = self.editNode.getOutputParamByName ( str ( list_item.text () ) )

				self.nodeParamEditor.setParam ( param )
				if param is not None and param.type == 'control' :
					self.paramCodeEditor.setNodeCode ( param.code, 'python' )
					#print '*** set (%s).param.code :' % param.label
					#print param.code

			elif idx == IDX_HANDLERS :
				handler_item = self.ui.handlers_list.ui.listWidget.currentItem ()
				if handler_item is not None :
					handler = str ( handler_item.text () )
					handler_code = self.editNode.event_code [ handler ]
					self.eventCodeEditor.setNodeCode ( handler_code, 'python' )
				#else :
				#  print '** no selection in handlers_list'

			elif idx == IDX_LINKS :
				inputLinkSelected = False
				link_id = None
				tab_idx = self.ui.tabs_links_list.currentIndex ()

				if tab_idx == 0 :
					# input links
					inputLinkSelected = True
					links_item = self.ui.input_links_listWidget.currentItem ()
					if links_item is not None : ( link_id, ok ) = links_item.data ( QtCore.Qt.UserRole ).toInt ()

				else :
					# output links
					links_item = self.ui.output_links_listWidget.currentItem ()
					if links_item is not None : ( link_id, ok ) = links_item.data ( QtCore.Qt.UserRole ).toInt ()

				if link_id is not None :
					link = None

					if inputLinkSelected : link = self.editNode.getInputLinkByID ( link_id )
					else                 : link = self.editNode.getOutputLinkByID ( link_id )

					if link is not None :
						( srcNode, srcParam ) = link.getSrc ()
						( dstNode, dstParam ) = link.getDst ()
						self.nodeLinkEditor.ui.src_node_lineEdit.setText ( srcNode.label )
						self.nodeLinkEditor.ui.src_param_lineEdit.setText ( srcParam.label )
						self.nodeLinkEditor.ui.src_id_lineEdit.setText ( str ( srcNode.id ) )
						self.nodeLinkEditor.ui.dst_node_lineEdit.setText ( dstNode.label )
						self.nodeLinkEditor.ui.dst_param_lineEdit.setText ( dstParam.label )
						self.nodeLinkEditor.ui.dst_id_lineEdit.setText ( str ( dstNode.id ) )
			self.connectSignals ()
	#
	# onToolBoxIndexChanged
	#
	def onToolBoxIndexChanged ( self, idx ) :
		if DEBUG_MODE : print '>> NodeEditorDialog::onToolBoxIndexChanged (idx = %d)' % idx
		#
		#self.disconnectSignals ()

		if idx == IDX_PARAM :
			# Input, Output Parameters
			self.ui.tabWidget.setCurrentIndex ( TAB_PARAM )

		elif idx == IDX_LINKS :
			# Input, Output Links
			self.ui.tabWidget.setCurrentIndex ( TAB_LINK_INFO )

		elif idx == IDX_INTERNALS :
			# Includes, Local Names, Code
			self.ui.tabWidget.setCurrentIndex ( TAB_NODE_CODE )
			
		elif idx == IDX_HANDLERS :
			# Event Handlers code
			self.ui.tabWidget.setCurrentIndex ( TAB_EVENT_CODE )

		#self.connectSignals ()
		self.updateGui ()
	#
	# onInputParamSelectionChanged
	#
	def onInputParamSelectionChanged ( self, paramName ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onInputParamSelectionChanged (%s)' % paramName
		param = self.editNode.getInputParamByName ( str ( paramName ) )
		self.nodeParamEditor.setParam ( param )
	#
	# onOutputParamSelectionChanged
	#
	def onOutputParamSelectionChanged ( self, paramName ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onOutputParamSelectionChanged (%s)' % paramName
		param = self.editNode.getOutputParamByName ( str ( paramName ) )
		self.nodeParamEditor.setParam ( param )
	#
	# onCodeListIndexChanged
	#
	def onCodeListIndexChanged ( self, idx ) :
		# if DEBUG_MODE : print '>> NodeEditorDialog: onCodeListIndexChanged idx = %d' % idx
		self.updateGui ()
	#
	# onRemoveInternal
	#
	def onRemoveInternal ( self, internal ) :
		#
		internalsListWidget = self.ui.internals_list.ui.listWidget
		self.editNode.internals.remove ( internal )
		item = internalsListWidget.currentItem ()
		internalsListWidget.takeItem ( internalsListWidget.currentRow () )
		internalsListWidget.removeItemWidget ( item )
		internalsListWidget.clearSelection ()
		internalsListWidget.setCurrentItem ( None )
	#
	# onRemoveInclude
	#
	def onRemoveInclude ( self, include ) :
		#
		includesListWidget = self.ui.includes_list.ui.listWidget
		self.editNode.includes.remove ( include )
		item = includesListWidget.currentItem()
		includesListWidget.takeItem ( includesListWidget.currentRow () )
		includesListWidget.removeItemWidget ( item )
		includesListWidget.clearSelection ()
		includesListWidget.setCurrentItem ( None )
	#
	# onRemoveParam
	#
	def onRemoveParam ( self, paramName ) :
		#
		isInputParam = False
		tab_idx = self.ui.tabs_param_list.currentIndex ()
		if tab_idx == 0 : isInputParam = True
		param = None
		paramList = None
		linkList = None

		if isInputParam :
			param = self.editNode.getInputParamByName ( paramName )
			paramList = self.ui.input_list
			linkList = self.ui.input_links_listWidget
		else :
			param = self.editNode.getOutputParamByName ( paramName )
			paramList = self.ui.output_list
			linkList = self.ui.output_links_listWidget

		removedLinks = self.editNode.removeParam ( param )

		# remove item from links list and node network
		for link in removedLinks :
			item_name = 'id=%d' % link.id
			item = linkList.findItems ( item_name, QtCore.Qt.MatchExactly )[0]
			linkList.takeItem ( linkList.row ( item ) )
			link.nodenet.removeLink ( link )

		# remove item from param list
		item = paramList.ui.listWidget.currentItem ()
		paramList.ui.listWidget.takeItem ( paramList.ui.listWidget.currentRow () )
		paramList.ui.listWidget.removeItemWidget ( item )
		paramList.ui.listWidget.clearSelection ()
		paramList.ui.listWidget.setCurrentItem ( None )

		# remove item from code (invalidate code)
		pass
	#
	# onRenameInternal
	#
	def onRenameInternal ( self, oldName, newName ) :
		#
		internalsListWidget = self.ui.internals_list.ui.listWidget
		from core.meCommon import getUniqueName
		idx = self.editNode.internals.index ( oldName )
		newName = getUniqueName ( newName, self.editNode.internals )
		self.editNode.internals [ idx ] = newName

		item = internalsListWidget.findItems ( oldName, QtCore.Qt.MatchExactly )[0]
		item.setText ( newName )
		self.ui.internals_list.setName ( newName )
		internalsListWidget.clearSelection ()
		internalsListWidget.setCurrentItem ( item )
	#
	# onRenameInclude
	#
	def onRenameInclude ( self, oldName, newName ) :
		#
		includesListWidget = self.ui.includes_list.ui.listWidget
		from core.meCommon import getUniqueName
		idx = self.editNode.includes.index ( oldName )
		newName = getUniqueName ( newName, self.editNode.includes )
		self.editNode.includes [ idx ] = newName

		item = includesListWidget.findItems ( oldName, QtCore.Qt.MatchExactly )[0]
		item.setText ( newName )
		self.ui.includes_list.setName ( newName )
		includesListWidget.clearSelection ()
		includesListWidget.setCurrentItem ( item )
	#
	# onRenameParam
	#
	def onRenameParam ( self, oldName, newName ) :
		#
		isInputParam = False
		tab_idx = self.ui.tabs_param_list.currentIndex ()
		if tab_idx == 0 : isInputParam = True
		param = None
		paramList = None
		if isInputParam :
			param = self.editNode.getInputParamByName ( oldName )
			paramList = self.ui.input_list
		else :
			param = self.editNode.getOutputParamByName ( oldName )
			paramList = self.ui.output_list

		self.editNode.renameParamName ( param, newName )

		item = paramList.ui.listWidget.findItems ( oldName, QtCore.Qt.MatchExactly )[0]
		item.setText ( param.name )
		paramList.setName ( param.name )
		paramList.ui.listWidget.clearSelection ()
		paramList.ui.listWidget.setCurrentItem ( item )
	#
	# onRenameParamLabel
	#
	def onRenameParamLabel ( self, oldName, newName ) :
		#
		param = self.nodeParamEditor.param
		self.editNode.renameParamLabel ( param, newName )
		self.nodeParamEditor.ui.label_lineEdit.setText ( param.label )
	#
	# onAddInternal
	#
	def onAddInternal ( self, newName ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onAddInternal (%s) ' % (newName)
		# name can be changed to be unique
		newName = self.editNode.addInternal ( newName )
		internalsListWidget = self.ui.internals_list.ui.listWidget
		internalsListWidget.addItem ( newName )
		internalsListWidget.setCurrentItem ( internalsListWidget.findItems ( newName, QtCore.Qt.MatchExactly )[0] )
	#
	# onAddInclude
	#
	def onAddInclude ( self, newName ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onAddInclude (%s) ' % (newName)
		# name can be changed to be unique
		newName = self.editNode.addInclude ( newName )
		includesListWidget = self.ui.includes_list.ui.listWidget
		includesListWidget.addItem ( newName )
		includesListWidget.setCurrentItem ( includesListWidget.findItems ( newName, QtCore.Qt.MatchExactly )[0] )
	#
	# onAddParam
	#
	def onAddParam ( self, newName ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onAddParam (%s) ' % (newName)
		isInputParam = False
		paramType = None
		isRibParam = ( self.editNode.type in VALID_RIB_NODE_TYPES )
		tab_idx = self.ui.tabs_param_list.currentIndex ()
		if tab_idx == 0 : isInputParam = True
		# ask user about param type
		typeDialog = QtModule.QDialog () # Qt.MSWindowsFixedSizeDialogHint
		typeDialog.setModal ( True )

		typeDialog.setWindowTitle ( 'Parameter Type' )
		typeDialog.resize (180, 100 )
		sizePolicy = QtModule.QSizePolicy ( QtModule.QSizePolicy.Fixed, QtModule.QSizePolicy.Fixed )
		sizePolicy.setHorizontalStretch ( 0 )
		sizePolicy.setVerticalStretch ( 0 )
		sizePolicy.setHeightForWidth ( typeDialog.sizePolicy().hasHeightForWidth() )
		typeDialog.setSizePolicy ( sizePolicy )
		typeDialog.setSizeGripEnabled ( False )

		typeDialog.verticalLayout = QtGui.QVBoxLayout ( typeDialog )
		typeDialog.verticalLayout.setSizeConstraint ( QtGui.QLayout.SetMinimumSize )
		typeDialog.type_comboBox = QtGui.QComboBox ( typeDialog )
		
		for label in VALID_PARAM_TYPES : typeDialog.type_comboBox.addItem ( label )
		
		typeDialog.verticalLayout.addWidget ( typeDialog.type_comboBox )

		typeDialog.btnBox = QtModule.QDialogButtonBox ( QtModule.QDialogButtonBox.Ok | QtModule.QDialogButtonBox.Cancel, parent = typeDialog )
		typeDialog.btnBox.setCenterButtons ( True )
		typeDialog.verticalLayout.addWidget ( typeDialog.btnBox )

		if QtCore.QT_VERSION < 50000 :
			QtCore.QObject.connect ( typeDialog.btnBox, QtCore.SIGNAL ( 'accepted()' ), typeDialog.accept )
			QtCore.QObject.connect ( typeDialog.btnBox, QtCore.SIGNAL ( 'rejected()' ), typeDialog.reject )
		else :
			typeDialog.btnBox,accepted.connect ( typeDialog.accept )
			typeDialog.btnBox,rejected.connect ( typeDialog.reject )

		if typeDialog.exec_() == QtModule.QDialog.Accepted  :
			paramType = str ( typeDialog.type_comboBox.currentText () )

			if DEBUG_MODE : print '>> NodeEditorDialog::onAddParam typeDialog Accepted (%s)' % paramType
			# create empty xml node parameter
			dom = QtXml.QDomDocument ( newName )
			xmlnode = dom.createElement( 'property' )

			xmlnode.setAttribute ( 'name', newName )
			xmlnode.setAttribute ( 'label', newName )
			xmlnode.setAttribute ( 'type', paramType )
			param = createParamFromXml ( xmlnode, isRibParam, isInputParam )
			item = QtModule.QListWidgetItem ( param.name )

			paramListWidget = self.ui.input_list.ui.listWidget

			if isInputParam :
				self.editNode.addInputParam ( param )
			else :
				self.editNode.addOutputParam ( param )
				paramListWidget = self.ui.output_list.ui.listWidget

			paramListWidget.addItem ( param.name )
			paramListWidget.setCurrentItem ( paramListWidget.findItems ( param.name, QtCore.Qt.MatchExactly )[0] )
			#self.nodeParamEditor.setParam ( param )
	#
	# onEditCode
	#
	def onEditCode ( self ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onEditCode'
		if self.nodeCodeEditor is not None :
			#self.nodeCodeEditor.ui.textEdit
			self.editNode.code = str ( self.nodeCodeEditor.ui.textEdit.toPlainText () )
	#
	# onEditControlCode
	#
	def onEditControlCode ( self ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onEditControlCode'
		if self.controlCodeEditor is not None :
			self.editNode.control_code = str ( self.controlCodeEditor.ui.textEdit.toPlainText () )
	#
	# onEditParamCode
	#
	def onEditParamCode ( self ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onEditParamCode'
		if self.paramCodeEditor is not None :
			param = self.nodeParamEditor.param
			if param is not None and param.type == 'control' :
				param.code = str ( self.paramCodeEditor.ui.textEdit.toPlainText () )
				#print '*** set (%s).param.code :' % param.label
				#print param.code
	#
	# onEditEventCode
	#
	def onEditEventCode ( self ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::onEditEventCode'
		if self.eventCodeEditor is not None :
			handler_item = self.ui.handlers_list.ui.listWidget.currentItem ()
			if handler_item is not None :
				handler = str ( handler_item.text () )
				self.editNode.event_code [ handler ] = str ( self.eventCodeEditor.ui.textEdit.toPlainText () )

	#
	# Ignore default Enter press event
	#
	def keyPressEvent ( self, event  ) :
		#
		#if DEBUG_MODE : print '>> NodeEditorDialog::keyPressEvent'
		if  event.key () == QtCore.Qt.Key_Enter or event.key () == QtCore.Qt.Key_Return :
			event.ignore ()
		else:
			QtModule.QDialog.keyPressEvent ( self, event )
	#
	# accept
	#
	def accept ( self ) :
		#
		if DEBUG_MODE : print '>> NodeEditorDialog::accept'
		self.done ( QtModule.QDialog.Accepted )
