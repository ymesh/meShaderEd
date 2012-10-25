# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_geomViewWidget.ui'
#
# Created: Tue Oct  9 17:55:21 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_geomViewWidget(object):
    def setupUi(self, geomViewWidget):
        geomViewWidget.setObjectName(_fromUtf8("geomViewWidget"))
        geomViewWidget.resize(479, 520)
        self.verticalLayout = QtGui.QVBoxLayout(geomViewWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(geomViewWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.selector = QtGui.QComboBox(geomViewWidget)
        self.selector.setMinimumSize(QtCore.QSize(120, 20))
        self.selector.setMaximumSize(QtCore.QSize(16777215, 20))
        self.selector.setFrame(True)
        self.selector.setObjectName(_fromUtf8("selector"))
        self.horizontalLayout.addWidget(self.selector)
        spacerItem = QtGui.QSpacerItem(68, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_render = QtGui.QPushButton(geomViewWidget)
        self.btn_render.setMaximumSize(QtCore.QSize(16777215, 20))
        self.btn_render.setObjectName(_fromUtf8("btn_render"))
        self.horizontalLayout.addWidget(self.btn_render)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.geomView = GeomView(geomViewWidget)
        self.geomView.setObjectName(_fromUtf8("geomView"))
        self.verticalLayout.addWidget(self.geomView)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(geomViewWidget)
        QtCore.QObject.connect(self.btn_render, QtCore.SIGNAL(_fromUtf8("clicked()")), geomViewWidget.updateViewer)
        QtCore.QMetaObject.connectSlotsByName(geomViewWidget)

    def retranslateUi(self, geomViewWidget):
        geomViewWidget.setWindowTitle(QtGui.QApplication.translate("geomViewWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("geomViewWidget", "Geom Node", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_render.setText(QtGui.QApplication.translate("geomViewWidget", "Update", None, QtGui.QApplication.UnicodeUTF8))

from gfx.geomView import GeomView
