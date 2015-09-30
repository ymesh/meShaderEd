# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/nodeEditor\ui_nodeCodeEditor.ui'
#
# Created: Sat Oct 19 22:17:58 2013
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
		_encoding = QtGui.QApplication.UnicodeUTF8
		def _translate(context, text, disambig):
				return QtModule.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
		def _translate(context, text, disambig):
				return QtModule.QApplication.translate(context, text, disambig)

class Ui_NodeCodeEditor(object):
		def setupUi(self, NodeCodeEditor):
				NodeCodeEditor.setObjectName(_fromUtf8("NodeCodeEditor"))
				NodeCodeEditor.resize(683, 838)
				self.gridLayout = QtModule.QGridLayout(NodeCodeEditor)
				if QtCore.QT_VERSION < 0x50000 :
					self.gridLayout.setMargin(0)
				self.gridLayout.setSpacing(0)
				self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
				self.textEdit = QtModule.QTextEdit(NodeCodeEditor)
				self.textEdit.setLineWidth(2)
				self.textEdit.setObjectName(_fromUtf8("textEdit"))
				self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)

				self.retranslateUi(NodeCodeEditor)
				QtCore.QMetaObject.connectSlotsByName(NodeCodeEditor)

		def retranslateUi(self, NodeCodeEditor):
				NodeCodeEditor.setWindowTitle(_translate("NodeCodeEditor", "Form", None))

