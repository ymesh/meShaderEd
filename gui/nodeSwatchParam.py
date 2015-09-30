"""

	nodeSwatchParam.py

"""
from core.mePyQt import QtCore, QtGui

from ui_nodeSwatchParam import Ui_NodeSwatchParam

import ui_settings as UI

if QtCore.QT_VERSION < 0x50000 :
	QtModule = QtGui
else :
	from core.mePyQt import QtWidgets
	QtModule = QtWidgets
	
#
# NodeSwatchParam
#
class NodeSwatchParam ( QtModule.QWidget ) :
	#
	# __init__
	#
	def __init__ ( self ) :
		#
		QtModule.QWidget.__init__ ( self )

		self.ui = Ui_NodeSwatchParam () 
		self.ui.setupUi ( self )

		self.buildGui ()
		self.updateGui ()
	#
	# buildGui
	#
	def buildGui ( self ) :
		#
		pass 
		#
	# updateGui
	#
	def updateGui ( self ) :
		#
		pass 
		#            