"""

 linkWidget.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

from global_vars import app_global_vars, DEBUG_MODE
import gui.ui_settings as UI 
from paramWidget import ParamWidget 

if  not usePyQt5 :
    QtModule = QtGui
else :
    from core.mePyQt import QtWidgets
    QtModule = QtWidgets
#
# LinkWidget widgets for linked parameter
#
class LinkWidget ( ParamWidget ) :
    #
    # __init__
    #
    def __init__ ( self, param, gfxNode, ignoreSubtype = False, linkedParamsList = [] ) :
        #
        self.linkedParamsList = linkedParamsList
        ParamWidget.__init__ ( self, param, gfxNode, ignoreSubtype )
        
    #
    # buildGui
    #                 
    def buildGui ( self ) :
        #
        self.ui = Ui_LinkWidget ()    
        self.ui.setupUi ( self )
        
        #if DEBUG_MODE : print ">> LinkWidget.buildGui"
#
# Ui_LinkWidget
#
class Ui_LinkWidget ( object ) :
    #
    # setupUi
    #
    def setupUi ( self, LinkWidget ) :
        #
        self.widget = LinkWidget
        
        for ( linkNode, linkParam ) in self.widget.linkedParamsList :
            hl = QtModule.QHBoxLayout ()
            hl.setStretch ( 1, 0 )
             
            stringEdit = QtModule.QLineEdit ( LinkWidget )
            stringEdit.setEnabled ( False )
            
            stringEdit.setText ( linkNode.label + '.' + linkParam.label + ' (' + linkParam.name + ')' )
            
            stringEdit.setMinimumSize ( QtCore.QSize ( UI.LABEL_WIDTH, UI.HEIGHT ) ) # UI.EDIT_WIDTH
            stringEdit.setMaximumSize ( QtCore.QSize ( UI.MAX, UI.HEIGHT ) )
            
            btnSize = QtCore.QSize ( 20, 20 )
            sizePolicy = QtModule.QSizePolicy ( QtModule.QSizePolicy.Fixed, QtModule.QSizePolicy.Fixed )
            sizePolicy.setHorizontalStretch ( 20 )
            sizePolicy.setVerticalStretch ( 20 )
            
            selectButton = QtModule.QToolButton ()
            selectButton.setText ( '>' )
            sizePolicy.setHeightForWidth ( selectButton.sizePolicy().hasHeightForWidth() )
            selectButton.setSizePolicy ( sizePolicy )
            selectButton.setMaximumSize ( btnSize )
            selectButton.setAutoRaise ( False )
            selectButton.setToolTip ( 'Go to connection' )
            #selectButton.setIconSize ( QtCore.QSize ( 16, 16 ) )
            selectButton.setObjectName ( 'selectButton' )
            #QtCore.QObject.connect ( self.selectButton, QtCore.SIGNAL ( 'clicked()' ), self.onRemoveItem )
            selectButton.setEnabled ( False )
            
            removeButton = QtModule.QToolButton ()
            sizePolicy.setHeightForWidth ( removeButton.sizePolicy().hasHeightForWidth() )
            removeButton.setSizePolicy ( sizePolicy )
            removeButton.setMaximumSize ( btnSize )
            del_icon = QtGui.QIcon ()
            del_icon.addPixmap ( QtGui.QPixmap ( ':/edit_icons/resources/del.png' ), QtGui.QIcon.Normal, QtGui.QIcon.On )
            removeButton.setIcon ( del_icon )
            removeButton.setAutoRaise ( False )
            removeButton.setToolTip ( 'Remove connection' )
            #removeButton.setIconSize ( QtCore.QSize ( 16, 16 ) )
            removeButton.setObjectName ( 'removeButton' )
            #QtCore.QObject.connect ( self.removeButton, QtCore.SIGNAL ( 'clicked()' ), self.onRemoveItem )
            removeButton.setEnabled ( False )
        
            hl.addWidget ( stringEdit )
            hl.addWidget ( selectButton )
            hl.addWidget ( removeButton )
            
            self.widget.param_vl.addLayout ( hl )
        
        QtCore.QMetaObject.connectSlotsByName ( LinkWidget )
        self.connectSignals ( LinkWidget )
    #
    # connectSignals
    #
    def connectSignals ( self, LinkWidget ) :
        #
        pass
        #LinkWidget.connect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
    #
    # disconnectSignals
    #
    def disconnectSignals ( self, LinkWidget ) :
        #
        pass
        #LinkWidget.disconnect ( self.stringEdit, QtCore.SIGNAL ( 'editingFinished()' ), self.onStringEditEditingFinished )
    #
    # updateGui
    #
    def updateGui ( self, value ) :
        # 
        pass
        #print ">> LinkWidget.updateGui",  value
        #if self.linkNode is not None :
        #  self.stringEdit.setText ( self.linkNode.label + '.' + self.linkParam.label + ' (' + self.linkParam.name + ')' )