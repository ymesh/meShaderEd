# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_nodeList.ui'
#
# Created: Thu May 17 23:20:55 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_nodeList(object):
    def setupUi(self, nodeList):
        nodeList.setObjectName(_fromUtf8("nodeList"))
        nodeList.resize(374, 699)
        self.verticalLayout_2 = QtGui.QVBoxLayout(nodeList)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setMargin(2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(nodeList)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeView = NodeTreeView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setSortingEnabled(False)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeView.header().setVisible(False)
        self.groupBox = QtGui.QGroupBox(self.splitter)
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.infoText = QtGui.QTextEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.infoText.sizePolicy().hasHeightForWidth())
        self.infoText.setSizePolicy(sizePolicy)
        self.infoText.setFrameShape(QtGui.QFrame.HLine)
        self.infoText.setFrameShadow(QtGui.QFrame.Raised)
        self.infoText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.infoText.setObjectName(_fromUtf8("infoText"))
        self.verticalLayout.addWidget(self.infoText)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(nodeList)
        QtCore.QMetaObject.connectSlotsByName(nodeList)

    def retranslateUi(self, nodeList):
        nodeList.setWindowTitle(QtGui.QApplication.translate("nodeList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("nodeList", "Description", None, QtGui.QApplication.UnicodeUTF8))

from nodeTreeView import NodeTreeView
