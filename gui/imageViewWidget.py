"""

	imageViewWidget.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui
from core.signal import Signal

#from PyQt4.QtCore import QDir, QString, QModelIndex
#from PyQt4.QtGui  import QFileSystemModel
#from PyQt4.QtGui  import QFileIconProvider

from ui_imageViewWidget import Ui_imageViewWidget

import gui.ui_settings as UI
from core.node import Node
from core.nodeLibrary import NodeLibrary

if  not usePyQt5 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
#
# ImageViewWidget
#
class ImageViewWidget ( QtModule.QWidget ) :
	#
	#  __init__
	#
	def __init__ ( self ) :
		#
		QtModule.QWidget.__init__ ( self )

		# This is always the same
		self.ui = Ui_imageViewWidget ()
		self.ui.setupUi ( self )

		self.ui.selector.setMinimumSize ( QtCore.QSize ( UI.COMBO_WIDTH, UI.COMBO_HEIGHT ) )
		self.ui.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )

		self.imageNodes = []

		#self.ui.treeView.setDragEnabled ( True )
		#self.ui.treeView.setRootIsDecorated( True )

		if usePyQt4 :
			QtCore.QObject.connect ( self.ui.imageArea, QtCore.SIGNAL ( 'mouseDoubleClickSignal' ), self.updateViewer )
			QtCore.QObject.connect ( self.ui.selector, QtCore.SIGNAL ( 'currentIndexChanged(int)' ), self.onViewerChanged )
		else :
			self.ui.imageArea.mouseDoubleClickSignal.connect ( self.updateViewer )
			self.ui.selector.currentIndexChanged.connect ( self.onViewerChanged )
		#QtCore.QObject.connect( self.ui, QtCore.SIGNAL( 'paramChanged()' ), self.onParamChanged )

		#self.updateGui()
		#self.emit( QtCore.SIGNAL( 'onGfxNodeParamChanged(QObject,QObject)' ), self, param.name )
	#
	# currentImageNode
	#
	def currentImageNode ( self ) :
		#
		gfxNode = None
		idx = self.ui.selector.currentIndex ()
		if len ( self.imageNodes ) > 0 :
			gfxNode = self.imageNodes [ idx ]
		return gfxNode
	#
	# addViewer
	#
	def addViewer ( self, gfxNode ) :
		#
		self.imageNodes.append ( gfxNode )
		self.ui.selector.addItem ( gfxNode.node.label )
	#
	# removeAllViewers
	#
	def removeAllViewers ( self ) :
		#
		self.imageNodes = []
		self.ui.selector.clear()
	#
	# removeViewer
	#
	def removeViewer ( self, gfxNode ) :
		#
		for i in range ( 0, len ( self.imageNodes ) ) :
			if gfxNode ==  self.imageNodes [ i ] :
				self.imageNodes.pop ( i )
				self.ui.selector.removeItem ( i )
				#QtCore.QObject.disconnect ( gfxNode.node, QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self.onNodeParamChanged )
				break
	#
	# onViewerChanged
	#
	def onViewerChanged ( self, idx ) :
		#
		if len ( self.imageNodes ) > 0 :
			print ">> ImageViewWidget.onViewerChanged to %s" % self.imageNodes [ idx ].node.label
			#QtCore.QObject.connect( self.imageNodes[ idx ].node, QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self.onNodeParamChanged )
			self.updateViewer ( compute = False )
	#
	# updateViewer
	#
	#@QtCore.pyqtSlot ()
	def updateViewer ( self, compute = True ) :
		#
		print ">> ImageViewWidget.updateViewer compute = %d" % compute
		RenderViewMode = False
		idx = self.ui.selector.currentIndex ()
		if len ( self.imageNodes ) > 0 :
			gfxNode = self.imageNodes [ idx ]
			print ">> ImageViewWidget.getImageName on %s" % gfxNode.node.label

			imageInputParam = gfxNode.node.getInputParamByName ( 'image' )
			if imageInputParam is not None :
				if gfxNode.node.isInputParamLinked ( imageInputParam ):
					link = gfxNode.node.inputLinks [ imageInputParam ]
					displayParam = link.srcNode.getInputParamByName ( 'DisplayDriver' )
					if displayParam is not None :
						print '>> Display driver = %s' % displayParam.value
						if displayParam.value != 'tiff' :
							RenderViewMode = True

			if compute :
				print '* compute '
				imageName = gfxNode.node.computeNode ()
			else :
				print '* use image '
				imageName = gfxNode.node.imageName

			print ">> ImageViewWidget: imageName = %s" % imageName

			if not RenderViewMode :
				self.ui.imageArea.setImage ( imageName )

			#imageParam = None
			#for param in gfxNode.node.inputParams :
			#  if param.name == 'image' :
			#    imageParam = param
			#    break
			#if imageParam is not None :
			#  print ">> ImageViewWidget: image = %s" % imageParam.value
			#  self.ui.imageArea.setImage ( imageParam.value )
	#
	# autoUpdate
	#
	def autoUpdate ( self ) : return self.ui.chk_auto.isChecked ()
	#
	# onNodeParamChanged
	#
	def onNodeParamChanged ( self, node, param ) :
		#
		print ">> ImageViewWidget.onNodeParamChanged %s %s" % ( node.label, param.name )
		if node == self.currentImageNode().node :
			self.updateViewer ()
	#
	# onNodeLabelChanged
	#
	def onNodeLabelChanged ( self, gfxNode, newLabel ) :
		#
		print ">> ImageViewWidget.onNodeLabelChanged %s %s" % ( gfxNode.node.label, newLabel )
		i = 0
		for i in range ( len ( self.imageNodes ) ) :
			if gfxNode ==  self.imageNodes [ i ] :
				self.ui.selector.setItemText ( i, newLabel )
				break
			i += 1

