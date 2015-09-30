"""

 meRendererSetup.py

 ver. 2.0.0
 7/6/2014 6:27:40 PM
 Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)
 
 Dialog for managing renderer presets
 
 Presets are stored in xml file 

"""
from core.mePyQt import QtCore, QtGui, QtXml

from global_vars import app_global_vars, DEBUG_MODE

from ui_meRendererSetup import Ui_meRendererSetup

if QtCore.QT_VERSION < 0x50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
	
#
# meRendererSetup
#
class meRendererSetup ( QtModule.QDialog ) :
	#
	# Define signals for PyQt5
	#
	if QtCore.QT_VERSION >= 0x50000 :
		presetChanged = QtCore.pyqtSignal ()
		savePreset = QtCore.pyqtSignal ()
	#
	# __init__
	#
	def __init__ ( self, rendererPreset ) :
		#
		QtModule.QDialog.__init__ ( self )

		self.rendererPreset = rendererPreset
		self.labelsReady = False
		self.buildGui ()
	#
	# buildGui
	#
	def buildGui ( self ) :
		# build the gui created with QtDesigner
		import sys
		self.ui = Ui_meRendererSetup ()
		self.ui.setupUi ( self )
		
		font = QtGui.QFont ()
		if ( sys.platform == 'win32' ) :
			# Runing on windows, override font sizes from Designer to default 
			font.setPointSize ( 8 )
		else :
			font.setPointSize ( 10 )
		self.ui.labelPreset.setFont ( font )
		self.ui.listPreset.setFont ( font )
		self.ui.newButton.setFont ( font )
		self.ui.deleteButton.setFont ( font )
		self.ui.cancelButton.setFont ( font )
		self.ui.okButton.setFont ( font )
		self.ui.saveButton.setFont ( font )
		self.ui.tabs.setFont ( font )
		self.ui.labelName.setFont ( font )
		self.ui.labelCmd.setFont ( font )
		self.ui.labelFlags.setFont ( font )
		self.ui.labelCompiler.setFont ( font )
		self.ui.labelShaderInfo.setFont ( font )
		self.ui.labelDefines.setFont ( font )
		self.ui.labelShaderExt.setFont ( font )
		self.ui.labelShaderExt.setFont ( font )
		self.ui.labelTexMake.setFont ( font )
		self.ui.labelTexInfo.setFont ( font )
		self.ui.labelTexViewer.setFont ( font )
		self.ui.labelTexExt.setFont ( font )

		self.labelsReady = False

		for label in self.rendererPreset.getPresetNames () :
			self.ui.listPreset.addItem ( label )
		
		self.labelsReady = True
		
		presetName = self.rendererPreset.getCurrentPresetName ()
		idx = self.ui.listPreset.findText ( presetName ) 
		print ">> buildGui:: set current renderer to: %s (%d)" % ( presetName, idx )
		#self.ui.listPreset.setCurrentIndex ( -1 )
		self.ui.listPreset.setCurrentIndex ( idx ) 
	#
	# getDataFromGui
	# 
	def getDataFromGui ( self ) :
		# ckeck if current_renderer still exists after deleting preset
		#print ">> getDataFromGui:: current renderer to: %s" % self.rendererPreset.getCurrentPresetName() 
			
		self.rendererPreset.currentPreset.RendererName = str ( self.ui.lineCmd.text () )
		self.rendererPreset.currentPreset.RendererFlags = str ( self.ui.lineFlags.text () )
		self.rendererPreset.currentPreset.ShaderCompiler = str ( self.ui.lineCompiler.text () )
		self.rendererPreset.currentPreset.ShaderInfo = str ( self.ui.lineShaderInfo.text () )
		self.rendererPreset.currentPreset.ShaderDefines = str ( self.ui.lineDefines.text () )
		self.rendererPreset.currentPreset.ShaderExt = str ( self.ui.lineShaderExt.text () )
		self.rendererPreset.currentPreset.TextureMake = str ( self.ui.lineTexMake.text () )
		self.rendererPreset.currentPreset.TextureInfo = str ( self.ui.lineTexInfo.text () )
		self.rendererPreset.currentPreset.TextureViewer = str ( self.ui.lineTexViewer.text () )
		self.rendererPreset.currentPreset.TextureExt = str ( self.ui.lineTexExt.text () )
	#
	# onIndexChanged
	#    
	def onIndexChanged ( self, name ) : 
		if DEBUG_MODE : print ">> onIndexChanged:: nam = %s self.labelsReady == %d" % ( name, self.labelsReady )
		#if DEBUG_MODE : print self.ui.listPreset.currentText ()
		name = self.ui.listPreset.currentText ()
		if ( self.labelsReady and name != '' ) :
			# change current renderer
			self.rendererPreset.setCurrentPresetByName ( str ( name ) )
		self.updateGui ()
	#
	# updateGui
	#  
	def updateGui ( self ) :
		# redraw gui elements
		#print ">> updateGui:: current renderer: %s" % self.rendererPreset.getCurrentPresetName() 
		if len ( self.rendererPreset.presetsList ) > 0 :
			if self.rendererPreset.currentPreset is not None :
				self.ui.lineName.setText ( self.rendererPreset.getCurrentPresetName () )
				self.ui.lineCmd.setText ( self.rendererPreset.currentPreset.RendererName )
				self.ui.lineFlags.setText ( self.rendererPreset.currentPreset.RendererFlags )
				self.ui.lineCompiler.setText ( self.rendererPreset.currentPreset.ShaderCompiler )
				self.ui.lineShaderInfo.setText ( self.rendererPreset.currentPreset.ShaderInfo )
				self.ui.lineDefines.setText ( self.rendererPreset.currentPreset.ShaderDefines )
				self.ui.lineShaderExt.setText ( self.rendererPreset.currentPreset.ShaderExt )
				self.ui.lineTexMake.setText ( self.rendererPreset.currentPreset.TextureMake )
				self.ui.lineTexInfo.setText ( self.rendererPreset.currentPreset.TextureInfo )
				self.ui.lineTexViewer.setText ( self.rendererPreset.currentPreset.TextureViewer )
				self.ui.lineTexExt.setText ( self.rendererPreset.currentPreset.TextureExt )
				self.ui.deleteButton.setEnabled ( True )
				self.ui.tab1.setEnabled ( True )
				self.ui.tab2.setEnabled ( True)
				self.ui.tab3.setEnabled ( True )
		else :
			self.ui.deleteButton.setEnabled ( False )
			self.ui.tab1.setEnabled ( False )
			self.ui.tab2.setEnabled ( False )
			self.ui.tab3.setEnabled ( False )
			self.ui.lineName.clear ()
			self.ui.lineCmd.clear ()
			self.ui.lineFlags.clear ()
			self.ui.lineCompiler.clear ()
			self.ui.lineShaderInfo.clear ()
			self.ui.lineDefines.clear ()
			self.ui.lineShaderExt.clear ()
			self.ui.lineTexMake.clear ()
			self.ui.lineTexInfo.clear ()
			self.ui.lineTexViewer.clear ()
			self.ui.lineTexExt.clear ()
	#
	# onNewPreset
	#
	def onNewPreset ( self ) :
		# create new empty preset
		title = 'Untitled' 
		newLabel = title
		#self.labelsReady = False
		i = 0
		while True :
			if newLabel in self.rendererPreset.getPresetNames () :
				newLabel = title + str ( i )
				i += 1
				continue
			else :
				break;
		self.rendererPreset.addPreset ( newLabel )
		#self.labelsReady = True
		self.ui.listPreset.addItem ( newLabel ) 
		idx = self.ui.listPreset.findText ( newLabel )
		self.ui.listPreset.setCurrentIndex ( -1 )
		self.ui.listPreset.setCurrentIndex ( idx ) 
		#self.updateGui ()
	#  
	# onDeletePreset
	#  
	def onDeletePreset ( self ) :
		# delete existing preset
		if len ( self.rendererPreset.presetsList ) > 0 :
			msgBox = QtModule.QMessageBox ()
			ret = msgBox.warning ( self, 'Warning', "Do you really want to delete this preset?", 
			QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,  QtGui.QMessageBox.No )
			
			if ret ==  QtModule.QMessageBox.Yes :
				self.rendererPreset.deleteCurrentPreset ()
				i = self.ui.listPreset.currentIndex ()
				self.ui.listPreset.removeItem ( i )
				self.rendererPreset.setCurrentPresetByName ( str ( self.ui.listPreset.currentText () ) )
	#
	# onEditLabel
	#    
	def onEditLabel ( self ) :
		# edit label
		newLabel = str ( self.ui.lineName.text () )
		if ( self.rendererPreset.getCurrentPresetName () != newLabel ) :
			if newLabel not in self.rendererPreset.getPresetNames () :
				self.rendererPreset.renameCurrentPreset ( newLabel )
				# rename current preset ComboBox item to new label
				i = self.ui.listPreset.currentIndex ()
				self.ui.listPreset.setItemText ( i, newLabel )
			else :
				# this label already exists, so restore to previose
				self.ui.lineName.setText ( self.rendererPreset.getCurrentPresetName () )
	#
	# onSave
	#  
	def onSave ( self ) :
		# get data from Gui for current renderer before saving
		self.getDataFromGui ()
		if QtCore.QT_VERSION < 0x50000 :
			self.emit ( QtCore.SIGNAL ( 'presetChanged' ) )
			self.emit ( QtCore.SIGNAL ( 'savePreset' ) )
		else :
			self.presetChanged.emit ()
			self.savePreset.emit ()
		#self.done ( 0 ) 
	#
	# onSelect
	#  
	def onSelect ( self ) :
		# get data from Gui for current renderer before saving
		self.getDataFromGui ()
		if QtCore.QT_VERSION < 0x50000 :
			self.emit( QtCore.SIGNAL ( 'presetChanged' ) )
		else :
			self.presetChanged.emit ()
		self.done ( 0 ) 
