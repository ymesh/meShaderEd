# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/nodeEditor\ui_nodePropertiesEditor.ui'
#
# Created: Wed Oct 16 19:16:22 2013
#      by: PyQt4 UI code generator 4.10.2-snapshot-a8a14dd99d1e
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
		def _fromUtf8(s):
				return s

try:
		_encoding = QtModule.QApplication.UnicodeUTF8
		def _translate(context, text, disambig):
				return QtModule.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
		def _translate(context, text, disambig):
				return QtModule.QApplication.translate(context, text, disambig)

class Ui_NodePropertiesEditor(object):
		def setupUi(self, NodePropertiesEditor):
				NodePropertiesEditor.setObjectName(_fromUtf8("NodePropertiesEditor"))
				NodePropertiesEditor.resize(448, 498)
				self.verticalLayout = QtModule.QVBoxLayout(NodePropertiesEditor)
				self.verticalLayout.setSpacing(2)
				self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
				self.horizontalLayout_2 = QtModule.QHBoxLayout()
				self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
				self.name_label = QtModule.QLabel(NodePropertiesEditor)
				self.name_label.setMinimumSize(QtCore.QSize(100, 0))
				self.name_label.setObjectName(_fromUtf8("name_label"))
				self.horizontalLayout_2.addWidget(self.name_label)
				self.name_lineEdit = QtModule.QLineEdit(NodePropertiesEditor)
				self.name_lineEdit.setObjectName(_fromUtf8("name_lineEdit"))
				self.horizontalLayout_2.addWidget(self.name_lineEdit)
				self.horizontalLayout_2.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_2)
				self.horizontalLayout_3 = QtModule.QHBoxLayout()
				self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
				self.label_label = QtModule.QLabel(NodePropertiesEditor)
				self.label_label.setMinimumSize(QtCore.QSize(100, 0))
				self.label_label.setObjectName(_fromUtf8("label_label"))
				self.horizontalLayout_3.addWidget(self.label_label)
				self.label_lineEdit = QtModule.QLineEdit(NodePropertiesEditor)
				self.label_lineEdit.setObjectName(_fromUtf8("label_lineEdit"))
				self.horizontalLayout_3.addWidget(self.label_lineEdit)
				self.horizontalLayout_3.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_3)
				self.horizontalLayout_7 = QtModule.QHBoxLayout()
				self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
				self.type_label = QtModule.QLabel(NodePropertiesEditor)
				self.type_label.setMinimumSize(QtCore.QSize(100, 0))
				self.type_label.setObjectName(_fromUtf8("type_label"))
				self.horizontalLayout_7.addWidget(self.type_label)
				self.type_comboBox = QtModule.QComboBox(NodePropertiesEditor)
				self.type_comboBox.setMinimumSize(QtCore.QSize(100, 0))
				self.type_comboBox.setObjectName(_fromUtf8("type_comboBox"))
				self.horizontalLayout_7.addWidget(self.type_comboBox)
				spacerItem = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_7.addItem(spacerItem)
				self.verticalLayout.addLayout(self.horizontalLayout_7)
				self.horizontalLayout_5 = QtModule.QHBoxLayout()
				self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
				self.author_label = QtModule.QLabel(NodePropertiesEditor)
				self.author_label.setMinimumSize(QtCore.QSize(100, 0))
				self.author_label.setObjectName(_fromUtf8("author_label"))
				self.horizontalLayout_5.addWidget(self.author_label)
				self.author_lineEdit = QtModule.QLineEdit(NodePropertiesEditor)
				self.author_lineEdit.setObjectName(_fromUtf8("author_lineEdit"))
				self.horizontalLayout_5.addWidget(self.author_lineEdit)
				self.horizontalLayout_5.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_5)
				self.horizontalLayout_6 = QtModule.QHBoxLayout()
				self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
				self.icon_label = QtModule.QLabel(NodePropertiesEditor)
				self.icon_label.setMinimumSize(QtCore.QSize(100, 0))
				self.icon_label.setObjectName(_fromUtf8("icon_label"))
				self.horizontalLayout_6.addWidget(self.icon_label)
				self.icon_lineEdit = QtModule.QLineEdit(NodePropertiesEditor)
				self.icon_lineEdit.setObjectName(_fromUtf8("icon_lineEdit"))
				self.horizontalLayout_6.addWidget(self.icon_lineEdit)
				self.horizontalLayout_6.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_6)
				self.horizontalLayout_8 = QtModule.QHBoxLayout()
				self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
				self.master_label = QtModule.QLabel(NodePropertiesEditor)
				self.master_label.setMinimumSize(QtCore.QSize(100, 0))
				self.master_label.setObjectName(_fromUtf8("master_label"))
				self.horizontalLayout_8.addWidget(self.master_label)
				self.master_lineEdit = QtModule.QLineEdit(NodePropertiesEditor)
				self.master_lineEdit.setObjectName(_fromUtf8("master_lineEdit"))
				self.horizontalLayout_8.addWidget(self.master_lineEdit)
				self.horizontalLayout_8.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_8)
				self.horizontalLayout_9 = QtModule.QHBoxLayout()
				self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
				self.id_label = QtModule.QLabel(NodePropertiesEditor)
				self.id_label.setEnabled(False)
				self.id_label.setMinimumSize(QtCore.QSize(100, 0))
				self.id_label.setObjectName(_fromUtf8("id_label"))
				self.horizontalLayout_9.addWidget(self.id_label)
				self.id_lineEdit = QtModule.QLineEdit(NodePropertiesEditor)
				self.id_lineEdit.setEnabled(False)
				self.id_lineEdit.setMinimumSize(QtCore.QSize(60, 0))
				self.id_lineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
				self.id_lineEdit.setObjectName(_fromUtf8("id_lineEdit"))
				self.horizontalLayout_9.addWidget(self.id_lineEdit)
				spacerItem1 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout_9.addItem(spacerItem1)
				self.horizontalLayout_9.setStretch(2, 1)
				self.verticalLayout.addLayout(self.horizontalLayout_9)
				spacerItem2 = QtModule.QSpacerItem(20, 109, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
				self.verticalLayout.addItem(spacerItem2)
				self.horizontalLayout_4 = QtModule.QHBoxLayout()
				self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
				self.help_label = QtModule.QLabel(NodePropertiesEditor)
				self.help_label.setMinimumSize(QtCore.QSize(100, 0))
				self.help_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
				self.help_label.setObjectName(_fromUtf8("help_label"))
				self.horizontalLayout_4.addWidget(self.help_label)
				self.help_plainTextEdit = QtModule.QPlainTextEdit(NodePropertiesEditor)
				self.help_plainTextEdit.setMinimumSize(QtCore.QSize(0, 60))
				self.help_plainTextEdit.setObjectName(_fromUtf8("help_plainTextEdit"))
				self.horizontalLayout_4.addWidget(self.help_plainTextEdit)
				self.verticalLayout.addLayout(self.horizontalLayout_4)

				self.retranslateUi(NodePropertiesEditor)
				QtCore.QMetaObject.connectSlotsByName(NodePropertiesEditor)

		def retranslateUi(self, NodePropertiesEditor):
				NodePropertiesEditor.setWindowTitle(_translate("NodePropertiesEditor", "NodeEditor", None))
				self.name_label.setText(_translate("NodePropertiesEditor", "Name", None))
				self.label_label.setText(_translate("NodePropertiesEditor", "Label", None))
				self.type_label.setText(_translate("NodePropertiesEditor", "Type", None))
				self.author_label.setText(_translate("NodePropertiesEditor", "Author", None))
				self.icon_label.setText(_translate("NodePropertiesEditor", "Icon", None))
				self.master_label.setText(_translate("NodePropertiesEditor", "Master", None))
				self.id_label.setText(_translate("NodePropertiesEditor", "Node ID", None))
				self.help_label.setText(_translate("NodePropertiesEditor", "Description", None))

