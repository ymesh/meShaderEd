# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_nodeParam.ui'
#
# Created: Thu Apr 11 21:06:16 2013
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

class Ui_Form(object):
		def setupUi(self, Form):
				Form.setObjectName(_fromUtf8("Form"))
				Form.resize(370, 474)
				self.verticalLayout = QtModule.QVBoxLayout(Form)
				self.verticalLayout.setSpacing(2)
				self.verticalLayout.setMargin(4)
				self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
				self.labelLayout = QtModule.QHBoxLayout()
				self.labelLayout.setObjectName(_fromUtf8("labelLayout"))
				self.label = QtModule.QLabel(Form)
				self.label.setObjectName(_fromUtf8("label"))
				self.labelLayout.addWidget(self.label)
				self.nodeLabelEdit = QtModule.QLineEdit(Form)
				self.nodeLabelEdit.setObjectName(_fromUtf8("nodeLabelEdit"))
				self.labelLayout.addWidget(self.nodeLabelEdit)
				self.labelLayout.setStretch(1, 1)
				self.verticalLayout.addLayout(self.labelLayout)
				self.label.setBuddy(self.nodeLabelEdit)

				self.retranslateUi(Form)
				QtCore.QMetaObject.connectSlotsByName(Form)

		def retranslateUi(self, Form):
				Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None)
				self.label.setText(QtGui.QApplication.translate("Form", "Label", None)

