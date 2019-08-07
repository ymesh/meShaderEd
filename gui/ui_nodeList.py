# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_nodeList.ui'
#
# Created: Tue Oct  9 18:01:39 2012
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

class Ui_nodeList(object):
    def setupUi(self, nodeList):
        nodeList.setObjectName(_fromUtf8("nodeList"))
        nodeList.resize(374, 699)
        self.verticalLayout_2 = QtModule.QVBoxLayout(nodeList)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins ( 2, 2, 2, 2 )
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtModule.QSplitter(nodeList)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeView = NodeTreeView(self.splitter)
        sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setSortingEnabled(False)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeView.header().setVisible(False)
        self.groupBox = QtModule.QGroupBox(self.splitter)
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtModule.QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins ( 2, 2, 2, 2 )
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.infoText = QtModule.QTextEdit(self.groupBox)
        sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.infoText.sizePolicy().hasHeightForWidth())
        self.infoText.setSizePolicy(sizePolicy)
        self.infoText.setFrameShape(QtModule.QFrame.HLine)
        self.infoText.setFrameShadow(QtModule.QFrame.Raised)
        self.infoText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.infoText.setObjectName(_fromUtf8("infoText"))
        self.verticalLayout.addWidget(self.infoText)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(nodeList)
        QtCore.QMetaObject.connectSlotsByName(nodeList)

    def retranslateUi(self, nodeList):
        nodeList.setWindowTitle(QtModule.QApplication.translate("nodeList", "Form", None))
        self.groupBox.setTitle(QtModule.QApplication.translate("nodeList", "Description", None))

from nodeTreeView import NodeTreeView
