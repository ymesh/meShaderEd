# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_nodeParamEditor.ui'
#
# Created: Wed Jul 03 21:58:32 2013
#      by: PyQt4 UI code generator 4.10.2-snapshot-a8a14dd99d1e
#
# WARNING! All changes made in this file will be lost!

from core.mePyQt import QtCore, QtGui

if QtCore.QT_VERSION < 0x50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		def _fromUtf8(s):
				return s

try:
		_encoding = QtModule.QApplication.UnicodeUTF8
		def _translate(context, text, disambig):
				return QtModule.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
		def _translate(context, text, disambig):
				return QtModule.QApplication.translate(context, text, disambig)

class Ui_NodeParamEditor(object):
		def setupUi(self, NodeParamEditor):
				NodeParamEditor.setObjectName(_fromUtf8("NodeParamEditor"))
				NodeParamEditor.resize(646, 773)
				self.verticalLayout = QtModule.QVBoxLayout(NodeParamEditor)
				self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
				self.horizontalLayout_2 = QtModule.QHBoxLayout()
				self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
				self.name_label = QtModule.QLabel(NodeParamEditor)
				self.name_label.setMinimumSize(QtCore.QSize(100, 0))
				self.name_label.setObjectName(_fromUtf8("name_label"))
				self.horizontalLayout_2.addWidget(self.name_label)
				self.name_lineEdit = QtModule.QLineEdit(NodeParamEditor)
				self.name_lineEdit.setObjectName(_fromUtf8("name_lineEdit"))
				self.horizontalLayout_2.addWidget(self.name_lineEdit)
				self.horizontalLayout_2.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_2)
				self.horizontalLayout_3 = QtModule.QHBoxLayout()
				self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
				self.label_label = QtModule.QLabel(NodeParamEditor)
				self.label_label.setMinimumSize(QtCore.QSize(100, 0))
				self.label_label.setObjectName(_fromUtf8("label_label"))
				self.horizontalLayout_3.addWidget(self.label_label)
				self.label_lineEdit = QtModule.QLineEdit(NodeParamEditor)
				self.label_lineEdit.setObjectName(_fromUtf8("label_lineEdit"))
				self.horizontalLayout_3.addWidget(self.label_lineEdit)
				self.horizontalLayout_3.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_3)
				self.horizontalLayout_12 = QtModule.QHBoxLayout()
				self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
				self.enabled_label = QtModule.QLabel(NodeParamEditor)
				self.enabled_label.setMinimumSize(QtCore.QSize(100, 0))
				self.enabled_label.setObjectName(_fromUtf8("enabled_label"))
				self.horizontalLayout_12.addWidget(self.enabled_label)
				self.check_enabled = QtModule.QCheckBox(NodeParamEditor)
				self.check_enabled.setText(_fromUtf8(""))
				self.check_enabled.setObjectName(_fromUtf8("check_enabled"))
				self.horizontalLayout_12.addWidget(self.check_enabled)
				spacerItem = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_12.addItem(spacerItem)
				self.verticalLayout.addLayout(self.horizontalLayout_12)
				self.horizontalLayout_5 = QtModule.QHBoxLayout()
				self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
				self.display_label = QtModule.QLabel(NodeParamEditor)
				self.display_label.setMinimumSize(QtCore.QSize(100, 0))
				self.display_label.setObjectName(_fromUtf8("display_label"))
				self.horizontalLayout_5.addWidget(self.display_label)
				self.check_display = QtModule.QCheckBox(NodeParamEditor)
				self.check_display.setText(_fromUtf8(""))
				self.check_display.setObjectName(_fromUtf8("check_display"))
				self.horizontalLayout_5.addWidget(self.check_display)
				spacerItem1 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_5.addItem(spacerItem1)
				self.verticalLayout.addLayout(self.horizontalLayout_5)
				self.horizontalLayout_6 = QtModule.QHBoxLayout()
				self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
				self.shader_label = QtModule.QLabel(NodeParamEditor)
				self.shader_label.setMinimumSize(QtCore.QSize(100, 0))
				self.shader_label.setObjectName(_fromUtf8("shader_label"))
				self.horizontalLayout_6.addWidget(self.shader_label)
				self.check_shader = QtModule.QCheckBox(NodeParamEditor)
				self.check_shader.setText(_fromUtf8(""))
				self.check_shader.setObjectName(_fromUtf8("check_shader"))
				self.horizontalLayout_6.addWidget(self.check_shader)
				spacerItem2 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_6.addItem(spacerItem2)
				self.verticalLayout.addLayout(self.horizontalLayout_6)
				self.horizontalLayout_7 = QtModule.QHBoxLayout()
				self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
				self.type_label = QtModule.QLabel(NodeParamEditor)
				self.type_label.setMinimumSize(QtCore.QSize(100, 0))
				self.type_label.setObjectName(_fromUtf8("type_label"))
				self.horizontalLayout_7.addWidget(self.type_label)
				self.type_comboBox = QtModule.QComboBox(NodeParamEditor)
				self.type_comboBox.setMinimumSize(QtCore.QSize(100, 0))
				self.type_comboBox.setObjectName(_fromUtf8("type_comboBox"))
				self.horizontalLayout_7.addWidget(self.type_comboBox)
				spacerItem3 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_7.addItem(spacerItem3)
				self.verticalLayout.addLayout(self.horizontalLayout_7)
				self.horizontalLayout_8 = QtModule.QHBoxLayout()
				self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
				self.detail_label = QtModule.QLabel(NodeParamEditor)
				self.detail_label.setMinimumSize(QtCore.QSize(100, 0))
				self.detail_label.setObjectName(_fromUtf8("detail_label"))
				self.horizontalLayout_8.addWidget(self.detail_label)
				self.detail_comboBox = QtModule.QComboBox(NodeParamEditor)
				self.detail_comboBox.setMinimumSize(QtCore.QSize(100, 0))
				self.detail_comboBox.setObjectName(_fromUtf8("detail_comboBox"))
				self.horizontalLayout_8.addWidget(self.detail_comboBox)
				spacerItem4 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_8.addItem(spacerItem4)
				self.verticalLayout.addLayout(self.horizontalLayout_8)
				self.horizontalLayout_11 = QtModule.QHBoxLayout()
				self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
				self.provider_label_2 = QtModule.QLabel(NodeParamEditor)
				self.provider_label_2.setMinimumSize(QtCore.QSize(100, 0))
				self.provider_label_2.setObjectName(_fromUtf8("provider_label_2"))
				self.horizontalLayout_11.addWidget(self.provider_label_2)
				self.provider_comboBox = QtModule.QComboBox(NodeParamEditor)
				self.provider_comboBox.setMinimumSize(QtCore.QSize(100, 0))
				self.provider_comboBox.setObjectName(_fromUtf8("provider_comboBox"))
				self.horizontalLayout_11.addWidget(self.provider_comboBox)
				spacerItem5 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_11.addItem(spacerItem5)
				self.verticalLayout.addLayout(self.horizontalLayout_11)
				self.horizontalLayout_9 = QtModule.QHBoxLayout()
				self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
				self.subtype_label = QtModule.QLabel(NodeParamEditor)
				self.subtype_label.setMinimumSize(QtCore.QSize(100, 0))
				self.subtype_label.setObjectName(_fromUtf8("subtype_label"))
				self.horizontalLayout_9.addWidget(self.subtype_label)
				self.subtype_comboBox = QtModule.QComboBox(NodeParamEditor)
				self.subtype_comboBox.setMinimumSize(QtCore.QSize(100, 0))
				self.subtype_comboBox.setObjectName(_fromUtf8("subtype_comboBox"))
				self.horizontalLayout_9.addWidget(self.subtype_comboBox)
				spacerItem6 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_9.addItem(spacerItem6)
				self.verticalLayout.addLayout(self.horizontalLayout_9)
				self.horizontalLayout_10 = QtModule.QHBoxLayout()
				self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
				self.range_label = QtModule.QLabel(NodeParamEditor)
				self.range_label.setMinimumSize(QtCore.QSize(100, 0))
				self.range_label.setObjectName(_fromUtf8("range_label"))
				self.horizontalLayout_10.addWidget(self.range_label)
				self.range_lineEdit = QtModule.QLineEdit(NodeParamEditor)
				self.range_lineEdit.setObjectName(_fromUtf8("range_lineEdit"))
				self.horizontalLayout_10.addWidget(self.range_lineEdit)
				self.horizontalLayout_10.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_10)
				self.value_stackedWidget = QtModule.QStackedWidget(NodeParamEditor)
				self.value_stackedWidget.setObjectName(_fromUtf8("value_stackedWidget"))
				self.value_stackedWidgetPage1 = QtModule.QWidget()
				self.value_stackedWidgetPage1.setObjectName(_fromUtf8("value_stackedWidgetPage1"))
				self.value_stackedWidget.addWidget(self.value_stackedWidgetPage1)
				self.verticalLayout.addWidget(self.value_stackedWidget)
				spacerItem7 = QtModule.QSpacerItem(20, 0, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
				self.verticalLayout.addItem(spacerItem7)
				self.horizontalLayout_4 = QtModule.QHBoxLayout()
				self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
				self.descr_label = QtModule.QLabel(NodeParamEditor)
				self.descr_label.setMinimumSize(QtCore.QSize(100, 0))
				self.descr_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
				self.descr_label.setObjectName(_fromUtf8("descr_label"))
				self.horizontalLayout_4.addWidget(self.descr_label)
				self.descr_plainTextEdit = QtModule.QPlainTextEdit(NodeParamEditor)
				self.descr_plainTextEdit.setMinimumSize(QtCore.QSize(0, 60))
				self.descr_plainTextEdit.setObjectName(_fromUtf8("descr_plainTextEdit"))
				self.horizontalLayout_4.addWidget(self.descr_plainTextEdit)
				self.verticalLayout.addLayout(self.horizontalLayout_4)

				self.retranslateUi(NodeParamEditor)
				QtCore.QMetaObject.connectSlotsByName(NodeParamEditor)

		def retranslateUi(self, NodeParamEditor):
				NodeParamEditor.setWindowTitle(_translate("NodeParamEditor", "Form", None))
				self.name_label.setText(_translate("NodeParamEditor", "Name", None))
				self.label_label.setText(_translate("NodeParamEditor", "Label", None))
				self.enabled_label.setText(_translate("NodeParamEditor", "Enabled", None))
				self.display_label.setText(_translate("NodeParamEditor", "Display", None))
				self.shader_label.setText(_translate("NodeParamEditor", "Use in Shader", None))
				self.type_label.setText(_translate("NodeParamEditor", "Type", None))
				self.detail_label.setText(_translate("NodeParamEditor", "Detail", None))
				self.provider_label_2.setText(_translate("NodeParamEditor", "Provider", None))
				self.subtype_label.setText(_translate("NodeParamEditor", "GUI Subtype", None))
				self.range_label.setText(_translate("NodeParamEditor", "Range", None))
				self.descr_label.setText(_translate("NodeParamEditor", "Description", None))

