# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_nodeSwatchParam.ui'
#
# Created: Thu Apr 11 14:10:28 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from core.mePyQt import QtCore, QtGui

if QtCore.QT_VERSION < 50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class Ui_NodeSwatchParam(object):
		def setupUi(self, NodeSwatchParam):
				NodeSwatchParam.setObjectName(_fromUtf8("NodeSwatchParam"))
				NodeSwatchParam.resize(408, 309)
				self.verticalLayout = QtModule.QVBoxLayout(NodeSwatchParam)
				self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
				self.hl_type = QtModule.QHBoxLayout()
				self.hl_type.setObjectName(_fromUtf8("hl_type"))
				self.label = QtModule.QLabel(NodeSwatchParam)
				self.label.setMinimumSize(QtCore.QSize(80, 0))
				self.label.setObjectName(_fromUtf8("label"))
				self.hl_type.addWidget(self.label)
				self.type_selector = QtModule.QComboBox(NodeSwatchParam)
				self.type_selector.setEnabled(False)
				self.type_selector.setObjectName(_fromUtf8("type_selector"))
				self.hl_type.addWidget(self.type_selector)
				spacerItem = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.hl_type.addItem(spacerItem)
				self.hl_type.setStretch(2, 1)
				self.verticalLayout.addLayout(self.hl_type)
				self.hl_param = QtModule.QHBoxLayout()
				self.hl_param.setObjectName(_fromUtf8("hl_param"))
				self.label_2 = QtModule.QLabel(NodeSwatchParam)
				self.label_2.setMinimumSize(QtCore.QSize(80, 0))
				self.label_2.setObjectName(_fromUtf8("label_2"))
				self.hl_param.addWidget(self.label_2)
				self.param_selector = QtModule.QComboBox(NodeSwatchParam)
				self.param_selector.setObjectName(_fromUtf8("param_selector"))
				self.hl_param.addWidget(self.param_selector)
				spacerItem1 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.hl_param.addItem(spacerItem1)
				self.verticalLayout.addLayout(self.hl_param)
				self.hl_shape = QtModule.QHBoxLayout()
				self.hl_shape.setObjectName(_fromUtf8("hl_shape"))
				self.label_3 = QtModule.QLabel(NodeSwatchParam)
				self.label_3.setMinimumSize(QtCore.QSize(80, 0))
				self.label_3.setObjectName(_fromUtf8("label_3"))
				self.hl_shape.addWidget(self.label_3)
				self.shape_selector = QtModule.QComboBox(NodeSwatchParam)
				self.shape_selector.setObjectName(_fromUtf8("shape_selector"))
				self.hl_shape.addWidget(self.shape_selector)
				spacerItem2 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.hl_shape.addItem(spacerItem2)
				self.verticalLayout.addLayout(self.hl_shape)
				self.hl_size = QtModule.QHBoxLayout()
				self.hl_size.setObjectName(_fromUtf8("hl_size"))
				self.label_4 = QtModule.QLabel(NodeSwatchParam)
				self.label_4.setMinimumSize(QtCore.QSize(80, 0))
				self.label_4.setObjectName(_fromUtf8("label_4"))
				self.hl_size.addWidget(self.label_4)
				self.size_selector = QtModule.QComboBox(NodeSwatchParam)
				self.size_selector.setObjectName(_fromUtf8("size_selector"))
				self.hl_size.addWidget(self.size_selector)
				spacerItem3 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.hl_size.addItem(spacerItem3)
				self.verticalLayout.addLayout(self.hl_size)
				self.hl_rate = QtModule.QHBoxLayout()
				self.hl_rate.setObjectName(_fromUtf8("hl_rate"))
				self.label_5 = QtModule.QLabel(NodeSwatchParam)
				self.label_5.setMinimumSize(QtCore.QSize(80, 0))
				self.label_5.setObjectName(_fromUtf8("label_5"))
				self.hl_rate.addWidget(self.label_5)
				self.lineEdit = QtModule.QLineEdit(NodeSwatchParam)
				self.lineEdit.setMinimumSize(QtCore.QSize(50, 0))
				self.lineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
				self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
				self.hl_rate.addWidget(self.lineEdit)
				spacerItem4 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.hl_rate.addItem(spacerItem4)
				self.verticalLayout.addLayout(self.hl_rate)
				spacerItem5 = QtModule.QSpacerItem(20, 148, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
				self.verticalLayout.addItem(spacerItem5)

				self.retranslateUi(NodeSwatchParam)
				QtCore.QMetaObject.connectSlotsByName(NodeSwatchParam)

		def retranslateUi(self, NodeSwatchParam):
				NodeSwatchParam.setWindowTitle(QtModule.QApplication.translate("NodeSwatchParam", "Form", None))
				self.label.setText(QtModule.QApplication.translate("NodeSwatchParam", "Type", None))
				self.label_2.setText(QtModule.QApplication.translate("NodeSwatchParam", "Parameter", None))
				self.label_3.setText(QtModule.QApplication.translate("NodeSwatchParam", "Shape", None))
				self.label_4.setText(QtModule.QApplication.translate("NodeSwatchParam", "Size", None))
				self.label_5.setText(QtModule.QApplication.translate("NodeSwatchParam", "Shading Rate", None))

