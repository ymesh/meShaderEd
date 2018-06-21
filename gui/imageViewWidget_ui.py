# -*- coding: utf-8 -*-

from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets

class Ui_imageViewWidget ( object ) :
	#
	def setupUi ( self, imageViewWidget ) :
		#
		imageViewWidget.setObjectName ( "imageViewWidget" )
		imageViewWidget.setWindowTitle ( "ImageView" )
		imageViewWidget.resize ( 480, 340 )
		
		self.gridLayout = QtModule.QGridLayout ( imageViewWidget )
		self.gridLayout.setContentsMargins  ( 4, 4, 4, 4 )
		self.gridLayout.setHorizontalSpacing ( 4 )
		self.gridLayout.setVerticalSpacing ( 2 )
		
		self.horizontalLayout = QtModule.QHBoxLayout ()
		self.horizontalLayout.setSpacing ( 8 )
		self.horizontalLayout.setContentsMargins ( 0, -1, 0, -1 )
		
		self.label = QtModule.QLabel (  "Node", imageViewWidget )
		self.horizontalLayout.addWidget ( self.label )
		
		self.selector = QtModule.QComboBox ( imageViewWidget )
		self.selector.setMinimumSize ( QtCore.QSize ( 120, 20 ) )
		self.selector.setMaximumSize ( QtCore.QSize ( 16777215, 20 ) )
		self.selector.setFrame ( True )
		self.horizontalLayout.addWidget ( self.selector )
		
		self.btn_reset = QtModule.QToolButton (imageViewWidget )
		self.btn_reset.setText (  "1:1" )
		self.btn_reset.setToolTip ( "Reset zoom" )
		self.horizontalLayout.addWidget ( self.btn_reset )

		spacerItem = QtModule.QSpacerItem (70, 20, QtModule.QSizePolicy.Expanding, QtModule.QSizePolicy.Minimum )
		self.horizontalLayout.addItem ( spacerItem )
		
		self.chk_auto = QtModule.QCheckBox (  "auto", imageViewWidget )
		self.horizontalLayout.addWidget ( self.chk_auto )
		
		self.btn_render = QtModule.QPushButton ( "Update", imageViewWidget )
		self.btn_render.setMaximumSize ( QtCore.QSize ( 16777215, 20 ) )
		self.horizontalLayout.addWidget ( self.btn_render )

		self.horizontalLayout.setStretch ( 3, 1 )
		self.gridLayout.addLayout ( self.horizontalLayout, 0, 0, 1, 1 )
		
		self.imageArea = ImageView ( imageViewWidget )
		self.gridLayout.addWidget ( self.imageArea, 1, 0, 1, 1 )
		self.gridLayout.setRowStretch ( 1, 1 )

		if  usePyQt4 :
			QtCore.QObject.connect ( self.btn_render, QtCore.SIGNAL( "clicked()" ), imageViewWidget.updateViewer )
			QtCore.QObject.connect ( self.btn_reset, QtCore.SIGNAL( "clicked()" ), self.imageArea.resetZoom )
		else :
			self.btn_render.clicked.connect ( imageViewWidget.updateViewer)
			self.btn_reset.clicked.connect ( self.imageArea.resetZoom)
		
		QtCore.QMetaObject.connectSlotsByName ( imageViewWidget )

from gfx.imageView import ImageView
