# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_geomViewWidget.ui'
#
# Created: Tue Jul 09 00:42:52 2013
#      by: PyQt4 UI code generator 4.10.2-snapshot-a8a14dd99d1e
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
    def _fromUtf8(s):
            return s

try:
    _encoding = QtModule.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtModule.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtModule.QApplication.translate(context, text, disambig)

class Ui_geomViewWidget(object):
    def setupUi(self, geomViewWidget):
        geomViewWidget.setObjectName(_fromUtf8("geomViewWidget"))
        geomViewWidget.resize(499, 592)
        self.gridLayout = QtModule.QGridLayout(geomViewWidget)
        self.gridLayout.setContentsMargins ( 4, 4, 4, 4 )
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtModule.QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtModule.QLabel(geomViewWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.selector = QtModule.QComboBox(geomViewWidget)
        self.selector.setMinimumSize(QtCore.QSize(120, 20))
        self.selector.setMaximumSize(QtCore.QSize(16777215, 20))
        self.selector.setFrame(True)
        self.selector.setObjectName(_fromUtf8("selector"))
        self.horizontalLayout.addWidget(self.selector)
        self.btn_reset = QtModule.QToolButton(geomViewWidget)
        self.btn_reset.setMinimumSize(QtCore.QSize(0, 20))
        self.btn_reset.setMaximumSize(QtCore.QSize(16777215, 20))
        self.btn_reset.setObjectName(_fromUtf8("btn_reset"))
        self.horizontalLayout.addWidget(self.btn_reset)
        spacerItem = QtModule.QSpacerItem(68, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_render = QtModule.QPushButton(geomViewWidget)
        self.btn_render.setMaximumSize(QtCore.QSize(16777215, 20))
        self.btn_render.setObjectName(_fromUtf8("btn_render"))
        self.horizontalLayout.addWidget(self.btn_render)
        self.horizontalLayout.setStretch(3, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.geomView = GeomView(geomViewWidget)
        self.geomView.setObjectName(_fromUtf8("geomView"))
        self.gridLayout.addWidget(self.geomView, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(geomViewWidget)
        if usePyQt4 :
            QtCore.QObject.connect(self.btn_render, QtCore.SIGNAL(_fromUtf8("clicked()")), geomViewWidget.updateViewer)
            QtCore.QObject.connect(self.btn_reset, QtCore.SIGNAL(_fromUtf8("clicked()")), self.geomView.resetView)
        else :
            self.btn_render.clicked.connect( geomViewWidget.updateViewer)
            self.btn_reset.clicked.connect( self.geomView.resetView)
        QtCore.QMetaObject.connectSlotsByName(geomViewWidget)

    def retranslateUi(self, geomViewWidget):
        geomViewWidget.setWindowTitle(_translate("geomViewWidget", "GeomView", None))
        self.label.setText(_translate("geomViewWidget", "Node", None))
        self.btn_reset.setToolTip(_translate("geomViewWidget", "Reset zoom", None))
        self.btn_reset.setText(_translate("geomViewWidget", "Reset", None))
        self.btn_render.setText(_translate("geomViewWidget", "Update", None))

from gfx.geomView import GeomView
