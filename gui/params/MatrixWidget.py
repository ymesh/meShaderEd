"""

 MatrixWidget.py

"""
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

import gui.ui_settings as UI 
from paramWidget import ParamWidget
from global_vars import VALID_RSL_SPACES

if  not usePyQt5 :
    QtModule = QtGui
else :
    from core.mePyQt import QtWidgets
    QtModule = QtWidgets
#
# MatrixWidget
#
class MatrixWidget ( ParamWidget ) :
    #
    # buildGui
    #
    def buildGui ( self ) :
        #
        if self.param.isArray () :
            self.ui = Ui_MatrixWidget_array () 
        else :
            self.ui = Ui_MatrixWidget_field () 
        self.ui.setupUi ( self )
#
# Ui_MatrixWidget_field
# 
class Ui_MatrixWidget_field ( object ) :
    #
    # setupUi
    #
    def setupUi ( self, MatrixWidget ) :
        #
        self.widget = MatrixWidget
        
        self.floatEdit0 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit1 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit2 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit3 = QtModule.QLineEdit( MatrixWidget )
        
        self.floatEdit4 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit5 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit6 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit7 = QtModule.QLineEdit( MatrixWidget )
        
        self.floatEdit8 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit9 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit10 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit11 = QtModule.QLineEdit( MatrixWidget )
        
        self.floatEdit12 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit13 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit14 = QtModule.QLineEdit( MatrixWidget )
        self.floatEdit15 = QtModule.QLineEdit( MatrixWidget )
        
        
        self.floatEdit0.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
        self.floatEdit1.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit2.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit3.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.floatEdit4.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
        self.floatEdit5.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit6.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit7.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.floatEdit8.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
        self.floatEdit9.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit10.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit11.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.floatEdit12.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
        self.floatEdit13.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit14.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit15.setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        
        self.floatEdit0.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit1.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit2.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit3.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.floatEdit4.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit5.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit6.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit7.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.floatEdit8.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit9.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit10.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit11.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.floatEdit12.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit13.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit14.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        self.floatEdit15.setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
        
        self.selector = QtModule.QComboBox ( MatrixWidget )
        self.selector.setEditable ( False )
        self.selector.setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
        
        for label in VALID_RSL_SPACES :
            self.selector.addItem ( label )
        if self.widget.param.space != None :
            self.selector.setCurrentIndex( self.selector.findText ( self.widget.param.space ) )
        
        spacer0 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
        
        hl = QtModule.QHBoxLayout ()
        hl.addWidget ( self.selector )
        hl.addItem ( spacer0 )
        self.widget.param_vl.addLayout ( hl )
        
        hl1 = QtModule.QHBoxLayout ()
        hl1.setSpacing ( UI.SPACING )
        #if usePyQt4 :
        hl1.setContentsMargins ( 0, 0, 0, 0 )
        hl1.addWidget ( self.floatEdit0 )
        hl1.addWidget ( self.floatEdit1 )
        hl1.addWidget ( self.floatEdit2 )
        hl1.addWidget ( self.floatEdit3 )
        spacer1 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
        hl1.addItem ( spacer1 )
        
        self.widget.param_vl.addLayout ( hl1 )
        
        hl2 = QtModule.QHBoxLayout ()
        hl2.setSpacing ( UI.SPACING )
        #if usePyQt4 :
        hl2.setContentsMargins ( 0, 0, 0, 0 )
        hl2.addWidget ( self.floatEdit4 )
        hl2.addWidget ( self.floatEdit5 )
        hl2.addWidget ( self.floatEdit6 )
        hl2.addWidget ( self.floatEdit7 )
        spacer2 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
        hl2.addItem ( spacer2 )
        
        self.widget.param_vl.addLayout ( hl2 )
        
        hl3 = QtModule.QHBoxLayout ()
        hl3.setSpacing ( UI.SPACING )
        #if usePyQt4 :
        hl3.setContentsMargins ( 0, 0, 0, 0 )
        hl3.addWidget ( self.floatEdit8 )
        hl3.addWidget ( self.floatEdit9 )
        hl3.addWidget ( self.floatEdit10 )
        hl3.addWidget ( self.floatEdit11 )
        spacer3 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
        hl3.addItem ( spacer3 )
        
        self.widget.param_vl.addLayout ( hl3 )
        
        hl4 = QtModule.QHBoxLayout ()
        hl4.setSpacing ( UI.SPACING )
        #if usePyQt4 :
        hl4.setContentsMargins ( 0, 0, 0, 0 )
        hl4.addWidget ( self.floatEdit12 )
        hl4.addWidget ( self.floatEdit13 )
        hl4.addWidget ( self.floatEdit14 )
        hl4.addWidget ( self.floatEdit15 )
        spacer4 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
        hl4.addItem ( spacer4 )
        
        self.widget.param_vl.addLayout ( hl4 )
        
        self.connectSignals ( MatrixWidget )
        QtCore.QMetaObject.connectSlotsByName ( MatrixWidget )
    #
    # connectSignals
    #
    def connectSignals ( self, MatrixWidget ) :
        #
        if usePyQt4 :
            MatrixWidget.connect ( self.floatEdit0, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit1, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit2, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit3, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            
            MatrixWidget.connect ( self.floatEdit4, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit5, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit6, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit7, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            
            MatrixWidget.connect ( self.floatEdit8, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit9, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit10, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit11, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            
            MatrixWidget.connect ( self.floatEdit12, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit13, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit14, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.connect ( self.floatEdit15, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
        
            MatrixWidget.connect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged ) 
        else :
            self.floatEdit0.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit1.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit2.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit3.editingFinished.connect ( self.onFloatEditEditingFinished )
            
            self.floatEdit4.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit5.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit6.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit7.editingFinished.connect ( self.onFloatEditEditingFinished )
            
            self.floatEdit8.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit9.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit10.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit11.editingFinished.connect ( self.onFloatEditEditingFinished )
            
            self.floatEdit12.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit13.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit14.editingFinished.connect ( self.onFloatEditEditingFinished )
            self.floatEdit15.editingFinished.connect ( self.onFloatEditEditingFinished )
        
            self.selector.activated.connect ( self.onCurrentIndexChanged ) 
    #
    # disconnectSignals
    #
    def disconnectSignals ( self, MatrixWidget ) :
        #
        if usePyQt4 :
            MatrixWidget.disconnect ( self.floatEdit0, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit1, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit2, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit3, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            
            MatrixWidget.disconnect ( self.floatEdit4, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit5, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit6, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit7, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            
            MatrixWidget.disconnect ( self.floatEdit8, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit9, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit10, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit11, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            
            MatrixWidget.disconnect ( self.floatEdit12, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit13, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit14, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            MatrixWidget.disconnect ( self.floatEdit15, QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            
            MatrixWidget.disconnect ( self.selector, QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
        else :
            self.floatEdit0.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit1.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit2.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit3.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            
            self.floatEdit4.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit5.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit6.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit7.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            
            self.floatEdit8.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit9.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit10.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit11.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            
            self.floatEdit12.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit13.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit14.editingFinished.disconnect ( self.onFloatEditEditingFinished )
            self.floatEdit15.editingFinished.disconnect ( self.onFloatEditEditingFinished )
        
            self.selector.activated.connect ( self.onCurrentIndexChanged ) 
    #
    # onFloatEditEditingFinished
    #
    def onFloatEditEditingFinished ( self ) :
        #
        floatStr0 = self.floatEdit0.text ()
        floatStr1 = self.floatEdit1.text ()
        floatStr2 = self.floatEdit2.text ()
        floatStr3 = self.floatEdit3.text ()
        if usePyQt4 :
            f0 = floatStr0.toFloat ()[0]
            f1 = floatStr1.toFloat ()[0] 
            f2 = floatStr2.toFloat ()[0]
            f3 = floatStr3.toFloat ()[0]
        else :
            f0 = float ( floatStr0 )
            f1 = float ( floatStr1 )
            f2 = float ( floatStr2 )
            f3 = float ( floatStr3 )
         
        floatStr0 = self.floatEdit4.text ()
        floatStr1 = self.floatEdit5.text ()
        floatStr2 = self.floatEdit6.text ()
        floatStr3 = self.floatEdit7.text ()
        if usePyQt4 :
            f4 = floatStr0.toFloat ()[0]
            f5 = floatStr1.toFloat ()[0] 
            f6 = floatStr2.toFloat ()[0]
            f7 = floatStr3.toFloat ()[0]
        else :
            f4 = float ( floatStr0 )
            f5 = float ( floatStr1 )
            f6 = float ( floatStr2 )
            f7 = float ( floatStr3 )
        
        floatStr0 = self.floatEdit8.text ()
        floatStr1 = self.floatEdit9.text ()
        floatStr2 = self.floatEdit10.text ()
        floatStr3 = self.floatEdit11.text ()
        if usePyQt4 :
            f8 = floatStr0.toFloat ()[0]
            f9 = floatStr1.toFloat ()[0] 
            f10 = floatStr2.toFloat ()[0]
            f11 = floatStr3.toFloat ()[0]
        else :
            f8  = float ( floatStr0 ) 
            f9  = float ( floatStr1 ) 
            f10 = float ( floatStr2 ) 
            f11 = float ( floatStr3 ) 
        
        floatStr0 = self.floatEdit12.text ()
        floatStr1 = self.floatEdit13.text ()
        floatStr2 = self.floatEdit14.text ()
        floatStr3 = self.floatEdit15.text ()
        if usePyQt4 :
            f12 = floatStr0.toFloat ()[0]
            f13 = floatStr1.toFloat ()[0] 
            f14 = floatStr2.toFloat ()[0]
            f15 = floatStr3.toFloat ()[0]
        else :
            f12 = float ( floatStr0 )
            f13 = float ( floatStr1 )
            f14 = float ( floatStr2 )
            f15 = float ( floatStr3 )
        
        self.widget.param.setValue ( [ [f0,f1,f2,f3], [f4,f5,f6,f7], [f8,f9,f10,f11], [f12,f13,f14,f15] ] )
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
    # value  = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]   
    #      
    def updateGui ( self, value ) :
        #
        #print ( '>>> MatrixWidget_field.updateGui' )
        if usePyQt4 :
            self.floatEdit0.setText  ( QtCore.QString.number ( float ( value [0][0] ), 'f', 3 ) )
            self.floatEdit1.setText  ( QtCore.QString.number ( float ( value [0][1] ), 'f', 3 ) )
            self.floatEdit2.setText  ( QtCore.QString.number ( float ( value [0][2] ), 'f', 3 ) )
            self.floatEdit3.setText  ( QtCore.QString.number ( float ( value [0][3] ), 'f', 3 ) )
            
            self.floatEdit4.setText  ( QtCore.QString.number ( float ( value [1][0] ), 'f', 3 ) )
            self.floatEdit5.setText  ( QtCore.QString.number ( float ( value [1][1] ), 'f', 3 ) )
            self.floatEdit6.setText  ( QtCore.QString.number ( float ( value [1][2] ), 'f', 3 ) )
            self.floatEdit7.setText  ( QtCore.QString.number ( float ( value [1][3] ), 'f', 3 ) )
            
            self.floatEdit8.setText  ( QtCore.QString.number ( float ( value [2][0] ), 'f', 3 ) )
            self.floatEdit9.setText  ( QtCore.QString.number ( float ( value [2][1] ), 'f', 3 ) )
            self.floatEdit10.setText ( QtCore.QString.number ( float ( value [2][2] ), 'f', 3 ) )
            self.floatEdit11.setText ( QtCore.QString.number ( float ( value [2][3] ), 'f', 3 ) )
            
            self.floatEdit12.setText ( QtCore.QString.number ( float ( value [3][0] ), 'f', 3 ) )
            self.floatEdit13.setText ( QtCore.QString.number ( float ( value [3][1] ), 'f', 3 ) )
            self.floatEdit14.setText ( QtCore.QString.number ( float ( value [3][2] ), 'f', 3 ) )
            self.floatEdit15.setText ( QtCore.QString.number ( float ( value [3][3] ), 'f', 3 ) )
        else :
            self.floatEdit0.setText  ( str ( value [0][0] ) )
            self.floatEdit1.setText  ( str ( value [0][1] ) )
            self.floatEdit2.setText  ( str ( value [0][2] ) )
            self.floatEdit3.setText  ( str ( value [0][3] ) )
            
            self.floatEdit4.setText  ( str ( value [1][0] ) )
            self.floatEdit5.setText  ( str ( value [1][1] ) )
            self.floatEdit6.setText  ( str ( value [1][2] ) )
            self.floatEdit7.setText  ( str ( value [1][3] ) )
            
            self.floatEdit8.setText  ( str ( value [2][0] ) )
            self.floatEdit9.setText  ( str ( value [2][1] ) )
            self.floatEdit10.setText ( str ( value [2][2] ) )
            self.floatEdit11.setText ( str ( value [2][3] ) )
            
            self.floatEdit12.setText ( str ( value [3][0] ) )
            self.floatEdit13.setText ( str ( value [3][1] ) )
            self.floatEdit14.setText ( str ( value [3][2] ) )
            self.floatEdit15.setText ( str ( value [3][3] ) )
#
# Ui_MatrixWidget_array
# 
class Ui_MatrixWidget_array ( object ) :
    #
    # setupUi
    #
    def setupUi ( self, MatrixWidget ) :
        #
        self.widget = MatrixWidget
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
            self.labels.append ( QtModule.QLabel ( MatrixWidget ) )
            self.labels [ i ].setMinimumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
            self.labels [ i ].setMaximumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
            self.labels [ i ].setAlignment ( QtCore.Qt.AlignRight )
            self.labels [ i ].setText ( '[' + str ( i ) + ']' )
            
            empty_label =  QtModule.QLabel ( MatrixWidget )
            empty_label.setMinimumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
            empty_label.setMaximumSize ( QtCore.QSize ( label_wi, UI.HEIGHT ) )
            empty_label.setAlignment ( QtCore.Qt.AlignRight )
            empty_label.setText ( ' ' )
            
            elem = []
            
            elem.append ( QtModule.QComboBox ( MatrixWidget ) )
            elem [ 0 ].setEditable ( False )
            elem [ 0 ].setMaximumSize ( QtCore.QSize( UI.MAX, UI.COMBO_HEIGHT ) )
            
            for label in VALID_RSL_SPACES :
                elem [ 0 ].addItem ( label )
            space = self.widget.param.spaceArray [ i ]
            if space != None :
                elem [ 0 ].setCurrentIndex( elem [ 0 ].findText ( space ) )
                
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            elem.append ( QtModule.QLineEdit( MatrixWidget ) )
            
            
            elem [ 1  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
            elem [ 2  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 3  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 4  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            
            elem [ 5  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
            elem [ 6  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 7  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 8  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            
            elem [ 9  ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
            elem [ 10 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 11 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 12 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            
            elem [ 13 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) ) 
            elem [ 14 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 15 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 16 ].setMinimumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            
            
            elem [ 1  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 2  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 3  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 4  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
                       
            elem [ 5  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 6  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 7  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 8  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
                       
            elem [ 9  ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 10 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 11 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 12 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
                       
            elem [ 13 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 14 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 15 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            elem [ 16 ].setMaximumSize ( QtCore.QSize ( UI.FIELD_WIDTH, UI.HEIGHT ) )
            
            self.controls.append ( elem )
            
            spacer0 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
            
            hl = QtModule.QHBoxLayout ()
            hl.addWidget ( self.labels [ i ] ) # array index
            hl.addWidget ( elem [ 0 ] ) # space selector
            hl.addItem ( spacer0 )
            
            self.widget.param_vl.addLayout ( hl )
            
            hl1 = QtModule.QHBoxLayout ()
            hl1.setSpacing ( UI.SPACING )
            hl1.setContentsMargins ( 0, 0, 0, 0 )
            hl1.addWidget ( empty_label ) 
            hl1.addWidget ( elem [ 1 ] )
            hl1.addWidget ( elem [ 2 ] )
            hl1.addWidget ( elem [ 3 ] )
            hl1.addWidget ( elem [ 4 ] )
            spacer1 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
            hl1.addItem ( spacer1 )
            
            self.widget.param_vl.addLayout ( hl1 )
            
            hl2 = QtModule.QHBoxLayout ()
            hl2.setSpacing ( UI.SPACING )
            hl2.setContentsMargins ( 0, 0, 0, 0 )
            hl2.addWidget ( empty_label ) 
            hl2.addWidget ( elem [ 5 ] )  
            hl2.addWidget ( elem [ 6 ] )  
            hl2.addWidget ( elem [ 7 ] )  
            hl2.addWidget ( elem [ 8 ] )  
            spacer2 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
            hl2.addItem ( spacer2 )
            
            self.widget.param_vl.addLayout ( hl2 )
            
            hl3 = QtModule.QHBoxLayout ()
            hl3.setSpacing ( UI.SPACING )
            hl3.setContentsMargins ( 0, 0, 0, 0 )
            hl3.addWidget ( empty_label ) 
            hl3.addWidget ( elem [ 9 ]  )
            hl3.addWidget ( elem [ 10 ] )
            hl3.addWidget ( elem [ 11 ] )
            hl3.addWidget ( elem [ 12 ] )
            spacer3 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
            hl3.addItem ( spacer3 )
            
            self.widget.param_vl.addLayout ( hl3 )
            
            hl4 = QtModule.QHBoxLayout ()
            hl4.setSpacing ( UI.SPACING )
            hl4.setContentsMargins ( 0, 0, 0, 0 )
            hl4.addWidget ( empty_label ) 
            hl4.addWidget ( elem [ 13 ] )
            hl4.addWidget ( elem [ 14 ] )
            hl4.addWidget ( elem [ 15 ] )
            hl4.addWidget ( elem [ 16 ] )
            spacer4 = QtModule.QSpacerItem ( 0, 0, UI.SP_EXPAND, UI.SP_MIN )
            hl4.addItem ( spacer4 )
            
            self.widget.param_vl.addLayout ( hl4 )
        
        self.connectSignals ( MatrixWidget )
        QtCore.QMetaObject.connectSlotsByName ( MatrixWidget )
    #
    # connectSignals
    #
    def connectSignals ( self, MatrixWidget ) :
        #
        for i in range ( self.widget.param.arraySize ) :
            elem = self.controls [ i ] 
            if usePyQt4 :
                MatrixWidget.connect ( elem [ 1  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 2  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 3  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 4  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
                MatrixWidget.connect ( elem [ 5  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 6  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 7  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 8  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
                MatrixWidget.connect ( elem [ 9  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 10 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 11 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 12 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
                MatrixWidget.connect ( elem [ 13 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 14 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 15 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.connect ( elem [ 16 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
            
                MatrixWidget.connect ( elem [ 0 ], QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged ) 
            else :
                elem [ 1  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 2  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 3  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 4  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                                          
                elem [ 5  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 6  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 7  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 8  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                                          
                elem [ 9  ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 10 ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 11 ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 12 ].editingFinished.connect ( self.onFloatEditEditingFinished )
                                          
                elem [ 13 ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 14 ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 15 ].editingFinished.connect ( self.onFloatEditEditingFinished )
                elem [ 16 ].editingFinished.connect ( self.onFloatEditEditingFinished )
            
                elem [ 0 ].activated.connect ( self.onCurrentIndexChanged ) 
    #
    # disconnectSignals
    #
    def disconnectSignals ( self, MatrixWidget ) :
        #
        for i in range ( self.widget.param.arraySize ) :
            elem = self.controls [ i ] 
            if usePyQt4 :
                MatrixWidget.disconnect ( elem [ 1  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 2  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 3  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 4  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
                MatrixWidget.disconnect ( elem [ 5  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 6  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 7  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 8  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
                MatrixWidget.disconnect ( elem [ 9  ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 10 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 11 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 12 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
    
                MatrixWidget.disconnect ( elem [ 13 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 14 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 15 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                MatrixWidget.disconnect ( elem [ 16 ], QtCore.SIGNAL ( 'editingFinished()' ), self.onFloatEditEditingFinished )
                
                MatrixWidget.disconnect ( elem [ 0 ], QtCore.SIGNAL ( 'activated(int)' ), self.onCurrentIndexChanged )
            else :
                elem [ 1  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 2  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 3  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 4  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
    
                elem [ 5  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 6  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 7  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 8  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
    
                elem [ 9  ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 10 ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 11 ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 12 ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
    
                elem [ 13 ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 14 ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 15 ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
                elem [ 16 ].editingFinished.disconnect ( self.onFloatEditEditingFinished )
            
                elem [ 0 ].activated.connect ( self.onCurrentIndexChanged ) 
    #
    # onFloatEditEditingFinished
    #
    def onFloatEditEditingFinished ( self ) :
        #
        arrayValue = []
        for i in range ( self.widget.param.arraySize ) :
            elem = self.controls [ i ] 
            floatStr0 = elem [ 1  ].text ()
            floatStr1 = elem [ 2  ].text ()
            floatStr2 = elem [ 3  ].text ()
            floatStr3 = elem [ 4  ].text ()
            if usePyQt4 :
                f0 = floatStr0.toFloat ()[0]
                f1 = floatStr1.toFloat ()[0] 
                f2 = floatStr2.toFloat ()[0]
                f3 = floatStr3.toFloat ()[0]
            else :
                f0 = float ( floatStr0 )
                f1 = float ( floatStr1 )
                f2 = float ( floatStr2 )
                f3 = float ( floatStr3 )
            
            floatStr0 = elem [ 5  ].text ()
            floatStr1 = elem [ 6  ].text ()
            floatStr2 = elem [ 7  ].text ()
            floatStr3 = elem [ 8  ].text ()
            if usePyQt4 :
                f4 = floatStr0.toFloat ()[0]
                f5 = floatStr1.toFloat ()[0] 
                f6 = floatStr2.toFloat ()[0]
                f7 = floatStr3.toFloat ()[0]
            else :
                f4 = float ( floatStr0 )
                f5 = float ( floatStr1 )
                f6 = float ( floatStr2 )
                f7 = float ( floatStr3 )
            
            floatStr0 = elem [ 9  ].text ()
            floatStr1 = elem [ 10 ].text ()
            floatStr2 = elem [ 11 ].text ()
            floatStr3 = elem [ 12 ].text ()
            if usePyQt4 :
                f8 = floatStr0.toFloat ()[0]
                f9 = floatStr1.toFloat ()[0] 
                f10 = floatStr2.toFloat ()[0]
                f11 = floatStr3.toFloat ()[0]
            else :
                f8  = float ( floatStr0 ) 
                f9  = float ( floatStr1 ) 
                f10 = float ( floatStr2 ) 
                f11 = float ( floatStr3 ) 
            
            floatStr0 = elem [ 13 ].text ()
            floatStr1 = elem [ 14 ].text ()
            floatStr2 = elem [ 15 ].text ()
            floatStr3 = elem [ 16 ].text ()
            if usePyQt4 :
                f12 = floatStr0.toFloat ()[0]
                f13 = floatStr1.toFloat ()[0] 
                f14 = floatStr2.toFloat ()[0]
                f15 = floatStr3.toFloat ()[0]
            else :
                f12 = float ( floatStr0 )
                f13 = float ( floatStr1 )
                f14 = float ( floatStr2 )
                f15 = float ( floatStr3 )
            arrayValue.append ( [ [f0,f1,f2,f3], [f4,f5,f6,f7], [f8,f9,f10,f11], [f12,f13,f14,f15] ] ) 
        self.widget.param.setValue ( arrayValue )
    #
    # onCurrentIndexChanged
    #
    def onCurrentIndexChanged ( self, idx ) :
        #
        # TODO: spaces should be stored in separate spaces array
        #
        for i in range ( self.widget.param.arraySize ) :
            space = str ( self.controls [ i ][ 0 ].currentText () ) 
            if space == 'current' : space = None
            self.widget.param.space = space
    #
    # updateGui
    # value  = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]   
    #      
    def updateGui ( self, value ) :
        # 
        #print ( '>>> MatrixWidget_array.updateGui' )
        for i in range ( self.widget.param.arraySize ) :
            elem = self.controls [ i ] 	
            if usePyQt4 :
                elem [ 1  ].setText ( QtCore.QString.number ( float ( value [i][0][0] ), 'f', 3 ) )
                elem [ 2  ].setText ( QtCore.QString.number ( float ( value [i][0][1] ), 'f', 3 ) )
                elem [ 3  ].setText ( QtCore.QString.number ( float ( value [i][0][2] ), 'f', 3 ) )
                elem [ 4  ].setText ( QtCore.QString.number ( float ( value [i][0][3] ), 'f', 3 ) )
                           
                elem [ 5  ].setText ( QtCore.QString.number ( float ( value [i][1][0] ), 'f', 3 ) )
                elem [ 6  ].setText ( QtCore.QString.number ( float ( value [i][1][1] ), 'f', 3 ) )
                elem [ 7  ].setText ( QtCore.QString.number ( float ( value [i][1][2] ), 'f', 3 ) )
                elem [ 8  ].setText ( QtCore.QString.number ( float ( value [i][1][3] ), 'f', 3 ) )
                           
                elem [ 9  ].setText ( QtCore.QString.number ( float ( value [i][2][0] ), 'f', 3 ) )
                elem [ 10 ].setText ( QtCore.QString.number ( float ( value [i][2][1] ), 'f', 3 ) )
                elem [ 11 ].setText ( QtCore.QString.number ( float ( value [i][2][2] ), 'f', 3 ) )
                elem [ 12 ].setText ( QtCore.QString.number ( float ( value [i][2][3] ), 'f', 3 ) )
                           
                elem [ 13 ].setText ( QtCore.QString.number ( float ( value [i][3][0] ), 'f', 3 ) )
                elem [ 14 ].setText ( QtCore.QString.number ( float ( value [i][3][1] ), 'f', 3 ) )
                elem [ 15 ].setText ( QtCore.QString.number ( float ( value [i][3][2] ), 'f', 3 ) )
                elem [ 16 ].setText ( QtCore.QString.number ( float ( value [i][3][3] ), 'f', 3 ) )
            else :
                elem [ 1  ].setText ( str ( value [i][0][0] ) )
                elem [ 2  ].setText ( str ( value [i][0][1] ) )
                elem [ 3  ].setText ( str ( value [i][0][2] ) )
                elem [ 4  ].setText ( str ( value [i][0][3] ) )
                                                           
                elem [ 5  ].setText ( str ( value [i][1][0] ) )
                elem [ 6  ].setText ( str ( value [i][1][1] ) )
                elem [ 7  ].setText ( str ( value [i][1][2] ) )
                elem [ 8  ].setText ( str ( value [i][1][3] ) )
                                                           
                elem [ 9  ].setText ( str ( value [i][2][0] ) )
                elem [ 10 ].setText ( str ( value [i][2][1] ) )
                elem [ 11 ].setText ( str ( value [i][2][2] ) )
                elem [ 12 ].setText ( str ( value [i][2][3] ) )
                                                           
                elem [ 13 ].setText ( str ( value [i][3][0] ) )
                elem [ 14 ].setText ( str ( value [i][3][1] ) )
                elem [ 15 ].setText ( str ( value [i][3][2] ) )
                elem [ 16 ].setText ( str ( value [i][3][3] ) )
