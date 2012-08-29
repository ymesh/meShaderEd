# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_nodeEditorWindow.ui'
#
# Created: Sun Aug 12 02:41:31 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NodeEditorWindow(object):
    def setupUi(self, NodeEditorWindow):
        NodeEditorWindow.setObjectName(_fromUtf8("NodeEditorWindow"))
        NodeEditorWindow.resize(712, 485)
        self.verticalLayout = QtGui.QVBoxLayout(NodeEditorWindow)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = NodeEditorPanel(NodeEditorWindow)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtGui.QDialogButtonBox(NodeEditorWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NodeEditorWindow)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NodeEditorWindow.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NodeEditorWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(NodeEditorWindow)

    def retranslateUi(self, NodeEditorWindow):
        NodeEditorWindow.setWindowTitle(QtGui.QApplication.translate("NodeEditorWindow", "Node Editor", None, QtGui.QApplication.UnicodeUTF8))

from NodeEditorPanel import NodeEditorPanel
