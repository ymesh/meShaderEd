# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_meRendererSetup.ui'
#
# Created: Tue Jan  4 02:56:05 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

if  not usePyQt5 :
  QtModule = QtGui
else :
  from core.mePyQt import QtWidgets
  QtModule = QtWidgets

class Ui_meRendererSetup(object):
    def setupUi(self, meRendererSetup):
        meRendererSetup.setObjectName("meRendererSetup")
        meRendererSetup.resize(447, 258)
        self.gridLayout = QtModule.QGridLayout(meRendererSetup)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtModule.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelPreset = QtModule.QLabel(meRendererSetup)
        self.labelPreset.setMinimumSize(QtCore.QSize(80, 0))
        self.labelPreset.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.labelPreset.setFont(font)
        self.labelPreset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPreset.setObjectName("labelPreset")
        self.horizontalLayout.addWidget(self.labelPreset)
        self.listPreset = QtModule.QComboBox(meRendererSetup)
        self.listPreset.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listPreset.setFont(font)
        self.listPreset.setEditable(False)
        self.listPreset.setInsertPolicy(QtModule.QComboBox.InsertAtBottom)
        self.listPreset.setSizeAdjustPolicy(QtModule.QComboBox.AdjustToContentsOnFirstShow)
        self.listPreset.setFrame(True)
        self.listPreset.setObjectName("listPreset")
        self.horizontalLayout.addWidget(self.listPreset)
        spacerItem = QtModule.QSpacerItem(138, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.btnlt = QtModule.QHBoxLayout()
        self.btnlt.setSpacing(6)
        self.btnlt.setObjectName("btnlt")
        self.newButton = QtModule.QPushButton(meRendererSetup)
        self.newButton.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.newButton.setFont(font)
        self.newButton.setAutoDefault(False)
        self.newButton.setObjectName("newButton")
        self.btnlt.addWidget(self.newButton)
        self.deleteButton = QtModule.QPushButton(meRendererSetup)
        self.deleteButton.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deleteButton.setFont(font)
        self.deleteButton.setAutoDefault(False)
        self.deleteButton.setObjectName("deleteButton")
        self.btnlt.addWidget(self.deleteButton)
        self.saveButton = QtModule.QPushButton(meRendererSetup)
        self.saveButton.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.saveButton.setFont(font)
        self.saveButton.setAutoDefault(False)
        self.saveButton.setObjectName("saveButton")
        self.btnlt.addWidget(self.saveButton)
        spacerItem1 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
        self.btnlt.addItem(spacerItem1)
        self.cancelButton = QtModule.QPushButton(meRendererSetup)
        self.cancelButton.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cancelButton.setFont(font)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.btnlt.addWidget(self.cancelButton)
        self.okButton = QtModule.QPushButton(meRendererSetup)
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
        self.tabs = QtModule.QTabWidget(meRendererSetup)
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
        self.tabs.setTabPosition(QtModule.QTabWidget.North)
        self.tabs.setTabShape(QtModule.QTabWidget.Rounded)
        self.tabs.setElideMode(QtCore.Qt.ElideLeft)
        self.tabs.setUsesScrollButtons(False)
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(False)
        self.tabs.setObjectName("tabs")
        self.tab1 = QtModule.QWidget()
        self.tab1.setObjectName("tab1")
        self.verticalLayout_2 = QtModule.QVBoxLayout(self.tab1)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(2, 4, 2, 2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtModule.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelName = QtModule.QLabel(self.tab1)
        self.labelName.setMinimumSize(QtCore.QSize(80, 0))
        self.labelName.setBaseSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelName.setFont(font)
        self.labelName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout_2.addWidget(self.labelName)
        self.lineName = QtModule.QLineEdit(self.tab1)
        self.lineName.setFrame(True)
        self.lineName.setObjectName("lineName")
        self.horizontalLayout_2.addWidget(self.lineName)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtModule.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelCmd = QtModule.QLabel(self.tab1)
        self.labelCmd.setMinimumSize(QtCore.QSize(80, 0))
        self.labelCmd.setBaseSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCmd.setFont(font)
        self.labelCmd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCmd.setObjectName("labelCmd")
        self.horizontalLayout_3.addWidget(self.labelCmd)
        self.lineCmd = QtModule.QLineEdit(self.tab1)
        self.lineCmd.setObjectName("lineCmd")
        self.horizontalLayout_3.addWidget(self.lineCmd)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtModule.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelFlags = QtModule.QLabel(self.tab1)
        self.labelFlags.setMinimumSize(QtCore.QSize(80, 0))
        self.labelFlags.setBaseSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelFlags.setFont(font)
        self.labelFlags.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelFlags.setObjectName("labelFlags")
        self.horizontalLayout_4.addWidget(self.labelFlags)
        self.lineFlags = QtModule.QLineEdit(self.tab1)
        self.lineFlags.setObjectName("lineFlags")
        self.horizontalLayout_4.addWidget(self.lineFlags)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtModule.QSpacerItem(20, 26, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tabs.addTab(self.tab1, "")
        self.tab2 = QtModule.QWidget()
        self.tab2.setObjectName("tab2")
        self.verticalLayout = QtModule.QVBoxLayout(self.tab2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(2, 4, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtModule.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labelCompiler = QtModule.QLabel(self.tab2)
        self.labelCompiler.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCompiler.setFont(font)
        self.labelCompiler.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCompiler.setObjectName("labelCompiler")
        self.horizontalLayout_5.addWidget(self.labelCompiler)
        self.lineCompiler = QtModule.QLineEdit(self.tab2)
        self.lineCompiler.setObjectName("lineCompiler")
        self.horizontalLayout_5.addWidget(self.lineCompiler)
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtModule.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labelShaderInfo = QtModule.QLabel(self.tab2)
        self.labelShaderInfo.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelShaderInfo.setFont(font)
        self.labelShaderInfo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelShaderInfo.setObjectName("labelShaderInfo")
        self.horizontalLayout_6.addWidget(self.labelShaderInfo)
        self.lineShaderInfo = QtModule.QLineEdit(self.tab2)
        self.lineShaderInfo.setObjectName("lineShaderInfo")
        self.horizontalLayout_6.addWidget(self.lineShaderInfo)
        self.horizontalLayout_6.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtModule.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(4)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.labelDefines = QtModule.QLabel(self.tab2)
        self.labelDefines.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelDefines.setFont(font)
        self.labelDefines.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelDefines.setObjectName("labelDefines")
        self.horizontalLayout_7.addWidget(self.labelDefines)
        self.lineDefines = QtModule.QLineEdit(self.tab2)
        sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineDefines.sizePolicy().hasHeightForWidth())
        self.lineDefines.setSizePolicy(sizePolicy)
        self.lineDefines.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineDefines.setObjectName("lineDefines")
        self.horizontalLayout_7.addWidget(self.lineDefines)
        self.horizontalLayout_7.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtModule.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(4)
        self.horizontalLayout_8.setSizeConstraint(QtModule.QLayout.SetNoConstraint)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.labelShaderExt = QtModule.QLabel(self.tab2)
        sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Fixed, QtModule.QSizePolicy.Preferred)
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
        self.lineShaderExt = QtModule.QLineEdit(self.tab2)
        sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Fixed, QtModule.QSizePolicy.Fixed)
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
        spacerItem3 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.horizontalLayout_8.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        spacerItem4 = QtModule.QSpacerItem(20, 0, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.tabs.addTab(self.tab2, "")
        self.tab3 = QtModule.QWidget()
        self.tab3.setObjectName("tab3")
        self.verticalLayout_3 = QtModule.QVBoxLayout(self.tab3)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setContentsMargins(2, 4, 2, 2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_9 = QtModule.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(4)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.labelTexMake = QtModule.QLabel(self.tab3)
        self.labelTexMake.setMinimumSize(QtCore.QSize(80, 0))
        self.labelTexMake.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTexMake.setFont(font)
        self.labelTexMake.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelTexMake.setObjectName("labelTexMake")
        self.horizontalLayout_9.addWidget(self.labelTexMake)
        self.lineTexMake = QtModule.QLineEdit(self.tab3)
        self.lineTexMake.setObjectName("lineTexMake")
        self.horizontalLayout_9.addWidget(self.lineTexMake)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtModule.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(4)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.labelTexInfo = QtModule.QLabel(self.tab3)
        self.labelTexInfo.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTexInfo.setFont(font)
        self.labelTexInfo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelTexInfo.setObjectName("labelTexInfo")
        self.horizontalLayout_10.addWidget(self.labelTexInfo)
        self.lineTexInfo = QtModule.QLineEdit(self.tab3)
        self.lineTexInfo.setObjectName("lineTexInfo")
        self.horizontalLayout_10.addWidget(self.lineTexInfo)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtModule.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(4)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.labelTexViewer = QtModule.QLabel(self.tab3)
        self.labelTexViewer.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTexViewer.setFont(font)
        self.labelTexViewer.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelTexViewer.setObjectName("labelTexViewer")
        self.horizontalLayout_11.addWidget(self.labelTexViewer)
        self.lineTexViewer = QtModule.QLineEdit(self.tab3)
        self.lineTexViewer.setObjectName("lineTexViewer")
        self.horizontalLayout_11.addWidget(self.lineTexViewer)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtModule.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(4)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.labelTexExt = QtModule.QLabel(self.tab3)
        self.labelTexExt.setMinimumSize(QtCore.QSize(80, 0))
        self.labelTexExt.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTexExt.setFont(font)
        self.labelTexExt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelTexExt.setObjectName("labelTexExt")
        self.horizontalLayout_12.addWidget(self.labelTexExt)
        self.lineTexExt = QtModule.QLineEdit(self.tab3)
        sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Fixed, QtModule.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineTexExt.sizePolicy().hasHeightForWidth())
        self.lineTexExt.setSizePolicy(sizePolicy)
        self.lineTexExt.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineTexExt.setObjectName("lineTexExt")
        self.horizontalLayout_12.addWidget(self.lineTexExt)
        spacerItem5 = QtModule.QSpacerItem(40, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem5)
        self.horizontalLayout_12.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        spacerItem6 = QtModule.QSpacerItem(20, 40, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.tabs.addTab(self.tab3, "")
        self.gridLayout.addWidget(self.tabs, 1, 0, 1, 1)
        spacerItem7 = QtModule.QSpacerItem(20, 40, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 4, 0, 1, 1)

        self.retranslateUi(meRendererSetup)
        self.tabs.setCurrentIndex(0)
        
        if  usePyQt4 :
          QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), meRendererSetup.close)
          QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), meRendererSetup.onSelect)
          QtCore.QObject.connect(self.listPreset, QtCore.SIGNAL("currentIndexChanged(QString)"), meRendererSetup.onIndexChanged)
          QtCore.QObject.connect(self.newButton, QtCore.SIGNAL("clicked()"), meRendererSetup.onNewPreset)
          QtCore.QObject.connect(self.deleteButton, QtCore.SIGNAL("clicked()"), meRendererSetup.onDeletePreset)
          QtCore.QObject.connect(self.lineName, QtCore.SIGNAL("editingFinished()"), meRendererSetup.onEditLabel)
          QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL("clicked()"), meRendererSetup.onSave)
        else :
          self.cancelButton.clicked.connect( meRendererSetup.close)
          self.okButton.clicked.connect( meRendererSetup.onSelect)
          self.listPreset.currentIndexChanged.connect( meRendererSetup.onIndexChanged)
          self.newButton.clicked.connect( meRendererSetup.onNewPreset)
          self.deleteButton.clicked.connect( meRendererSetup.onDeletePreset)
          self.lineName.editingFinished.connect( meRendererSetup.onEditLabel)
          self.saveButton.clicked.connect( meRendererSetup.onSave)
        
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
      meRendererSetup.setWindowTitle(QtModule.QApplication.translate("meRendererSetup", "Renderer preset setup", None))
      self.labelPreset.setText(QtModule.QApplication.translate("meRendererSetup", "Preset", None))
      self.newButton.setToolTip(QtModule.QApplication.translate("meRendererSetup", "Create new renderer preset", None))
      self.newButton.setText(QtModule.QApplication.translate("meRendererSetup", "New", None))
      self.deleteButton.setToolTip(QtModule.QApplication.translate("meRendererSetup", "Delete current renderer preset", None))
      self.deleteButton.setText(QtModule.QApplication.translate("meRendererSetup", "Delete", None))
      self.saveButton.setToolTip(QtModule.QApplication.translate("meRendererSetup", "Save current renderer preset", None))
      self.saveButton.setText(QtModule.QApplication.translate("meRendererSetup", "Save", None))
      self.cancelButton.setText(QtModule.QApplication.translate("meRendererSetup", "Cancel", None))
      self.okButton.setToolTip(QtModule.QApplication.translate("meRendererSetup", "Select current renderer preset", None))
      self.okButton.setText(QtModule.QApplication.translate("meRendererSetup", "Select", None))
      self.labelName.setText(QtModule.QApplication.translate("meRendererSetup", "Label", None))
      self.labelCmd.setText(QtModule.QApplication.translate("meRendererSetup", "Command", None))
      self.labelFlags.setText(QtModule.QApplication.translate("meRendererSetup", "Flags", None))
      self.tabs.setTabText(self.tabs.indexOf(self.tab1), QtModule.QApplication.translate("meRendererSetup", "Renderer", None))
      self.labelCompiler.setText(QtModule.QApplication.translate("meRendererSetup", " Compiler", None))
      self.labelShaderInfo.setText(QtModule.QApplication.translate("meRendererSetup", "SloInfo", None))
      self.labelDefines.setText(QtModule.QApplication.translate("meRendererSetup", "Defines", None))
      self.labelShaderExt.setText(QtModule.QApplication.translate("meRendererSetup", " Extension", None))
      self.tabs.setTabText(self.tabs.indexOf(self.tab2), QtModule.QApplication.translate("meRendererSetup", "Shaders", None))
      self.labelTexMake.setText(QtModule.QApplication.translate("meRendererSetup", "TexMake", None))
      self.labelTexInfo.setText(QtModule.QApplication.translate("meRendererSetup", " TexInfo", None))
      self.labelTexViewer.setText(QtModule.QApplication.translate("meRendererSetup", "Viewer", None))
      self.labelTexExt.setText(QtModule.QApplication.translate("meRendererSetup", " Extension", None))
      self.tabs.setTabText(self.tabs.indexOf(self.tab3), QtModule.QApplication.translate("meRendererSetup", "Textures", None))

