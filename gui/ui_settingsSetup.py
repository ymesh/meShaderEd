# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_settingsSetup.ui'
#
# Created: Wed Jul 18 14:26:06 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

if not usePyQt5 :
  QtModule = QtGui
else :
  from core.mePyQt import QtWidgets
  QtModule = QtWidgets
  
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingsSetup(object):
    def setupUi(self, SettingsSetup):
        SettingsSetup.setObjectName(_fromUtf8("SettingsSetup"))
        SettingsSetup.resize(376, 346)
        sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Preferred, QtModule.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsSetup.sizePolicy().hasHeightForWidth())
        SettingsSetup.setSizePolicy(sizePolicy)
        SettingsSetup.setMinimumSize(QtCore.QSize(0, 0))
        SettingsSetup.setMaximumSize(QtCore.QSize(16777215, 16777215))
        SettingsSetup.setSizeGripEnabled(False)
        self.verticalLayout_2 = QtModule.QVBoxLayout(SettingsSetup)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.grp_dirs = QtModule.QGroupBox(SettingsSetup)
        sizePolicy = QtModule.QSizePolicy(QtModule.QSizePolicy.Preferred, QtModule.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grp_dirs.sizePolicy().hasHeightForWidth())
        self.grp_dirs.setSizePolicy(sizePolicy)
        self.grp_dirs.setMinimumSize(QtCore.QSize(0, 0))
        self.grp_dirs.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.grp_dirs.setObjectName(_fromUtf8("grp_dirs"))
        self.verticalLayout = QtModule.QVBoxLayout(self.grp_dirs)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.hl_temp = QtModule.QHBoxLayout()
        self.hl_temp.setSizeConstraint(QtModule.QLayout.SetMinimumSize)
        self.hl_temp.setObjectName(_fromUtf8("hl_temp"))
        self.label_temp = QtModule.QLabel(self.grp_dirs)
        self.label_temp.setMinimumSize(QtCore.QSize(80, 0))
        self.label_temp.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_temp.setBaseSize(QtCore.QSize(60, 0))
        self.label_temp.setObjectName(_fromUtf8("label_temp"))
        self.hl_temp.addWidget(self.label_temp)
        self.lineEdit_temp = QtModule.QLineEdit(self.grp_dirs)
        self.lineEdit_temp.setObjectName(_fromUtf8("lineEdit_temp"))
        self.hl_temp.addWidget(self.lineEdit_temp)
        self.btn_temp_dir = QtModule.QToolButton(self.grp_dirs)
        self.btn_temp_dir.setObjectName(_fromUtf8("btn_temp_dir"))
        self.hl_temp.addWidget(self.btn_temp_dir)
        self.hl_temp.setStretch(1, 1)
        self.verticalLayout.addLayout(self.hl_temp)
        self.hl_inc = QtModule.QHBoxLayout()
        self.hl_inc.setObjectName(_fromUtf8("hl_inc"))
        self.label_inc = QtModule.QLabel(self.grp_dirs)
        self.label_inc.setMinimumSize(QtCore.QSize(80, 0))
        self.label_inc.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_inc.setObjectName(_fromUtf8("label_inc"))
        self.hl_inc.addWidget(self.label_inc)
        self.lineEdit_inc = QtModule.QLineEdit(self.grp_dirs)
        self.lineEdit_inc.setObjectName(_fromUtf8("lineEdit_inc"))
        self.hl_inc.addWidget(self.lineEdit_inc)
        self.btn_inc_dir = QtModule.QToolButton(self.grp_dirs)
        self.btn_inc_dir.setObjectName(_fromUtf8("btn_inc_dir"))
        self.hl_inc.addWidget(self.btn_inc_dir)
        self.hl_inc.setStretch(1, 1)
        self.verticalLayout.addLayout(self.hl_inc)
        self.hl_lib = QtModule.QHBoxLayout()
        self.hl_lib.setObjectName(_fromUtf8("hl_lib"))
        self.label_lib = QtModule.QLabel(self.grp_dirs)
        self.label_lib.setMinimumSize(QtCore.QSize(80, 0))
        self.label_lib.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_lib.setObjectName(_fromUtf8("label_lib"))
        self.hl_lib.addWidget(self.label_lib)
        self.lineEdit_lib = QtModule.QLineEdit(self.grp_dirs)
        self.lineEdit_lib.setObjectName(_fromUtf8("lineEdit_lib"))
        self.hl_lib.addWidget(self.lineEdit_lib)
        self.btn_lib_dir = QtModule.QToolButton(self.grp_dirs)
        self.btn_lib_dir.setObjectName(_fromUtf8("btn_lib_dir"))
        self.hl_lib.addWidget(self.btn_lib_dir)
        self.hl_lib.setStretch(1, 1)
        self.verticalLayout.addLayout(self.hl_lib)
        self.hl_nodes = QtModule.QHBoxLayout()
        self.hl_nodes.setObjectName(_fromUtf8("hl_nodes"))
        self.label_nodes = QtModule.QLabel(self.grp_dirs)
        self.label_nodes.setMinimumSize(QtCore.QSize(80, 0))
        self.label_nodes.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_nodes.setObjectName(_fromUtf8("label_nodes"))
        self.hl_nodes.addWidget(self.label_nodes)
        self.lineEdit_nodes = QtModule.QLineEdit(self.grp_dirs)
        self.lineEdit_nodes.setObjectName(_fromUtf8("lineEdit_nodes"))
        self.hl_nodes.addWidget(self.lineEdit_nodes)
        self.btn_nodes_dir = QtModule.QToolButton(self.grp_dirs)
        self.btn_nodes_dir.setObjectName(_fromUtf8("btn_nodes_dir"))
        self.hl_nodes.addWidget(self.btn_nodes_dir)
        self.hl_nodes.setStretch(1, 1)
        self.verticalLayout.addLayout(self.hl_nodes)
        self.hl_shaders = QtModule.QHBoxLayout()
        self.hl_shaders.setObjectName(_fromUtf8("hl_shaders"))
        self.label_shaders = QtModule.QLabel(self.grp_dirs)
        self.label_shaders.setMinimumSize(QtCore.QSize(80, 0))
        self.label_shaders.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_shaders.setObjectName(_fromUtf8("label_shaders"))
        self.hl_shaders.addWidget(self.label_shaders)
        self.lineEdit_shaders = QtModule.QLineEdit(self.grp_dirs)
        self.lineEdit_shaders.setObjectName(_fromUtf8("lineEdit_shaders"))
        self.hl_shaders.addWidget(self.lineEdit_shaders)
        self.btn_shaders_dir = QtModule.QToolButton(self.grp_dirs)
        self.btn_shaders_dir.setObjectName(_fromUtf8("btn_shaders_dir"))
        self.hl_shaders.addWidget(self.btn_shaders_dir)
        self.hl_shaders.setStretch(1, 1)
        self.verticalLayout.addLayout(self.hl_shaders)
        self.hl_textures = QtModule.QHBoxLayout()
        self.hl_textures.setObjectName(_fromUtf8("hl_textures"))
        self.label_textures = QtModule.QLabel(self.grp_dirs)
        self.label_textures.setMinimumSize(QtCore.QSize(80, 0))
        self.label_textures.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_textures.setObjectName(_fromUtf8("label_textures"))
        self.hl_textures.addWidget(self.label_textures)
        self.lineEdit_textures = QtModule.QLineEdit(self.grp_dirs)
        self.lineEdit_textures.setObjectName(_fromUtf8("lineEdit_textures"))
        self.hl_textures.addWidget(self.lineEdit_textures)
        self.btn_textures_dir = QtModule.QToolButton(self.grp_dirs)
        self.btn_textures_dir.setObjectName(_fromUtf8("btn_textures_dir"))
        self.hl_textures.addWidget(self.btn_textures_dir)
        self.hl_textures.setStretch(1, 1)
        self.verticalLayout.addLayout(self.hl_textures)
        self.hl_archives = QtModule.QHBoxLayout()
        self.hl_archives.setObjectName(_fromUtf8("hl_archives"))
        self.label_archives = QtModule.QLabel(self.grp_dirs)
        self.label_archives.setMinimumSize(QtCore.QSize(80, 0))
        self.label_archives.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_archives.setObjectName(_fromUtf8("label_archives"))
        self.hl_archives.addWidget(self.label_archives)
        self.lineEdit_archives = QtModule.QLineEdit(self.grp_dirs)
        self.lineEdit_archives.setObjectName(_fromUtf8("lineEdit_archives"))
        self.hl_archives.addWidget(self.lineEdit_archives)
        self.btn_archives_dir = QtModule.QToolButton(self.grp_dirs)
        self.btn_archives_dir.setObjectName(_fromUtf8("btn_archives_dir"))
        self.hl_archives.addWidget(self.btn_archives_dir)
        self.hl_archives.setStretch(1, 1)
        self.verticalLayout.addLayout(self.hl_archives)
        self.verticalLayout_2.addWidget(self.grp_dirs)
        spacerItem = QtModule.QSpacerItem(20, 20, QtModule.QSizePolicy.Minimum, QtModule.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox = QtModule.QDialogButtonBox(SettingsSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtModule.QDialogButtonBox.Cancel|QtModule.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SettingsSetup)
        if usePyQt4 :
          QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsSetup.accept)
          QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsSetup.reject)
          QtCore.QObject.connect(self.btn_lib_dir, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsSetup.onBrowseLibraryDir)
          QtCore.QObject.connect(self.btn_temp_dir, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsSetup.onBrowseTempDir)
          QtCore.QObject.connect(self.btn_inc_dir, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsSetup.onBrowseIncludesDir)
          QtCore.QObject.connect(self.btn_nodes_dir, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsSetup.onBrowseNodesDir)
          QtCore.QObject.connect(self.btn_shaders_dir, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsSetup.onBrowseShadersDir)
          QtCore.QObject.connect(self.btn_textures_dir, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsSetup.onBrowseTexturesDir)
          QtCore.QObject.connect(self.btn_archives_dir, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsSetup.onBrowseArchivesDir)
        else :
          self.buttonBox.accepted.connect( SettingsSetup.accept)
          self.buttonBox.rejected.connect( SettingsSetup.reject)
          self.btn_lib_dir.clicked.connect( SettingsSetup.onBrowseLibraryDir)
          self.btn_temp_dir.clicked.connect( SettingsSetup.onBrowseTempDir)
          self.btn_inc_dir.clicked.connect( SettingsSetup.onBrowseIncludesDir)
          self.btn_nodes_dir.clicked.connect( SettingsSetup.onBrowseNodesDir)
          self.btn_shaders_dir.clicked.connect( SettingsSetup.onBrowseShadersDir)
          self.btn_textures_dir.clicked.connect( SettingsSetup.onBrowseTexturesDir)
          self.btn_archives_dir.clicked.connect( SettingsSetup.onBrowseArchivesDir)
        QtCore.QMetaObject.connectSlotsByName(SettingsSetup)

    def retranslateUi(self, SettingsSetup):
        SettingsSetup.setWindowTitle(QtModule.QApplication.translate("SettingsSetup", "Settings Setup", None))
        self.grp_dirs.setTitle(QtModule.QApplication.translate("SettingsSetup", "Directories", None))
        self.label_temp.setText(QtModule.QApplication.translate("SettingsSetup", "Temp", None))
        self.btn_temp_dir.setText(QtModule.QApplication.translate("SettingsSetup", "...", None))
        self.label_inc.setText(QtModule.QApplication.translate("SettingsSetup", "Includes", None))
        self.btn_inc_dir.setText(QtModule.QApplication.translate("SettingsSetup", "...", None))
        self.label_lib.setText(QtModule.QApplication.translate("SettingsSetup", "Library", None))
        self.btn_lib_dir.setText(QtModule.QApplication.translate("SettingsSetup", "...", None))
        self.label_nodes.setText(QtModule.QApplication.translate("SettingsSetup", "Nodes", None))
        self.btn_nodes_dir.setText(QtModule.QApplication.translate("SettingsSetup", "...", None))
        self.label_shaders.setText(QtModule.QApplication.translate("SettingsSetup", "Shaders", None))
        self.btn_shaders_dir.setText(QtModule.QApplication.translate("SettingsSetup", "...", None))
        self.label_textures.setText(QtModule.QApplication.translate("SettingsSetup", "Textures", None))
        self.btn_textures_dir.setText(QtModule.QApplication.translate("SettingsSetup", "...", None))
        self.label_archives.setText(QtModule.QApplication.translate("SettingsSetup", "Archives", None))
        self.btn_archives_dir.setText(QtModule.QApplication.translate("SettingsSetup", "...", None))

