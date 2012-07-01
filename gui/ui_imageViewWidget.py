# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_imageViewWidget.ui'
#
# Created: Sun May 20 20:04:20 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_imageViewWidget(object):
    def setupUi(self, imageViewWidget):
        imageViewWidget.setObjectName(_fromUtf8("imageViewWidget"))
        imageViewWidget.resize(479, 520)
        self.gridLayout = QtGui.QGridLayout(imageViewWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(imageViewWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.selector = QtGui.QComboBox(imageViewWidget)
        self.selector.setMinimumSize(QtCore.QSize(120, 20))
        self.selector.setMaximumSize(QtCore.QSize(16777215, 20))
        self.selector.setFrame(True)
        self.selector.setObjectName(_fromUtf8("selector"))
        self.horizontalLayout.addWidget(self.selector)
        self.btn_render = QtGui.QPushButton(imageViewWidget)
        self.btn_render.setMaximumSize(QtCore.QSize(16777215, 20))
        self.btn_render.setObjectName(_fromUtf8("btn_render"))
        self.horizontalLayout.addWidget(self.btn_render)
        spacerItem = QtGui.QSpacerItem(68, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.imageArea = ImageView(imageViewWidget)
        self.imageArea.setObjectName(_fromUtf8("imageArea"))
        self.gridLayout.addWidget(self.imageArea, 1, 0, 1, 1)

        self.retranslateUi(imageViewWidget)
        QtCore.QObject.connect(self.btn_render, QtCore.SIGNAL(_fromUtf8("clicked()")), imageViewWidget.updateViewer)
        QtCore.QMetaObject.connectSlotsByName(imageViewWidget)

    def retranslateUi(self, imageViewWidget):
        imageViewWidget.setWindowTitle(QtGui.QApplication.translate("imageViewWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("imageViewWidget", "Image Node", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_render.setText(QtGui.QApplication.translate("imageViewWidget", "Update", None, QtGui.QApplication.UnicodeUTF8))

from gfx.imageView import ImageView
