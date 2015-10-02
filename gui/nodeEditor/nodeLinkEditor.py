"""

	nodeLinkEditor.py

	ver. 1.0.0
	Author: Yuri Meshalkin (aka mesh) (yuri.meshalkin@gmail.com)

	Dialog for managing node links

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

from core.meCommon import *
from global_vars import app_global_vars

import gui.ui_settings as UI

from core.node import Node

from ui_nodeLinkEditor import Ui_NodeLinkEditor

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# NodeLinkEditor
#
class NodeLinkEditor ( QtModule.QWidget ) :
	#
	# __init__
	#
	def __init__ ( self, parent ) :
		#
		QtModule.QWidget.__init__ ( self )

		self.buildGui ()
	#
	# buildGui
	#
	def buildGui ( self ) :
		# build the gui created with QtDesigner
		self.ui = Ui_NodeLinkEditor ()
		self.ui.setupUi ( self )
	#
	# connectSignals
	#
	def connectSignals ( self ) :
		# QtCore.QObject.
		pass
		"""
		self.connect ( self.ui.name_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrName )
		self.connect ( self.ui.label_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrLabel )
		self.connect ( self.ui.master_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrMaster )
		self.connect ( self.ui.author_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrAuthor )
		self.connect ( self.ui.icon_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrIcon )
		self.connect ( self.ui.type_comboBox, QtCore.SIGNAL( 'activated(int)' ), self.onEditNodeType )
		self.connect ( self.ui.help_plainTextEdit, QtCore.SIGNAL( 'textChanged()' ), self.onEditNodeTxtAttr )
		"""
	#
	# disconnectSignals
	#
	def disconnectSignals ( self ) :
		#
		pass
		"""
		if self.editNode is not None :
			self.disconnect ( self.ui.name_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrName )
			self.disconnect ( self.ui.label_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrLabel )
			self.disconnect ( self.ui.master_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrMaster )
			self.disconnect ( self.ui.author_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrAuthor )
			self.disconnect ( self.ui.icon_lineEdit, QtCore.SIGNAL( 'editingFinished()' ), self.onEditNodeStrAttrIcon )
			self.disconnect ( self.ui.type_comboBox, QtCore.SIGNAL( 'activated(int)' ), self.onEditNodeType )
			self.disconnect ( self.ui.help_plainTextEdit, QtCore.SIGNAL( 'textChanged()' ), self.onEditNodeTxtAttr )
		"""