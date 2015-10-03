# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_nodeLinkEditor.ui'
#
# Created: Thu Apr 11 02:03:08 2013
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

class Ui_NodeLinkEditor(object):
		def setupUi(self, NodeLinkEditor):
				NodeLinkEditor.setObjectName(_fromUtf8("NodeLinkEditor"))
				NodeLinkEditor.resize(714, 611)
				self.verticalLayout_3 = QtModule.QVBoxLayout(NodeLinkEditor)
				self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
				self.srcGroup = QtModule.QGroupBox(NodeLinkEditor)
				self.srcGroup.setObjectName(_fromUtf8("srcGroup"))
				self.verticalLayout = QtModule.QVBoxLayout(self.srcGroup)
				self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
				self.horizontalLayout_2 = QtModule.QHBoxLayout()
				self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
				self.name_label = QtModule.QLabel(self.srcGroup)
				self.name_label.setMinimumSize(QtCore.QSize(100, 0))
				self.name_label.setObjectName(_fromUtf8("name_label"))
				self.horizontalLayout_2.addWidget(self.name_label)
				self.src_node_lineEdit = QtModule.QLineEdit(self.srcGroup)
				self.src_node_lineEdit.setEnabled(False)
				self.src_node_lineEdit.setObjectName(_fromUtf8("src_node_lineEdit"))
				self.horizontalLayout_2.addWidget(self.src_node_lineEdit)
				self.horizontalLayout_2.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_2)
				self.horizontalLayout_3 = QtModule.QHBoxLayout()
				self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
				self.label_label = QtModule.QLabel(self.srcGroup)
				self.label_label.setMinimumSize(QtCore.QSize(100, 0))
				self.label_label.setObjectName(_fromUtf8("label_label"))
				self.horizontalLayout_3.addWidget(self.label_label)
				self.src_param_lineEdit = QtModule.QLineEdit(self.srcGroup)
				self.src_param_lineEdit.setEnabled(False)
				self.src_param_lineEdit.setObjectName(_fromUtf8("src_param_lineEdit"))
				self.horizontalLayout_3.addWidget(self.src_param_lineEdit)
				self.horizontalLayout_3.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_3)
				self.horizontalLayout_4 = QtModule.QHBoxLayout()
				self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
				self.name_label_2 = QtModule.QLabel(self.srcGroup)
				self.name_label_2.setMinimumSize(QtCore.QSize(100, 0))
				self.name_label_2.setObjectName(_fromUtf8("name_label_2"))
				self.horizontalLayout_4.addWidget(self.name_label_2)
				self.src_id_lineEdit = QtModule.QLineEdit(self.srcGroup)
				self.src_id_lineEdit.setEnabled(False)
				self.src_id_lineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
				self.src_id_lineEdit.setObjectName(_fromUtf8("src_id_lineEdit"))
				self.horizontalLayout_4.addWidget(self.src_id_lineEdit)
				spacerItem = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_4.addItem(spacerItem)
				self.verticalLayout.addLayout(self.horizontalLayout_4)
				self.verticalLayout_3.addWidget(self.srcGroup)
				self.dstGroup = QtModule.QGroupBox(NodeLinkEditor)
				self.dstGroup.setObjectName(_fromUtf8("dstGroup"))
				self.verticalLayout_2 = QtModule.QVBoxLayout(self.dstGroup)
				self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
				self.horizontalLayout_6 = QtModule.QHBoxLayout()
				self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
				self.name_label_3 = QtModule.QLabel(self.dstGroup)
				self.name_label_3.setMinimumSize(QtCore.QSize(100, 0))
				self.name_label_3.setObjectName(_fromUtf8("name_label_3"))
				self.horizontalLayout_6.addWidget(self.name_label_3)
				self.dst_node_lineEdit = QtModule.QLineEdit(self.dstGroup)
				self.dst_node_lineEdit.setEnabled(False)
				self.dst_node_lineEdit.setObjectName(_fromUtf8("dst_node_lineEdit"))
				self.horizontalLayout_6.addWidget(self.dst_node_lineEdit)
				self.horizontalLayout_6.setStretch(1, 1)
				self.verticalLayout_2.addLayout(self.horizontalLayout_6)
				self.horizontalLayout_5 = QtModule.QHBoxLayout()
				self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
				self.label_label_2 = QtModule.QLabel(self.dstGroup)
				self.label_label_2.setMinimumSize(QtCore.QSize(100, 0))
				self.label_label_2.setObjectName(_fromUtf8("label_label_2"))
				self.horizontalLayout_5.addWidget(self.label_label_2)
				self.dst_param_lineEdit = QtModule.QLineEdit(self.dstGroup)
				self.dst_param_lineEdit.setEnabled(False)
				self.dst_param_lineEdit.setObjectName(_fromUtf8("dst_param_lineEdit"))
				self.horizontalLayout_5.addWidget(self.dst_param_lineEdit)
				self.horizontalLayout_5.setStretch(1, 1)
				self.verticalLayout_2.addLayout(self.horizontalLayout_5)
				self.horizontalLayout_7 = QtModule.QHBoxLayout()
				self.horizontalLayout_7.setSpacing(6)
				self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
				self.name_label_4 = QtModule.QLabel(self.dstGroup)
				self.name_label_4.setMinimumSize(QtCore.QSize(100, 0))
				self.name_label_4.setObjectName(_fromUtf8("name_label_4"))
				self.horizontalLayout_7.addWidget(self.name_label_4)
				self.dst_id_lineEdit = QtModule.QLineEdit(self.dstGroup)
				self.dst_id_lineEdit.setEnabled(False)
				self.dst_id_lineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
				self.dst_id_lineEdit.setObjectName(_fromUtf8("dst_id_lineEdit"))
				self.horizontalLayout_7.addWidget(self.dst_id_lineEdit)
				spacerItem1 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_7.addItem(spacerItem1)
				self.verticalLayout_2.addLayout(self.horizontalLayout_7)
				self.verticalLayout_3.addWidget(self.dstGroup)
				spacerItem2 = QtModule.QSpacerItem(20, 0, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
				self.verticalLayout_3.addItem(spacerItem2)

				self.retranslateUi(NodeLinkEditor)
				QtCore.QMetaObject.connectSlotsByName(NodeLinkEditor)

		def retranslateUi(self, NodeLinkEditor):
				NodeLinkEditor.setWindowTitle(QtModule.QApplication.translate("NodeLinkEditor", "NodeLinkEditor", None))
				self.srcGroup.setTitle(QtModule.QApplication.translate("NodeLinkEditor", "Source Node", None))
				self.name_label.setText(QtModule.QApplication.translate("NodeLinkEditor", "Name", None))
				self.label_label.setText(QtModule.QApplication.translate("NodeLinkEditor", "Parameter", None))
				self.name_label_2.setText(QtModule.QApplication.translate("NodeLinkEditor", "id", None))
				self.dstGroup.setTitle(QtModule.QApplication.translate("NodeLinkEditor", "Destination Node", None))
				self.name_label_3.setText(QtModule.QApplication.translate("NodeLinkEditor", "Name", None))
				self.label_label_2.setText(QtModule.QApplication.translate("NodeLinkEditor", "Parameter", None))
				self.name_label_4.setText(QtModule.QApplication.translate("NodeLinkEditor", "id", None))

