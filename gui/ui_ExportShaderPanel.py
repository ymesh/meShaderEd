# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_ExportShaderPanel.ui'
#
# Created: Mon Apr 08 03:28:47 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ExportShaderPanel(object):
    def setupUi(self, ExportShaderPanel):
        ExportShaderPanel.setObjectName(_fromUtf8("ExportShaderPanel"))
        ExportShaderPanel.resize(938, 736)
        self.verticalLayout = QtGui.QVBoxLayout(ExportShaderPanel)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(ExportShaderPanel)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.nodes_toolBox = QtGui.QToolBox(self.splitter)
        self.nodes_toolBox.setObjectName(_fromUtf8("nodes_toolBox"))
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 345, 660))
        self.page.setObjectName(_fromUtf8("page"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.page)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.listView = QtGui.QListView(self.page)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.verticalLayout_2.addWidget(self.listView)
        self.nodes_toolBox.addItem(self.page, _fromUtf8(""))
        self.params_toolBox = QtGui.QToolBox(self.splitter)
        self.params_toolBox.setObjectName(_fromUtf8("params_toolBox"))
        self.inputs = QtGui.QWidget()
        self.inputs.setGeometry(QtCore.QRect(0, 0, 346, 633))
        self.inputs.setObjectName(_fromUtf8("inputs"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.inputs)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.inputs_treeView = QtGui.QTreeView(self.inputs)
        self.inputs_treeView.setObjectName(_fromUtf8("inputs_treeView"))
        self.verticalLayout_3.addWidget(self.inputs_treeView)
        self.params_toolBox.addItem(self.inputs, _fromUtf8(""))
        self.outputs = QtGui.QWidget()
        self.outputs.setGeometry(QtCore.QRect(0, 0, 346, 633))
        self.outputs.setObjectName(_fromUtf8("outputs"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.outputs)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.outputs_treeView = QtGui.QTreeView(self.outputs)
        self.outputs_treeView.setObjectName(_fromUtf8("outputs_treeView"))
        self.verticalLayout_4.addWidget(self.outputs_treeView)
        self.params_toolBox.addItem(self.outputs, _fromUtf8(""))
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_param = QtGui.QWidget()
        self.tab_param.setObjectName(_fromUtf8("tab_param"))
        self.tabWidget.addTab(self.tab_param, _fromUtf8(""))
        self.tab_code = QtGui.QWidget()
        self.tab_code.setObjectName(_fromUtf8("tab_code"))
        self.tabWidget.addTab(self.tab_code, _fromUtf8(""))
        self.verticalLayout.addWidget(self.splitter)
        self.hl_bottom = QtGui.QHBoxLayout()
        self.hl_bottom.setObjectName(_fromUtf8("hl_bottom"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_bottom.addItem(spacerItem)
        self.btn_save = QtGui.QPushButton(ExportShaderPanel)
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        self.hl_bottom.addWidget(self.btn_save)
        self.btn_close = QtGui.QPushButton(ExportShaderPanel)
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.hl_bottom.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.hl_bottom)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(ExportShaderPanel)
        self.nodes_toolBox.setCurrentIndex(0)
        self.params_toolBox.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.btn_save, QtCore.SIGNAL(_fromUtf8("clicked()")), ExportShaderPanel.accept)
        QtCore.QObject.connect(self.btn_close, QtCore.SIGNAL(_fromUtf8("clicked()")), ExportShaderPanel.reject)
        QtCore.QMetaObject.connectSlotsByName(ExportShaderPanel)

    def retranslateUi(self, ExportShaderPanel):
        ExportShaderPanel.setWindowTitle(QtGui.QApplication.translate("ExportShaderPanel", "ExportShader", None, QtGui.QApplication.UnicodeUTF8))
        self.nodes_toolBox.setItemText(self.nodes_toolBox.indexOf(self.page), QtGui.QApplication.translate("ExportShaderPanel", "Nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.params_toolBox.setItemText(self.params_toolBox.indexOf(self.inputs), QtGui.QApplication.translate("ExportShaderPanel", "Input Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.params_toolBox.setItemText(self.params_toolBox.indexOf(self.outputs), QtGui.QApplication.translate("ExportShaderPanel", "Output Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_param), QtGui.QApplication.translate("ExportShaderPanel", "Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_code), QtGui.QApplication.translate("ExportShaderPanel", "Shader Code", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_save.setText(QtGui.QApplication.translate("ExportShaderPanel", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("ExportShaderPanel", "Close", None, QtGui.QApplication.UnicodeUTF8))

