# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_nodeNamesEditor.ui'
#
# Created: Sun Aug 12 18:41:43 2012
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
        NodeNamesEditor.resize(681, 393)
        self.verticalLayout = QtGui.QVBoxLayout(NodeNamesEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addButton = QtGui.QPushButton(NodeNamesEditor)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(NodeNamesEditor)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.horizontalLayout.addWidget(self.removeButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.name_label = QtGui.QLabel(NodeNamesEditor)
        self.name_label.setMinimumSize(QtCore.QSize(100, 0))
        self.name_label.setObjectName(_fromUtf8("name_label"))
        self.horizontalLayout_2.addWidget(self.name_label)
        self.name_lineEdit = QtGui.QLineEdit(NodeNamesEditor)
        self.name_lineEdit.setObjectName(_fromUtf8("name_lineEdit"))
        self.horizontalLayout_2.addWidget(self.name_lineEdit)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(NodeNamesEditor)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL(_fromUtf8("clicked()")), NodeNamesEditor.onAddItem)
        QtCore.QObject.connect(self.removeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), NodeNamesEditor.onRemoveItem)
        QtCore.QMetaObject.connectSlotsByName(NodeNamesEditor)

    def retranslateUi(self, NodeNamesEditor):
        NodeNamesEditor.setWindowTitle(QtGui.QApplication.translate("NodeNamesEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("NodeNamesEditor", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("NodeNamesEditor", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.name_label.setText(QtGui.QApplication.translate("NodeNamesEditor", "Name", None, QtGui.QApplication.UnicodeUTF8))

