# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_nodeCodeEditor.ui'
#
# Created: Sun Aug 12 19:45:17 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NodeCodeEditor(object):
    def setupUi(self, NodeCodeEditor):
        NodeCodeEditor.setObjectName(_fromUtf8("NodeCodeEditor"))
        NodeCodeEditor.resize(630, 499)
        self.gridLayout = QtGui.QGridLayout(NodeCodeEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(NodeCodeEditor)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)

        self.retranslateUi(NodeCodeEditor)
        QtCore.QMetaObject.connectSlotsByName(NodeCodeEditor)

    def retranslateUi(self, NodeCodeEditor):
        NodeCodeEditor.setWindowTitle(QtGui.QApplication.translate("NodeCodeEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))

