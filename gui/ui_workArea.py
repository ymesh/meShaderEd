# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_workArea.ui'
#
# Created: Mon Mar 14 07:25:17 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_workArea(object):
    def setupUi(self, workArea):
        workArea.setObjectName(_fromUtf8("workArea"))
        workArea.resize(668, 594)
        workArea.setAcceptDrops(True)
        self.gridLayout = QtGui.QGridLayout(workArea)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.graphicsView = QtGui.QGraphicsView(workArea)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.retranslateUi(workArea)
        QtCore.QMetaObject.connectSlotsByName(workArea)

    def retranslateUi(self, workArea):
        workArea.setWindowTitle(QtGui.QApplication.translate("workArea", "network", None, QtGui.QApplication.UnicodeUTF8))

