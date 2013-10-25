# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/exportShader\ui_exportShaderDialog.ui'
#
# Created: Tue Oct 22 18:21:56 2013
#      by: PyQt4 UI code generator 4.10.2-snapshot-a8a14dd99d1e
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ExportShaderDialog(object):
    def setupUi(self, ExportShaderDialog):
        ExportShaderDialog.setObjectName(_fromUtf8("ExportShaderDialog"))
        ExportShaderDialog.resize(967, 735)
        self.widget = QtGui.QWidget(ExportShaderDialog)
        self.widget.setGeometry(QtCore.QRect(9, 9, 951, 721))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_6 = QtGui.QGridLayout(self.widget)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.splitter = QtGui.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.node_tabWidget = QtGui.QTabWidget(self.splitter)
        self.node_tabWidget.setObjectName(_fromUtf8("node_tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.list_nodes = QtGui.QListWidget(self.tab)
        self.list_nodes.setModelColumn(0)
        self.list_nodes.setObjectName(_fromUtf8("list_nodes"))
        self.gridLayout.addWidget(self.list_nodes, 0, 0, 1, 1)
        self.node_tabWidget.addTab(self.tab, _fromUtf8(""))
        self.params_tabWidget = QtGui.QTabWidget(self.splitter)
        self.params_tabWidget.setObjectName(_fromUtf8("params_tabWidget"))
        self.tab_inputs = QtGui.QWidget()
        self.tab_inputs.setObjectName(_fromUtf8("tab_inputs"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_inputs)
        self.gridLayout_2.setMargin(2)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.list_inputs = QtGui.QListWidget(self.tab_inputs)
        self.list_inputs.setObjectName(_fromUtf8("list_inputs"))
        self.gridLayout_2.addWidget(self.list_inputs, 0, 0, 1, 1)
        self.params_tabWidget.addTab(self.tab_inputs, _fromUtf8(""))
        self.tab_outputs = QtGui.QWidget()
        self.tab_outputs.setObjectName(_fromUtf8("tab_outputs"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_outputs)
        self.gridLayout_3.setMargin(2)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.list_outputs = QtGui.QListWidget(self.tab_outputs)
        self.list_outputs.setObjectName(_fromUtf8("list_outputs"))
        self.gridLayout_3.addWidget(self.list_outputs, 0, 0, 1, 1)
        self.params_tabWidget.addTab(self.tab_outputs, _fromUtf8(""))
        self.prop_tabWidget = QtGui.QTabWidget(self.splitter)
        self.prop_tabWidget.setObjectName(_fromUtf8("prop_tabWidget"))
        self.tab_prop_node = QtGui.QWidget()
        self.tab_prop_node.setObjectName(_fromUtf8("tab_prop_node"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_prop_node)
        self.gridLayout_4.setMargin(2)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.node = NodePropertiesEditor(self.tab_prop_node)
        self.node.setObjectName(_fromUtf8("node"))
        self.gridLayout_4.addWidget(self.node, 0, 0, 1, 1)
        self.prop_tabWidget.addTab(self.tab_prop_node, _fromUtf8(""))
        self.tab_prop_param = QtGui.QWidget()
        self.tab_prop_param.setObjectName(_fromUtf8("tab_prop_param"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab_prop_param)
        self.gridLayout_5.setMargin(2)
        self.gridLayout_5.setSpacing(2)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.param = NodeParamEditor(self.tab_prop_param)
        self.param.setObjectName(_fromUtf8("param"))
        self.gridLayout_5.addWidget(self.param, 0, 0, 1, 1)
        self.prop_tabWidget.addTab(self.tab_prop_param, _fromUtf8(""))
        self.gridLayout_6.addWidget(self.splitter, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chk_save_changes = QtGui.QCheckBox(self.widget)
        self.chk_save_changes.setChecked(True)
        self.chk_save_changes.setObjectName(_fromUtf8("chk_save_changes"))
        self.horizontalLayout.addWidget(self.chk_save_changes)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_view = QtGui.QPushButton(self.widget)
        self.btn_view.setObjectName(_fromUtf8("btn_view"))
        self.horizontalLayout.addWidget(self.btn_view)
        self.btn_export = QtGui.QPushButton(self.widget)
        self.btn_export.setObjectName(_fromUtf8("btn_export"))
        self.horizontalLayout.addWidget(self.btn_export)
        self.btn_close = QtGui.QPushButton(self.widget)
        self.btn_close.setDefault(False)
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.horizontalLayout.addWidget(self.btn_close)
        self.gridLayout_6.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout_6.setRowStretch(0, 1)

        self.retranslateUi(ExportShaderDialog)
        self.node_tabWidget.setCurrentIndex(0)
        self.params_tabWidget.setCurrentIndex(0)
        self.prop_tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.btn_export, QtCore.SIGNAL(_fromUtf8("clicked()")), ExportShaderDialog.onExport)
        QtCore.QObject.connect(self.btn_close, QtCore.SIGNAL(_fromUtf8("clicked()")), ExportShaderDialog.reject)
        QtCore.QObject.connect(self.btn_view, QtCore.SIGNAL(_fromUtf8("clicked()")), ExportShaderDialog.onViewCode)
        QtCore.QMetaObject.connectSlotsByName(ExportShaderDialog)

    def retranslateUi(self, ExportShaderDialog):
        ExportShaderDialog.setWindowTitle(_translate("ExportShaderDialog", "ExportShader", None))
        self.node_tabWidget.setTabText(self.node_tabWidget.indexOf(self.tab), _translate("ExportShaderDialog", "Nodes", None))
        self.params_tabWidget.setTabText(self.params_tabWidget.indexOf(self.tab_inputs), _translate("ExportShaderDialog", "Inputs", None))
        self.params_tabWidget.setTabText(self.params_tabWidget.indexOf(self.tab_outputs), _translate("ExportShaderDialog", "Outputs", None))
        self.prop_tabWidget.setTabText(self.prop_tabWidget.indexOf(self.tab_prop_node), _translate("ExportShaderDialog", "Node", None))
        self.prop_tabWidget.setTabText(self.prop_tabWidget.indexOf(self.tab_prop_param), _translate("ExportShaderDialog", "Parameter", None))
        self.chk_save_changes.setText(_translate("ExportShaderDialog", "Save changes", None))
        self.btn_view.setText(_translate("ExportShaderDialog", "View Code ...", None))
        self.btn_export.setText(_translate("ExportShaderDialog", "Export ...", None))
        self.btn_close.setText(_translate("ExportShaderDialog", "Close", None))

from gui.nodeEditor.nodeParamEditor import NodeParamEditor
from gui.nodeEditor.nodePropertiesEditor import NodePropertiesEditor
