# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_nodeParam.ui'
#
# Created: Tue Apr 24 21:19:48 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(370, 474)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelLayout = QtGui.QHBoxLayout()
        self.labelLayout.setObjectName(_fromUtf8("labelLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setText(QtGui.QApplication.translate("Form", "Node Label", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.labelLayout.addWidget(self.label)
        self.nodeLabelEdit = QtGui.QLineEdit(Form)
        self.nodeLabelEdit.setObjectName(_fromUtf8("nodeLabelEdit"))
        self.labelLayout.addWidget(self.nodeLabelEdit)
        self.labelLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.labelLayout)
        self.label.setBuddy(self.nodeLabelEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

