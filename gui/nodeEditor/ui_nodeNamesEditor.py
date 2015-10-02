# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_nodeNamesEditor.ui'
#
# Created: Tue Sep 25 14:45:48 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class Ui_NodeNamesEditor(object):
		def setupUi(self, NodeNamesEditor):
				NodeNamesEditor.setObjectName(_fromUtf8("NodeNamesEditor"))
				NodeNamesEditor.resize(417, 393)
				self.verticalLayout = QtModule.QVBoxLayout(NodeNamesEditor)
				self.verticalLayout.setSpacing(0)
				#if  usePyQt4 :
				self.verticalLayout.setContentsMargins ( 0, 0, 0, 0 )
				self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
				self.horizontalLayout = QtModule.QHBoxLayout()
				self.horizontalLayout.setSpacing(2)
				self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
				self.name_lineEdit = QtModule.QLineEdit(NodeNamesEditor)
				self.name_lineEdit.setObjectName(_fromUtf8("name_lineEdit"))
				self.horizontalLayout.addWidget(self.name_lineEdit)
				self.addButton = QtModule.QToolButton(NodeNamesEditor)
				self.addButton.setMinimumSize(QtCore.QSize(24, 24))
				self.addButton.setMaximumSize(QtCore.QSize(24, 24))
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/edit_icons/resources/plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
				self.addButton.setIcon(icon)
				self.addButton.setObjectName(_fromUtf8("addButton"))
				self.horizontalLayout.addWidget(self.addButton)
				self.removeButton = QtModule.QToolButton(NodeNamesEditor)
				sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Fixed, QtModule.QSizePolicy.Fixed)
				sizePolicy.setHorizontalStretch(24)
				sizePolicy.setVerticalStretch(24)
				sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
				self.removeButton.setSizePolicy(sizePolicy)
				self.removeButton.setMaximumSize(QtCore.QSize(24, 24))
				icon1 = QtGui.QIcon()
				icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/edit_icons/resources/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
				self.removeButton.setIcon(icon1)
				self.removeButton.setObjectName(_fromUtf8("removeButton"))
				self.horizontalLayout.addWidget(self.removeButton)
				self.verticalLayout.addLayout(self.horizontalLayout)
				self.listWidget = QtModule.QListWidget(NodeNamesEditor)
				self.listWidget.setAcceptDrops(True)
				self.listWidget.setDragEnabled(True)
				self.listWidget.setDragDropMode(QtModule.QAbstractItemView.InternalMove)
				self.listWidget.setObjectName(_fromUtf8("listWidget"))
				self.verticalLayout.addWidget(self.listWidget)

				self.retranslateUi(NodeNamesEditor)
				if  usePyQt4 :
					QtCore.QObject.connect(self.addButton, QtCore.SIGNAL(_fromUtf8("clicked()")), NodeNamesEditor.onAddItem)
					QtCore.QObject.connect(self.removeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), NodeNamesEditor.onRemoveItem)
					QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), NodeNamesEditor.onSelectionChanged)
					QtCore.QObject.connect(self.name_lineEdit, QtCore.SIGNAL(_fromUtf8("editingFinished()")), NodeNamesEditor.onRenameItem)
				else :
					self.addButton.clicked.connect( NodeNamesEditor.onAddItem)
					self.removeButton.clicked.connect( NodeNamesEditor.onRemoveItem)
					self.listWidget.itemSelectionChanged.connect( NodeNamesEditor.onSelectionChanged)
					self.name_lineEdit.editingFinished.connect( NodeNamesEditor.onRenameItem)
				QtCore.QMetaObject.connectSlotsByName(NodeNamesEditor)

		def retranslateUi(self, NodeNamesEditor):
				NodeNamesEditor.setWindowTitle(QtModule.QApplication.translate("NodeNamesEditor", "Form", None))
				self.addButton.setToolTip(QtModule.QApplication.translate("NodeNamesEditor", "Add", None))
				self.addButton.setText(QtModule.QApplication.translate("NodeNamesEditor", "...", None))
				self.removeButton.setToolTip(QtModule.QApplication.translate("NodeNamesEditor", "Remove", None))
				self.removeButton.setText(QtModule.QApplication.translate("NodeNamesEditor", "...", None))

import gui.resources_rc
