# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_meRendererSetup.ui'
#
# Created: Tue Jan  4 02:56:05 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from core.mePyQt import QtCore, QtGui

class Ui_meRendererSetup(object):
    def setupUi(self, meRendererSetup):
        meRendererSetup.setObjectName("meRendererSetup")
        meRendererSetup.resize(447, 258)
        self.gridLayout = QtGui.QGridLayout(meRendererSetup)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelPreset = QtGui.QLabel(meRendererSetup)
        self.labelPreset.setMinimumSize(QtCore.QSize(80, 0))
        self.labelPreset.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.labelPreset.setFont(font)
        self.labelPreset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPreset.setObjectName("labelPreset")
        self.horizontalLayout.addWidget(self.labelPreset)
        self.listPreset = QtGui.QComboBox(meRendererSetup)
        self.listPreset.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listPreset.setFont(font)
        self.listPreset.setEditable(False)
        self.listPreset.setInsertPolicy(QtGui.QComboBox.InsertAtBottom)
        self.listPreset.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.listPreset.setFrame(True)
        self.listPreset.setObjectName("listPreset")
        self.horizontalLayout.addWidget(self.listPreset)
        spacerItem = QtGui.QSpacerItem(138, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.btnlt = QtGui.QHBoxLayout()
        self.btnlt.setSpacing(6)
        self.btnlt.setObjectName("btnlt")
        self.newButton = QtGui.QPushButton(meRendererSetup)
        self.newButton.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.newButton.setFont(font)
        self.newButton.setAutoDefault(False)
        self.newButton.setObjectName("newButton")
        self.btnlt.addWidget(self.newButton)
        self.deleteButton = QtGui.QPushButton(meRendererSetup)
        self.deleteButton.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deleteButton.setFont(font)
        self.deleteButton.setAutoDefault(False)
        self.deleteButton.setObjectName("deleteButton")
        self.btnlt.addWidget(self.deleteButton)
        self.saveButton = QtGui.QPushButton(meRendererSetup)
        self.saveButton.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.saveButton.setFont(font)
        self.saveButton.setAutoDefault(False)
        self.saveButton.setObjectName("saveButton")
        self.btnlt.addWidget(self.saveButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.btnlt.addItem(spacerItem1)
        self.cancelButton = QtGui.QPushButton(meRendererSetup)
        self.cancelButton.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cancelButton.setFont(font)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.btnlt.addWidget(self.cancelButton)
        self.okButton = QtGui.QPushButton(meRendererSetup)
        self.okButton.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.okButton.setFont(font)
        self.okButton.setAutoDefault(True)
        self.okButton.setDefault(True)
        self.okButton.setObjectName("okButton")
        self.btnlt.addWidget(self.okButton)
        self.btnlt.setStretch(3, 1)
        self.gridLayout.addLayout(self.btnlt, 5, 0, 1, 1)
        self.tabs = QtGui.QTabWidget(meRendererSetup)
        self.tabs.setMinimumSize(QtCore.QSize(0, 140))
        self.tabs.setMaximumSize(QtCore.QSize(16777215, 140))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.tabs.setFont(font)
        self.tabs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabs.setAutoFillBackground(True)
        self.tabs.setTabPosition(QtGui.QTabWidget.North)
        self.tabs.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabs.setElideMode(QtCore.Qt.ElideLeft)
        self.tabs.setUsesScrollButtons(False)
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(False)
        self.tabs.setObjectName("tabs")
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab1)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(2, 4, 2, 2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelName = QtGui.QLabel(self.tab1)
        self.labelName.setMinimumSize(QtCore.QSize(80, 0))
        self.labelName.setBaseSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelName.setFont(font)
        self.labelName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout_2.addWidget(self.labelName)
        self.lineName = QtGui.QLineEdit(self.tab1)
        self.lineName.setFrame(True)
        self.lineName.setObjectName("lineName")
        self.horizontalLayout_2.addWidget(self.lineName)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelCmd = QtGui.QLabel(self.tab1)
        self.labelCmd.setMinimumSize(QtCore.QSize(80, 0))
        self.labelCmd.setBaseSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCmd.setFont(font)
        self.labelCmd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCmd.setObjectName("labelCmd")
        self.horizontalLayout_3.addWidget(self.labelCmd)
        self.lineCmd = QtGui.QLineEdit(self.tab1)
        self.lineCmd.setObjectName("lineCmd")
        self.horizontalLayout_3.addWidget(self.lineCmd)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelFlags = QtGui.QLabel(self.tab1)
        self.labelFlags.setMinimumSize(QtCore.QSize(80, 0))
        self.labelFlags.setBaseSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelFlags.setFont(font)
        self.labelFlags.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelFlags.setObjectName("labelFlags")
        self.horizontalLayout_4.addWidget(self.labelFlags)
        self.lineFlags = QtGui.QLineEdit(self.tab1)
        self.lineFlags.setObjectName("lineFlags")
        self.horizontalLayout_4.addWidget(self.lineFlags)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtGui.QSpacerItem(20, 26, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tabs.addTab(self.tab1, "")
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName("tab2")
        self.verticalLayout = QtGui.QVBoxLayout(self.tab2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(2, 4, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labelCompiler = QtGui.QLabel(self.tab2)
        self.labelCompiler.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCompiler.setFont(font)
        self.labelCompiler.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCompiler.setObjectName("labelCompiler")
        self.horizontalLayout_5.addWidget(self.labelCompiler)
        self.lineCompiler = QtGui.QLineEdit(self.tab2)
        self.lineCompiler.setObjectName("lineCompiler")
        self.horizontalLayout_5.addWidget(self.lineCompiler)
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labelShaderInfo = QtGui.QLabel(self.tab2)
        self.labelShaderInfo.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelShaderInfo.setFont(font)
        self.labelShaderInfo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelShaderInfo.setObjectName("labelShaderInfo")
        self.horizontalLayout_6.addWidget(self.labelShaderInfo)
        self.lineShaderInfo = QtGui.QLineEdit(self.tab2)
        self.lineShaderInfo.setObjectName("lineShaderInfo")
        self.horizontalLayout_6.addWidget(self.lineShaderInfo)
        self.horizontalLayout_6.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(4)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.labelDefines = QtGui.QLabel(self.tab2)
        self.labelDefines.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelDefines.setFont(font)
        self.labelDefines.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelDefines.setObjectName("labelDefines")
        self.horizontalLayout_7.addWidget(self.labelDefines)
        self.lineDefines = QtGui.QLineEdit(self.tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineDefines.sizePolicy().hasHeightForWidth())
        self.lineDefines.setSizePolicy(sizePolicy)
        self.lineDefines.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineDefines.setObjectName("lineDefines")
        self.horizontalLayout_7.addWidget(self.lineDefines)
        self.horizontalLayout_7.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(4)
        self.horizontalLayout_8.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.labelShaderExt = QtGui.QLabel(self.tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelShaderExt.sizePolicy().hasHeightForWidth())
        self.labelShaderExt.setSizePolicy(sizePolicy)
        self.labelShaderExt.setMinimumSize(QtCore.QSize(80, 0))
        self.labelShaderExt.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelShaderExt.setFont(font)
        self.labelShaderExt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelShaderExt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelShaderExt.setObjectName("labelShaderExt")
        self.horizontalLayout_8.addWidget(self.labelShaderExt)
        self.lineShaderExt = QtGui.QLineEdit(self.tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineShaderExt.sizePolicy().hasHeightForWidth())
        self.lineShaderExt.setSizePolicy(sizePolicy)
        self.lineShaderExt.setMinimumSize(QtCore.QSize(50, 0))
        self.lineShaderExt.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineShaderExt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineShaderExt.setAutoFillBackground(False)
        self.lineShaderExt.setObjectName("lineShaderExt")
        self.horizontalLayout_8.addWidget(self.lineShaderExt)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.horizontalLayout_8.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        spacerItem4 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.tabs.addTab(self.tab2, "")
        self.tab3 = QtGui.QWidget()
        self.tab3.setObjectName("tab3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab3)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setContentsMargins(2, 4, 2, 2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(4)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.labelTexMake = QtGui.QLabel(self.tab3)
        self.labelTexMake.setMinimumSize(QtCore.QSize(80, 0))
        self.labelTexMake.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTexMake.setFont(font)
        self.labelTexMake.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelTexMake.setObjectName("labelTexMake")
        self.horizontalLayout_9.addWidget(self.labelTexMake)
        self.lineTexMake = QtGui.QLineEdit(self.tab3)
        self.lineTexMake.setObjectName("lineTexMake")
        self.horizontalLayout_9.addWidget(self.lineTexMake)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(4)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.labelTexInfo = QtGui.QLabel(self.tab3)
        self.labelTexInfo.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTexInfo.setFont(font)
        self.labelTexInfo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelTexInfo.setObjectName("labelTexInfo")
        self.horizontalLayout_10.addWidget(self.labelTexInfo)
        self.lineTexInfo = QtGui.QLineEdit(self.tab3)
        self.lineTexInfo.setObjectName("lineTexInfo")
        self.horizontalLayout_10.addWidget(self.lineTexInfo)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(4)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.labelTexViewer = QtGui.QLabel(self.tab3)
        self.labelTexViewer.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTexViewer.setFont(font)
        self.labelTexViewer.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelTexViewer.setObjectName("labelTexViewer")
        self.horizontalLayout_11.addWidget(self.labelTexViewer)
        self.lineTexViewer = QtGui.QLineEdit(self.tab3)
        self.lineTexViewer.setObjectName("lineTexViewer")
        self.horizontalLayout_11.addWidget(self.lineTexViewer)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(4)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.labelTexExt = QtGui.QLabel(self.tab3)
        self.labelTexExt.setMinimumSize(QtCore.QSize(80, 0))
        self.labelTexExt.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTexExt.setFont(font)
        self.labelTexExt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelTexExt.setObjectName("labelTexExt")
        self.horizontalLayout_12.addWidget(self.labelTexExt)
        self.lineTexExt = QtGui.QLineEdit(self.tab3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineTexExt.sizePolicy().hasHeightForWidth())
        self.lineTexExt.setSizePolicy(sizePolicy)
        self.lineTexExt.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineTexExt.setObjectName("lineTexExt")
        self.horizontalLayout_12.addWidget(self.lineTexExt)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem5)
        self.horizontalLayout_12.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.tabs.addTab(self.tab3, "")
        self.gridLayout.addWidget(self.tabs, 1, 0, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 4, 0, 1, 1)

        self.retranslateUi(meRendererSetup)
        self.tabs.setCurrentIndex(0)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), meRendererSetup.close)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), meRendererSetup.onSelect)
        QtCore.QObject.connect(self.listPreset, QtCore.SIGNAL("currentIndexChanged(QString)"), meRendererSetup.onIndexChanged)
        QtCore.QObject.connect(self.newButton, QtCore.SIGNAL("clicked()"), meRendererSetup.onNewPreset)
        QtCore.QObject.connect(self.deleteButton, QtCore.SIGNAL("clicked()"), meRendererSetup.onDeletePreset)
        QtCore.QObject.connect(self.lineName, QtCore.SIGNAL("editingFinished()"), meRendererSetup.onEditLabel)
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL("clicked()"), meRendererSetup.onSave)
        QtCore.QMetaObject.connectSlotsByName(meRendererSetup)
        meRendererSetup.setTabOrder(self.tabs, self.listPreset)
        meRendererSetup.setTabOrder(self.listPreset, self.newButton)
        meRendererSetup.setTabOrder(self.newButton, self.deleteButton)
        meRendererSetup.setTabOrder(self.deleteButton, self.cancelButton)
        meRendererSetup.setTabOrder(self.cancelButton, self.lineName)
        meRendererSetup.setTabOrder(self.lineName, self.lineCmd)
        meRendererSetup.setTabOrder(self.lineCmd, self.lineFlags)
        meRendererSetup.setTabOrder(self.lineFlags, self.lineCompiler)
        meRendererSetup.setTabOrder(self.lineCompiler, self.lineShaderInfo)
        meRendererSetup.setTabOrder(self.lineShaderInfo, self.lineDefines)
        meRendererSetup.setTabOrder(self.lineDefines, self.lineShaderExt)
        meRendererSetup.setTabOrder(self.lineShaderExt, self.lineTexMake)
        meRendererSetup.setTabOrder(self.lineTexMake, self.lineTexInfo)
        meRendererSetup.setTabOrder(self.lineTexInfo, self.lineTexViewer)
        meRendererSetup.setTabOrder(self.lineTexViewer, self.lineTexExt)

    def retranslateUi(self, meRendererSetup):
        meRendererSetup.setWindowTitle(QtGui.QApplication.translate("meRendererSetup", "Renderer preset setup", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPreset.setText(QtGui.QApplication.translate("meRendererSetup", "Preset", None, QtGui.QApplication.UnicodeUTF8))
        self.newButton.setToolTip(QtGui.QApplication.translate("meRendererSetup", "Create new renderer preset", None, QtGui.QApplication.UnicodeUTF8))
        self.newButton.setText(QtGui.QApplication.translate("meRendererSetup", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setToolTip(QtGui.QApplication.translate("meRendererSetup", "Delete current renderer preset", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("meRendererSetup", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setToolTip(QtGui.QApplication.translate("meRendererSetup", "Save current renderer preset", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("meRendererSetup", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("meRendererSetup", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setToolTip(QtGui.QApplication.translate("meRendererSetup", "Select current renderer preset", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("meRendererSetup", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.labelName.setText(QtGui.QApplication.translate("meRendererSetup", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCmd.setText(QtGui.QApplication.translate("meRendererSetup", "Command", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFlags.setText(QtGui.QApplication.translate("meRendererSetup", "Flags", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab1), QtGui.QApplication.translate("meRendererSetup", "Renderer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCompiler.setText(QtGui.QApplication.translate("meRendererSetup", " Compiler", None, QtGui.QApplication.UnicodeUTF8))
        self.labelShaderInfo.setText(QtGui.QApplication.translate("meRendererSetup", "SloInfo", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDefines.setText(QtGui.QApplication.translate("meRendererSetup", "Defines", None, QtGui.QApplication.UnicodeUTF8))
        self.labelShaderExt.setText(QtGui.QApplication.translate("meRendererSetup", " Extension", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab2), QtGui.QApplication.translate("meRendererSetup", "Shaders", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTexMake.setText(QtGui.QApplication.translate("meRendererSetup", "TexMake", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTexInfo.setText(QtGui.QApplication.translate("meRendererSetup", " TexInfo", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTexViewer.setText(QtGui.QApplication.translate("meRendererSetup", "Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTexExt.setText(QtGui.QApplication.translate("meRendererSetup", " Extension", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab3), QtGui.QApplication.translate("meRendererSetup", "Textures", None, QtGui.QApplication.UnicodeUTF8))

