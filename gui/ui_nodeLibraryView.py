# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_nodeLibraryView.ui'
#
# Created: Tue Oct  9 18:06:09 2012
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

class Ui_nodeLibraryView(object):
		def setupUi(self, nodeLibraryView):
				nodeLibraryView.setObjectName(_fromUtf8("nodeLibraryView"))
				nodeLibraryView.resize(447, 443)
				self.verticalLayout = QtModule.QVBoxLayout(nodeLibraryView)
				self.verticalLayout.setSpacing(0)
				self.verticalLayout.setContentsMargins(2, 2, 2, 0)
				self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
				self.horizontalLayout = QtModule.QHBoxLayout()
				self.horizontalLayout.setSpacing(-1)
				self.horizontalLayout.setContentsMargins(8, -1, 8, -1)
				self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
				self.btn_reload = QtModule.QPushButton(nodeLibraryView)
				self.btn_reload.setMinimumSize(QtCore.QSize(60, 20))
				self.btn_reload.setMaximumSize(QtCore.QSize(60, 20))
				self.btn_reload.setObjectName(_fromUtf8("btn_reload"))
				self.horizontalLayout.addWidget(self.btn_reload)
				spacerItem = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
				self.horizontalLayout.addItem(spacerItem)
				self.horizontalLayout.setStretch(1, 1)
				self.verticalLayout.addLayout(self.horizontalLayout)
				self.nodeList = NodeList(nodeLibraryView)
				self.nodeList.setObjectName(_fromUtf8("nodeList"))
				self.verticalLayout.addWidget(self.nodeList)
				self.verticalLayout.setStretch(1, 1)

				self.retranslateUi(nodeLibraryView)
				
				if usePyQt4 :
					QtCore.QObject.connect(self.btn_reload, QtCore.SIGNAL(_fromUtf8("clicked()")), nodeLibraryView.onReload)
				else :
					self.btn_reload.clicked.connect( nodeLibraryView.onReload)
				QtCore.QMetaObject.connectSlotsByName(nodeLibraryView)

		def retranslateUi(self, nodeLibraryView):
				nodeLibraryView.setWindowTitle(QtModule.QApplication.translate("nodeLibraryView", "Form", None))
				self.btn_reload.setText(QtModule.QApplication.translate("nodeLibraryView", "Reload", None))

from nodeList import NodeList
