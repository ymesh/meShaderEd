"""

 PointWidget.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

import gui.ui_settings as UI
from global_vars import VALID_RSL_SPACES 
from paramWidget import ParamWidget

if  not usePyQt5 :
    QtModule = QtGui
else :
    from core.mePyQt import QtWidgets
    QtModule = QtWidgets
#
# PointWidget
#
class PointWidget ( ParamWidget ) :
    #
    # PointWidget
    #
    def buildGui ( self ) :
        #
        if self.param.isArray () :
            self.ui = Ui_PointWidget_array () 
        else :
            self.ui = Ui_PointWidget_field () 
        self.ui.setupUi ( self )
#
# Ui_PointWidget_field
#
class Ui_PointWidget_field ( object ) :
    #
    # setupUi
    #
    def setupUi ( self, PointWidget ) :
        #
        self.widget = PointWidget
        
        self.floatEdit0 = QtModule.QLineEdit ( PointWidget )
        self.floatEdit1 = QtModule.QLineEdit ( PointWidget )
        self.floatEdit2 = QtModule.QLineEdit ( PointWidget )
        
        self.floatEdit0.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit1.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit2.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.floatEdit0.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit1.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit2.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.selector = QtModule.QComboBox ( PointWidget )
        self.selector.setEditable ( False )
        self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
        
        for label in VALID_RSL_SPACES :
            self.selector.addItem ( label )
        if self.widget.param.space != None :
            self.selector.setCurrentIndex ( self.selector.findText ( self.widget.param.space ) )  
        
        sp = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
        
        hl = QtModule.QHBoxLayout ()
        hl.addWidget ( self.floatEdit0 )
        hl.addWidget ( self.floatEdit1 )
        hl.addWidget ( self.floatEdit2 )
        hl.addWidget ( self.selector )
        hl.addItem ( sp )
        
        self.widget.param_vl.addLayout ( hl )
        
        self.connectSignals ( PointWidget )
        QtCore.QMetaObject.connectSlotsByName ( PointWidget )
    #
    # connectSignals
    #
    def connectSignals ( self, PointWidget ) :
        #
        if usePyQt4 :
            PointWidget.connect ( self.floatEdit0, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            PointWidget.connect ( self.floatEdit1, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            PointWidget.connect ( self.floatEdit2, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            PointWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
        else :
            self.floatEdit0.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit1.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit2.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.selector.activated.connect ( self.onCurrentIndexChanged ) 
    #
    # disconnectSignals
    #
    def disconnectSignals ( self, PointWidget ) :
        #
        if usePyQt4 :
            PointWidget.disconnect ( self.floatEdit0, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            PointWidget.disconnect ( self.floatEdit1, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            PointWidget.disconnect ( self.floatEdit2, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            PointWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
        else :
            self.floatEdit0.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit1.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit2.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.selector.activated.disconnect ( self.onCurrentIndexChanged )  
    #
    # onFloatEditEditingFinished
    #
    def onFloatEditEditingFinished ( self ) :
        #
        floatStr0 = self.floatEdit0.text ()
        floatStr1 = self.floatEdit1.text ()
        floatStr2 = self.floatEdit2.text ()
        if usePyQt4 :
            f0 = floatStr0.toFloat ()[0]
            f1 = floatStr1.toFloat ()[0] 
            f2 = floatStr2.toFloat ()[0]
        else :
            f0 = float ( floatStr0 )
            f1 = float ( floatStr1 )
            f2 = float ( floatStr2 )
        
        self.widget.param.setValue ( [ f0, f1, f2 ] )
    #
    # onCurrentIndexChanged
    #
    def onCurrentIndexChanged ( self, idx ) :
        #
        space = str ( self.selector.currentText () ) 
        if space == 'current' : space = None
        self.widget.param.space = space
    #
    # updateGui
    #
    def updateGui ( self, value ) : 
        #
        if usePyQt4 :
            self.floatEdit0.setText ( QtCore.QString.number( value [0], 'f', 3 ) )
            self.floatEdit1.setText ( QtCore.QString.number( value [1], 'f', 3 ) )
            self.floatEdit2.setText ( QtCore.QString.number( value [2], 'f', 3 ) )
        else :
            self.floatEdit0.setText ( str ( value [0] ) )
            self.floatEdit1.setText ( str ( value [1] ) )
            self.floatEdit2.setText ( str ( value [2] ) )
#
# Ui_PointWidget_array
#
class Ui_PointWidget_array ( object ) :
    #
    # setupUi
    #
    def setupUi ( self, PointWidget ) :
        #
        self.widget = PointWidget
        self.labels = []
        self.controls = []
        
        font = QtGui.QFont ()
        labelFontMetric = QtGui.QFontMetricsF ( font )
        label_wi = 0
        char_wi = labelFontMetric.width ( 'x' )
        array_size = self.widget.param.arraySize
        if array_size > 0 :
            label_wi =  char_wi * ( len ( str ( array_size - 1 ) ) + 2 ) # [0]
        
        for i in range ( self.widget.param.arraySize ) :
            self.labels.append ( QtModule.QLabel ( PointWidget ) )
            self.labels [ i ].setMinimumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
            self.labels [ i ].setMaximumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
            self.labels [ i ].setAlignment ( QtCore.Qt.AlignRight )
            self.labels [ i ].setText ( '[' + str ( i ) + ']' )
            
            elem = []
            
            elem.append ( QtModule.QLineEdit( PointWidget ) )
            elem.append ( QtModule.QLineEdit( PointWidget ) )
            elem.append ( QtModule.QLineEdit( PointWidget ) )
            elem.append ( QtModule.QComboBox ( PointWidget ) )
            
            elem [ 0 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 1 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 2 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            
            elem [ 0 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 1 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 2 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            
            elem [ 3 ].setEditable ( False )
            elem [ 3 ].setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
        
            for label in VALID_RSL_SPACES :
                elem [ 3 ].addItem ( label )
            space = self.widget.param.spaceArray [ i ]
            if space != None :
                elem [ 3 ].setCurrentIndex ( elem [ 3 ].findText ( space ) ) 
            
            self.controls.append ( elem )
            
            sp = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
            
            hl = QtModule.QHBoxLayout ()
            hl.addWidget ( self.labels [ i ] )
            hl.addWidget ( elem [ 0 ] )
            hl.addWidget ( elem [ 1 ] )
            hl.addWidget ( elem [ 2 ] )
            hl.addWidget ( elem [ 3 ] )
            hl.addItem ( sp )
            self.widget.param_vl.addLayout ( hl )
        
        self.connectSignals ( PointWidget )
        QtCore.QMetaObject.connectSlotsByName ( PointWidget )
    #
    # connectSignals
    #
    def connectSignals ( self, PointWidget ) :
        #
        for i in range ( self.widget.param.arraySize ) :
            if usePyQt4 :
                PointWidget.connect ( self.controls [ i ][0], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                PointWidget.connect ( self.controls [ i ][1], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                PointWidget.connect ( self.controls [ i ][2], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                PointWidget.connect ( self.controls [ i ][3], QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
            else :
                self.controls [ i ][0].editingFinished.connect ( self.onFloatEditEditingFinished )
                self.controls [ i ][1].editingFinished.connect ( self.onFloatEditEditingFinished )
                self.controls [ i ][2].editingFinished.connect ( self.onFloatEditEditingFinished )
                self.controls [ i ][3].activated.connect ( self.onCurrentIndexChanged ) 
    #
    # disconnectSignals
    #
    def disconnectSignals ( self, PointWidget ) :
        #
        for i in range ( self.widget.param.arraySize ) :
            if usePyQt4 :
                PointWidget.disconnect ( self.controls [ i ][0], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                PointWidget.disconnect ( self.controls [ i ][1], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                PointWidget.disconnect ( self.controls [ i ][2], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                PointWidget.disconnect ( self.controls [ i ][3], QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
            else :
                self.controls [ i ][0].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                self.controls [ i ][1].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                self.controls [ i ][2].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                self.controls [ i ][3].activated.disconnect ( self.onCurrentIndexChanged )  
    #
    # onFloatEditEditingFinished
    #
    def onFloatEditEditingFinished ( self ) :
        #
        arrayValue = []
        for i in range ( self.widget.param.arraySize ) :
            floatStr0 = self.controls [ i ][0].text () 
            floatStr1 = self.controls [ i ][1].text () 
            floatStr2 = self.controls [ i ][2].text () 
            if usePyQt4 :
                f0 = floatStr0.toFloat ()[0]
                f1 = floatStr1.toFloat ()[0] 
                f2 = floatStr2.toFloat ()[0]
            else :
                f0 = float ( floatStr0 )
                f1 = float ( floatStr1 )
                f2 = float ( floatStr2 )
            arrayValue.append ( [ f0, f1, f2 ] )
            
        self.widget.param.setValue ( arrayValue )
    #
    # onCurrentIndexChanged
    #
    def onCurrentIndexChanged ( self, idx ) :
        #
        # TODO: spaces should be stored in separate spaces array
        #
        for i in range ( self.widget.param.arraySize ) :
            space = str ( self.controls [ i ][3].currentText () ) 
            if space == 'current' : space = None
            self.widget.param.space = space
    #
    # updateGui
    #
    def updateGui ( self, value ) : 
        #
        for i in range ( self.widget.param.arraySize ) :
            if usePyQt4 :
                self.controls [ i ][0].setText ( QtCore.QString.number( value [ i ][0], 'f', 3 ) )
                self.controls [ i ][1].setText ( QtCore.QString.number( value [ i ][1], 'f', 3 ) )
                self.controls [ i ][2].setText ( QtCore.QString.number( value [ i ][2], 'f', 3 ) )
            else :
                self.controls [ i ][0].setText ( str ( value [ i ][0] ) )
                self.controls [ i ][1].setText ( str ( value [ i ][1] ) )
                self.controls [ i ][2].setText ( str ( value [ i ][2] ) )
