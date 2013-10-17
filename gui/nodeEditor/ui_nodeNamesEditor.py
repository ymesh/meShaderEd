# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_nodeNamesEditor.ui'
#
# Created: Tue Sep 25 14:45:48 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NodeNamesEditor(object):
    def setupUi(self, NodeNamesEditor):
        NodeNamesEditor.setObjectName(_fromUtf8("NodeNamesEditor"))
        NodeNamesEditor.resize(417, 393)
        self.verticalLayout = QtGui.QVBoxLayout(NodeNamesEditor)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.name_lineEdit = QtGui.QLineEdit(NodeNamesEditor)
        self.name_lineEdit.setObjectName(_fromUtf8("name_lineEdit"))
        self.horizontalLayout.addWidget(self.name_lineEdit)
        self.addButton = QtGui.QToolButton(NodeNamesEditor)
        self.addButton.setMinimumSize(QtCore.QSize(24, 24))
        self.addButton.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/edit_icons/resources/plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.addButton.setIcon(icon)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QToolButton(NodeNamesEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
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
        self.listWidget = QtGui.QListWidget(NodeNamesEditor)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)

        self.retranslateUi(NodeNamesEditor)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL(_fromUtf8("clicked()")), NodeNamesEditor.onAddItem)
        QtCore.QObject.connect(self.removeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), NodeNamesEditor.onRemoveItem)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), NodeNamesEditor.onSelectionChanged)
        QtCore.QObject.connect(self.name_lineEdit, QtCore.SIGNAL(_fromUtf8("editingFinished()")), NodeNamesEditor.onRenameItem)
        QtCore.QMetaObject.connectSlotsByName(NodeNamesEditor)

    def retranslateUi(self, NodeNamesEditor):
        NodeNamesEditor.setWindowTitle(QtGui.QApplication.translate("NodeNamesEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setToolTip(QtGui.QApplication.translate("NodeNamesEditor", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("NodeNamesEditor", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setToolTip(QtGui.QApplication.translate("NodeNamesEditor", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("NodeNamesEditor", "...", None, QtGui.QApplication.UnicodeUTF8))

import gui.resources_rc
