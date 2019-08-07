"""

 node.py

"""
import os, sys, copy
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtXml
from core.signal import Signal

from global_vars import app_global_vars, DEBUG_MODE, VALID_RIB_NODE_TYPES
from core.node_global_vars import node_global_vars
from core.meCommon import getParsedLabel, normPath
#
# Node
#
class Node ( QtCore.QObject ) :
    #
    id = 0
    #
    # __init__
    #
    def __init__ ( self, xml_node = None, nodenet = None ) :
        #
        QtCore.QObject.__init__ ( self )
        #
        # Define signals for PyQt5
        #
        if usePySide or usePyQt5 :
            #
            self.nodeUpdated = Signal () # QtCore.pyqtSignal ( [QtCore.QObject] )
            self.nodeParamsUpdated = Signal () #QtCore.pyqtSignal ( [QtCore.QObject] )
            #
        self.id = None
        self.name = None
        self.label = None
        self.type = None
        
        self.version = None
        self.format = None
        self.parent = None
        self.dirty = False

        self.author = None
        self.help = None
        self.icon = None

        self.master = None

        self.code = None            # Node code (RSL, RIB, ... )
        self.control_code = None    # python code executed before node computation
        self.computed_code = None   # code collected after compute on all connected nodes
        
        self.event_code = {}
        #self.event_code [ 'ParamLabelRenamed' ] = None
        #self.event_code [ 'ParamAdded' ] = None
        #self.event_code [ 'ParamRemoved' ] = None

        self.display = True

        self.computedInputParams = None
        self.computedOutputParams = None
        self.computedLocalParams = None
        self.computedIncludes = None
        self.computedLocals = None
        self.computedCode = None

        #self.previewCode = None

        self.inputParams = []
        self.outputParams = []
        self.internals = []
        self.includes = []

        self.inputLinks = {}
        self.outputLinks = {}

        self.childs = set()

        self.nodenet = nodenet

        # position from GfxNode
        self.offset = ( 0, 0 )

        if xml_node != None :
            self.parseFromXML ( xml_node )
    #
    # __del__
    #
    def __del__ ( self ) :
        #
        if DEBUG_MODE : print ( '>> Node( %s ).__del__' % self.label )
    #
    # build
    #
    @classmethod
    def build ( cls ) :
        # set unique id while building
        node = cls ()
        Node.id += 1
        node.id = Node.id
        return node
    #
    # copy
    #
    def copy ( self ) : assert 0, 'copy needs to be implemented!'
    #
    # updateNode
    #
    def updateNode ( self, emit_signal = False ) : 
        #
        if DEBUG_MODE : print ( '>> Node( %s ).updateNode' % self.label  ), emit_signal
        if emit_signal :
            if DEBUG_MODE : print ( '** emit signal nodeUpdated' )
            if usePyQt4 :
                self.emit ( QtCore.SIGNAL ( 'nodeUpdated' ), self )
            else :
                self.nodeUpdated.emit ( self )
    #
    # updateNodeParams
    #
    def updateNodeParams ( self, emit_signal = False ) : 
        #
        if DEBUG_MODE : print ( '>> Node( %s ).updateNodeParams' % self.label ), emit_signal
        if emit_signal :
            if usePyQt4 :
                self.emit ( QtCore.SIGNAL ( 'nodeParamsUpdated' ), self )
            else :
                self.nodeParamsUpdated.emit ( self )
    #
    # addChild
    #
    def addChild ( self, node ) : self.childs.add ( node )
    #
    # removeChild
    #
    def removeChild ( self, node ) :
        #
        if node in self.childs :
            self.childs.remove ( node )
            if DEBUG_MODE : print ( '** Node(%s).removeChild %s' % ( self.label, node.label ) )
        else :
            if DEBUG_MODE : print ( '!! Node(%s).removeChild child %s is not in the list' % ( self.label, node.label ) )
    #
    # printInfo
    #
    def printInfo ( self ) :
        #
        print ( ':: Node (id = %d) label = %s' % ( self.id, self.label ) )
        print ( '** Node inputLinks:' )
        for param in self.inputLinks.keys () :
            print ( '\t* param: %s (%s) linked to ' % ( param.name, param.label ) )
            self.inputLinks [ param ].printInfo ()
        print ( '** Node outputLinks:' )
        #print '*****', self.outputLinks
        for param in self.outputLinks.keys () :
            print ( '\t* param: %s (%s) linked to ' % ( param.name, param.label ) )
            linklist = self.outputLinks [ param ]
            for link in linklist :
                link.printInfo ()
        print ( '** Node children:' )
        for child in self.childs :
            print ( '\t* %s' % child.label )
    #
    # addInputParam
    #
    def addInputParam ( self, param ) :
        #
        param.isInput = True
        # to be sure that name and label is unique
        if param.name in self.getParamsNames () : self.renameParamName ( param, param.name )
        if param.label in self.getParamsLabels () : self.renameParamLabel ( param, param.label )
        self.inputParams.append ( param )
        if self.event_code :
            if 'ParamAdded' in self.event_code.keys () :
                exec ( self.event_code [ 'ParamAdded' ], { 'param' : param, 'self' : self } )
    #
    # addOutputParam
    #
    def addOutputParam ( self, param ) :
        #
        param.isInput = False
        # to be sure that name and label is unique
        if param.name in self.getParamsNames () : self.renameParamName ( param, param.name )
        if param.label in self.getParamsLabels () : self.renameParamLabel ( param, param.label )
        self.outputParams.append ( param )
        if self.event_code :
            if 'ParamAdded' in self.event_code.keys () :
                exec ( self.event_code [ 'ParamAdded' ], { 'param' : param, 'self' : self } )
    #
    # addInternal
    #
    def addInternal ( self, newName ) :
        #print '--> add internal: %s' % internal
        internal = newName
        if internal != '' :
            from meCommon import getUniqueName
            internal = getUniqueName ( newName, self.internals )
            self.internals.append ( internal )
        return internal
    #
    # addInclude
    #
    def addInclude ( self, newName ) :
        #print '--> add include: %s' % include
        include = newName
        if include != '' :
            from meCommon import getUniqueName
            include = getUniqueName ( newName, self.includes )
            self.includes.append ( include )
        return include
    #
    # attachInputParamToLink
    #
    def attachInputParamToLink ( self, param, link ) :
        #
        self.inputLinks [ param ] = link
    #
    # attachOutputParamToLink
    #
    def attachOutputParamToLink ( self, param, link ) :
        #
        #if DEBUG_MODE : print ">> Node::attachOutputParamToLink param = %s" % param.name
        if not param in self.outputLinks.keys () :
            self.outputLinks [ param ] = []
        if not link in self.outputLinks [ param ] :
            self.outputLinks [ param ].append ( link )
    #
    # detachInputParam
    #
    def detachInputParam ( self, param ) :
        #
        removedLink = None
        if DEBUG_MODE : print ( ">> Node::detachInputParam param = %s" % param.name )
        if param in self.inputLinks.keys () :
            removedLink = self.inputLinks.pop ( param )
        return removedLink
    #
    # detachOutputParam
    #
    def detachOutputParam ( self, param ) :
        #
        removedLinks = []
        if param in self.outputLinks.keys () :
            outputLinks = self.outputLinks [ param ]
            for link in outputLinks :
                removedLinks.append ( link )
            self.outputLinks.pop ( param )
        return removedLinks
    #
    # detachOutputParamFromLink
    #
    def detachOutputParamFromLink ( self, param, link ) :
        #
        removedLink = None
        if param in self.outputLinks.keys () :
            outputLinks = self.outputLinks [ param ]
            if link in outputLinks :
                removedLink = link
                outputLinks.remove ( link )
        return removedLink
    #
    # isInputParamLinked
    #
    def isInputParamLinked ( self, param ) : return param in self.inputLinks.keys ()
    #
    # isOutputParamLinked
    #
    def isOutputParamLinked ( self, param ) : return param in self.outputLinks.keys ()
    #
    # getLinkedSrcNode
    #
    def getLinkedSrcNode ( self, param ) :
        # returns node linked to input parameter param,
        # skipping all ConnectorNode
        #
        #if DEBUG_MODE : print '* getLinkedSrcNode node = %s param = %s' % ( self.label, param.label )
        srcNode = None
        srcParam = None
        if self.isInputParamLinked ( param ) :
            #if DEBUG_MODE : print '* isInputParamLinked'
            link = self.inputLinks [ param ]
            if link.srcNode.type == 'connector' :
                if len ( link.srcNode.inputParams ) :
                    firstParam = link.srcNode.inputParams [0]
                    ( srcNode, srcParam ) = link.srcNode.getLinkedSrcNode ( firstParam )
                else :
                    if DEBUG_MODE : print ( '* no inputParams at connector %s' % ( link.srcNode.label ) )
            else :
                srcNode = link.srcNode
                srcParam = link.srcParam
        return ( srcNode, srcParam )
    #
    # getLinkedDstNodes
    #
    def getLinkedDstNodes ( self, param, dstConnections = [] ) :
        # returns nodes linked to output parameter param,
        # skipping all ConnectorNode
        #
        #if DEBUG_MODE : print '*** getLinkedDstNodese node = %s param = %s' % ( self.label, param.label )
        dstNode = None
        dstParam = None
        # dstConnections = []
        if self.isOutputParamLinked ( param ) :
            #if DEBUG_MODE : print '* isOutputParamLinked'
            dstLinks = self.getOutputLinks ( param )
            for link in dstLinks :
                if link.dstNode.type == 'connector' :
                    #if DEBUG_MODE : print '* link.dstNode.type == connector'
                    connectorOutputParams = link.dstNode.outputParams
                    if len ( connectorOutputParams ) > 0 :
                        for connectorOutputParam in connectorOutputParams :
                            connectorDstConnections = []
                            retList = link.dstNode.getLinkedDstNodes ( connectorOutputParam, connectorDstConnections )
                            for ( retNode, retParam ) in retList : 
                                dstConnections.append ( ( retNode, retParam ) )
                    else :
                        if DEBUG_MODE : print ( '* no outputParams at connector %s' % ( link.dstNode.label ) )
                else :
                    dstNode = link.dstNode
                    dstParam = link.dstParam
                    dstConnections.append ( ( dstNode, dstParam ) )
        return dstConnections
    #
    # removeParam
    #
    def removeParam ( self, param ) :
        #
        if self.event_code :
            if 'ParamRemoving' in self.event_code.keys () :
                exec ( self.event_code [ 'ParamRemoving' ], { 'param' : param, 'self' : self } )
        
        removedLinks = []
        if param.isInput :
            link = self.detachInputParam ( param )
            if link is not None : removedLinks.append ( link )
            self.inputParams.remove ( param )
        else :
            removedLinks = self.detachOutputParam ( param )
            self.outputParams.remove ( param )
        if self.event_code :
            if 'ParamRemoved' in self.event_code.keys () :
                exec ( self.event_code [ 'ParamRemoved' ], { 'param' : param, 'self' : self } )
        return removedLinks
    #
    # getInputParamByName
    #
    def getInputParamByName ( self, name ) :
        #
        result = None
        for param in self.inputParams :
            if param.name == name :
                result = param
                break
        return result
    #
    # getOutputParamByName
    #
    def getOutputParamByName ( self, name ) :
        #
        result = None
        for param in self.outputParams :
            if param.name == name :
                result = param
                break
        return result
    #
    # getInputParamValueByName
    #
    def getInputParamValueByName ( self, name, CodeOnly = False ) :
        #
        result = None
        srcNode = srcParam = None
        param = self.getInputParamByName ( name )
        ( srcNode, srcParam ) = self.getLinkedSrcNode ( param )
        if srcNode is not None :
            # computation may be skipped if we need only value
            #if compute :
            srcNode.computeNode ( CodeOnly )
            if self.computed_code is not None :
                self.computed_code += srcNode.computed_code
            result = srcNode.parseGlobalVars ( srcParam.getValueToStr () )
        else :
            result = param.getValueToStr ()

        return result
    #
    # return common list for input and output parameters
    #
    def getParamsList ( self ) :
        #
        params = self.inputParams + self.outputParams
        return params
    #
    # getParamsNames
    #
    def getParamsNames ( self ) :
        #
        names = []
        for pm in self.getParamsList () : names.append ( pm.name )
        return names
    #
    # getParamsLabels
    #
    def getParamsLabels ( self ) :
        #
        labels = []
        for pm in self.getParamsList () : labels.append ( pm.label )
        return labels
    #
    # getInputLinks
    #
    def getInputLinks ( self ) :
        #
        inputLinks = []
        for link in self.inputLinks.values () :
            inputLinks.append ( link )
        return inputLinks
    #
    # getOutputLinks
    #
    def getOutputLinks ( self, param = None ) :
        #
        outputLinks = []
        for link_list in self.outputLinks.values () :
            for link in link_list :
                if param is not None :
                    if link.srcParam != param :
                        continue
                outputLinks.append ( link )
        return outputLinks
    #
    # getInputLinkByID
    #
    def getInputLinkByID ( self, id ) :
        #
        result = None
        for link in self.getInputLinks () :
            if link.id == id :
                result = link
                break
        return result
    #
    # getOutputLinkByID
    #
    def getOutputLinkByID ( self, id ) :
        #
        result = None
        for link in self.getOutputLinks () :
            if link.id == id :
                result = link
                break
        return result
    #
    # renameParamName
    #
    def renameParamName ( self, param, newName ) :
        # assign new unique name to param
        from meCommon import getUniqueName
        param.name = getUniqueName ( newName, self.getParamsNames() )
        return param.name
    #
    # renameParamLabel
    #
    def renameParamLabel ( self, param, newLabel ) :
        #
        oldLabel = param.label
        if DEBUG_MODE : print ( ">> Node( %s ).renameParamLabel  oldLabel = %s newLabel = %s" % ( self.label, oldLabel, newLabel ) )
        if newLabel == '' : newLabel = self.param.name
        # assign new unique label to param
        from meCommon import getUniqueName
        param.label = getUniqueName ( newLabel, self.getParamsLabels () )
        if self.event_code :
            if 'ParamLabelRenamed' in self.event_code.keys () :
                exec ( self.event_code [ 'ParamLabelRenamed' ], { 'param' : param, 'self' : self, 'oldLabel' : oldLabel } )
        
        return param.label
    #
    # onParamChanged
    #
    def onParamChanged ( self, param ) :
        #
        if DEBUG_MODE : print ( ">> Node: onParamChanged node = %s param = %s (pass...)" % ( self.label, param.name ) )
        pass
        #self.emit( QtCore.SIGNAL( 'onNodeParamChanged(QObject,QObject)' ), self, param )
    #
    # getLabel
    #
    def getLabel ( self ) : return self.label
    #
    # getName
    #
    def getName ( self ) : return self.name
    #
    # getNodenetName
    #
    def getNodenetName ( self ) : return self.nodenet.getName ()
    #
    # getInstanceName
    #
    def getInstanceName ( self ) : return  getParsedLabel ( self.label )
    #
    # getParamName
    #
    def getParamName ( self, param ) :
        #
        if param.isRibParam  or param.provider == 'attribute':
            paramName = param.name
        elif param.provider == 'primitive' : 
            paramName = getParsedLabel ( param.label )
        else :
            paramName = self.getInstanceName () + '_' + getParsedLabel ( param.label )
        return paramName
    #
    # getParamDeclaration
    #
    def getParamDeclaration ( self, param ) :
        #
        result = ''
        result += param.typeToStr () + ' '
        result += self.getParamName ( param )
        if param.isArray () and not param.isRibParam :
            arraySize = ''
            if param.arraySize > 0 :
                arraySize = str ( param.arraySize )
            result += '[%s]' % arraySize
        result += ' = ' + param.getValueToStr () + ';\n'
        return result
    #
    # parseFromXML
    #
    def parseFromXML ( self, xml_node ) :
        #
        id_node = xml_node.attributes ().namedItem ( 'id' )
        if not id_node.isNull () :
            self.id = int ( id_node.nodeValue () )
        else :
            if DEBUG_MODE : print ( '>> Node::parseFromXML id is None' )

        self.name = str ( xml_node.attributes ().namedItem ( 'name' ).nodeValue () )
        self.label = str ( xml_node.attributes ().namedItem ( 'label' ).nodeValue () )
        if self.label == '' : self.label = self.name
        #print '-> parsing from XML node name= %s label= %s' % ( self.name, self.label )

        self.version = str ( xml_node.attributes ().namedItem ( 'version' ).nodeValue () )
        self.parent = str ( xml_node.attributes ().namedItem ( 'parent' ).nodeValue () )
        self.format = str ( xml_node.attributes ().namedItem ( 'format' ).nodeValue () )
        
        self.author = str ( xml_node.attributes ().namedItem ( 'author' ).nodeValue () )
        self.type = str ( xml_node.attributes ().namedItem ( 'type' ).nodeValue () )
        #
        # try to convert from old format nodes
        #
        if self.type != 'nodegroup' :
            if self.version == '' or self.version is None :
                if self.format == '' or self.format is None :
                    ( self.type, self.format ) = translateOldType ( self.type )
            
        help_tag = xml_node.namedItem ( 'help' )
        if not help_tag.isNull() :
            self.help = help_tag.toElement ().text ()
        self.icon = str ( xml_node.attributes ().namedItem ( 'icon' ).nodeValue () )

        input_tag = xml_node.namedItem ( 'input' )
        if not input_tag.isNull () :
            xml_paramList = input_tag.toElement ().elementsByTagName ( 'property' )
            for i in range ( 0, xml_paramList.length () ) :
                xml_param = xml_paramList.item ( i )
                #
                # some parameters (String, Color, Point, Vector, Normal, Matrix ...)
                # have different string interpretation in RIB
                #
                isRibParam = ( self.format == 'rib' )
                param = createParamFromXml ( xml_param, isRibParam, True ) # #param.isInput = True
                self.addInputParam ( param )

        output_tag = xml_node.namedItem ( 'output' )
        if not output_tag.isNull () :
            xml_paramList = output_tag.toElement ().elementsByTagName ( 'property' )
            for i in range ( 0, xml_paramList.length () ) :
                xml_param = xml_paramList.item ( i )
                #
                # some parameters (Color, Point, Vector, Normal, Matrix ...)
                # have different string interpretation in RIB
                #
                isRibParam = ( self.format == 'rib' )
                param = createParamFromXml ( xml_param, isRibParam, False ) # #param.isInput = False
                self.addOutputParam ( param )

        internal_tag = xml_node.namedItem ( 'internal' )
        if not internal_tag.isNull () :
            xml_internalList = internal_tag.toElement ().elementsByTagName ( 'variable' )
            for i in range ( 0, xml_internalList.length () ) :
                var_tag = xml_internalList.item ( i )
                var = str ( var_tag.attributes ().namedItem ( 'name' ).nodeValue () )
                self.addInternal ( var )

        include_tag = xml_node.namedItem ( 'include' )
        if not include_tag.isNull () :
            xml_includeList = include_tag.toElement ().elementsByTagName ( 'file' )
            for i in range ( 0, xml_includeList.length () ) :
                inc_tag = xml_includeList.item ( i )
                inc = str ( inc_tag.attributes ().namedItem ( 'name' ).nodeValue () )
                self.addInclude ( inc )

        offset_tag = xml_node.namedItem ( 'offset' )
        if not offset_tag.isNull() :
            x = float ( offset_tag.attributes ().namedItem ( 'x' ).nodeValue () )
            y = float ( offset_tag.attributes ().namedItem ( 'y' ).nodeValue () )
            self.offset = ( x, y )

        control_code_tag = xml_node.namedItem ( 'control_code' )
        if not control_code_tag.isNull () :
            code_str = str ( control_code_tag.toElement ().text () )
            if code_str.lstrip () == '' : code_str = None
            self.control_code = code_str
        else :
            # for temp. backward compatibility
            control_code_tag = xml_node.namedItem ( 'param_code' )
            if not control_code_tag.isNull() :
                code_str = str ( control_code_tag.toElement ().text () )
                if code_str.lstrip () == '' : code_str = None
                self.control_code = code_str
                
        code_tag = xml_node.namedItem ( 'code' )
        if not code_tag.isNull () :
            code_str = str ( code_tag.toElement ().text () )
            if code_str.lstrip () == '' : code_str = None
            self.code = code_str
            
        event_code_tag = xml_node.namedItem ( 'event_code' )
        if not event_code_tag.isNull () :
            xml_handlerList = event_code_tag.toElement ().elementsByTagName ( 'handler' )
            for i in range ( 0, xml_handlerList.length () ) :
                handler_tag = xml_handlerList.item ( i )
                handler_name = str ( handler_tag.attributes ().namedItem ( 'name' ).nodeValue () )
                code_str = str ( handler_tag.toElement ().text () ).lstrip ()
                if code_str == '' : code_str = None
                self.event_code [ handler_name ] = code_str
    #
    # parseToXML
    #
    def parseToXML ( self, dom ) :
        #
        xml_node = dom.createElement ( 'node' )
        if DEBUG_MODE : print ( '>> Node::parseToXML (id = %d)' % ( self.id ) )
        if self.id is None :
            if DEBUG_MODE : print ( '>> Node::parseToXML id is None' )
        xml_node.setAttribute ( 'id', str( self.id ) )
        xml_node.setAttribute ( 'name', self.name )
        if self.label != None : xml_node.setAttribute ( 'label', self.label )
        if self.type != None : xml_node.setAttribute ( 'type', self.type )
        if self.author != None : xml_node.setAttribute ( 'author', self.author )
        if self.icon != None : xml_node.setAttribute ( 'icon', self.icon )
            
        if self.version != None : xml_node.setAttribute ( 'version', self.version )
        if self.parent != None : xml_node.setAttribute ( 'parent', self.parent )
        if self.format != None : xml_node.setAttribute ( 'format', self.format )

        if self.help != None :
            # append node help (short description)
            help_tag = dom.createElement ( 'help' )
            help_text = dom.createTextNode ( self.help )
            help_tag.appendChild ( help_text )
            xml_node.appendChild ( help_tag )

        input_tag = dom.createElement ( 'input' )
        for param in self.inputParams :
            #print '--> parsing param to XML: %s ...' % param.name
            input_tag.appendChild ( param.parseToXML ( dom )  )
        xml_node.appendChild ( input_tag )

        output_tag = dom.createElement ( 'output' )
        for param in self.outputParams :
            #print '--> parsing param to XML: %s ...' % param.name
            output_tag.appendChild ( param.parseToXML ( dom )  )
        xml_node.appendChild ( output_tag )

        internal_tag = dom.createElement ( 'internal' )
        for var in self.internals :
            var_tag = dom.createElement( 'variable' )
            var_tag.setAttribute ( 'name', var )
            internal_tag.appendChild ( var_tag )
        xml_node.appendChild ( internal_tag )

        include_tag = dom.createElement ( 'include' )
        for inc in self.includes :
            inc_tag = dom.createElement( 'file' )
            inc_tag.setAttribute ( 'name', inc )
            include_tag.appendChild ( inc_tag )
        xml_node.appendChild ( include_tag )

        if self.control_code != None :
            control_code_tag = dom.createElement ( 'control_code' )
            control_code_data = dom.createCDATASection ( self.control_code )
            control_code_tag.appendChild ( control_code_data )
            xml_node.appendChild ( control_code_tag )

        if self.code != None :
            code_tag = dom.createElement ( 'code' )
            code_data = dom.createCDATASection ( self.code )
            code_tag.appendChild ( code_data )
            xml_node.appendChild ( code_tag )
            
        if self.event_code :
            event_code_tag = dom.createElement ( 'event_code' )
            print ( '*** write event_code' )
            for key in self.event_code.keys () :
                print ( '*** write handler "%s"' % key )
                handler_tag = dom.createElement( 'handler' )
                handler_tag.setAttribute ( 'name', key )
                event_code_tag.appendChild ( handler_tag )
                handler_data = dom.createCDATASection ( self.event_code [ key ] )
                handler_tag.appendChild ( handler_data )
            xml_node.appendChild ( event_code_tag )

        if self.offset != None :
            ( x, y ) = self.offset
            offset_tag = dom.createElement ( 'offset' )
            offset_tag.setAttribute ( 'x', str (x) ) # have to use 'str' because PySide throws 
            offset_tag.setAttribute ( 'y', str (y) ) # Overflow error for negative values here
            xml_node.appendChild ( offset_tag )

        return xml_node
    #
    # getHeader
    #
    def getHeader ( self ) : assert 0, 'getHeader needs to be implemented!'

    #
    # getComputedCode
    #
    def getComputedCode ( self, CodeOnly = False ) : assert 0, 'getComputedCode needs to be implemented!'

    #
    # computeNode
    #
    def computeNode ( self, CodeOnly = False ) : assert 0, 'computeNode needs to be implemented!'
    #
    # collectComputed
    #
    def collectComputed ( self, computedCode, visitedNodes, CodeOnly = False ) :
        #
        print ( '>>> Node.collectComputed (empty)' )
    #
    # parseGlobalVars
    #
    def parseGlobalVars ( self, parsedStr ) :
        #
        print ( '>>> Node.parseGlobalVars (empty)' )
    #
    # execControlCode
    #
    def execControlCode ( self ) :
        #
        if self.control_code != None :
            control_code = self.control_code.lstrip ()
            if control_code != '' :
                exec control_code
    #
    # copySetup
    #
    def copySetup ( self, newNode ) :
        #
        if DEBUG_MODE : print ( '>> Node( %s ).copySetup ' % self.label )

        newNode.id = self.id

        name = self.name
        if name is None : name = str ( self.type )

        newNode.name = name

        label = self.label
        if label is None : label = name

        newNode.label  = label
        newNode.type   = self.type
        newNode.author = self.author
        newNode.help   = self.help
        newNode.icon   = self.icon
        newNode.master = self.master
        newNode.display = self.display
        
        newNode.format = self.format
        newNode.parent = self.parent
        newNode.dirty = self.dirty

        newNode.offset = self.offset

        import copy
        newNode.code         = copy.copy ( self.code )
        newNode.control_code = copy.copy ( self.control_code )
        newNode.event_code   = copy.copy ( self.event_code )
        #self.computed_code = None

        newNode.internals = copy.copy ( self.internals )
        newNode.includes  = copy.copy ( self.includes )

        newNode.inputLinks = {}
        newNode.outputLinks = {}

        #newNode.childs = set ()
        print ( '***newNode.childs: ', newNode.childs )
        #newNode.childs = copy.copy ( self.childs )

        newNode.inputParams = []
        for param in self.inputParams : newNode.inputParams.append ( param.copy () )

        newNode.outputParams = []
        for param in self.outputParams : newNode.outputParams.append ( param.copy () )

        return newNode
    #
    # save Node to .xml document
    #
    def save ( self ) :
        #
        result = False
    
        dom = QtXml.QDomDocument ( self.name )
        xml_code = self.parseToXML ( dom )
        dom.appendChild ( xml_code )
        
        file = QFile ( self.master )
        if file.open ( QtCore.QIODevice.WriteOnly ) :
            if file.write ( dom.toByteArray () ) != -1 :
                result = True
        file.close()
        return result
    #
    # getChildrenSet
    #
    def getChildrenSet ( self, children_set = set () ) :
        #
        for node in self.childs :
            children_set = node.getChildrenSet ( children_set )
            children_set.add ( node )
        return children_set  
    #
    # getChildrenList
    #
    def getChildrenList ( self, children_list = [] ) :
        #
        for node in self.childs :
            children_list = node.getChildrenList ( children_list )
            if node not in children_list :
                children_list.append ( node )
            
        return children_list  
#
# createParamFromXml
#
# name and type must be specified in xml
#
def createParamFromXml ( xml_param, isRibParam, isInput = True ) :
    #
    from core.params.floatNodeParam        import FloatNodeParam
    from core.params.intNodeParam          import IntNodeParam
    from core.params.colorNodeParam        import ColorNodeParam
    from core.params.stringNodeParam       import StringNodeParam
    from core.params.normalNodeParam       import NormalNodeParam
    from core.params.pointNodeParam        import PointNodeParam
    from core.params.vectorNodeParam       import VectorNodeParam
    from core.params.matrixNodeParam       import MatrixNodeParam
    #from core.params.surfaceNodeParam      import SurfaceNodeParam
    #from core.params.displacementNodeParam import DisplacementNodeParam
    #from core.params.volumeNodeParam       import VolumeNodeParam
    #from core.params.lightNodeParam        import LightNodeParam
    from core.params.ribNodeParam          import RibNodeParam
    from core.params.textNodeParam         import TextNodeParam
    from core.params.transformNodeParam    import TransformNodeParam
    from core.params.imageNodeParam        import ImageNodeParam
    from core.params.controlParam          import ControlParam
    from core.params.shaderNodeParam       import ShaderNodeParam
    from core.params.geomNodeParam         import GeomNodeParam
    from core.nodeParam                    import NodeParam

    param = None
    createParamTable = {     'float'        : FloatNodeParam
                                                    ,'int'          : IntNodeParam
                                                    ,'color'        : ColorNodeParam
                                                    ,'string'       : StringNodeParam
                                                    ,'normal'       : NormalNodeParam
                                                    ,'point'        : PointNodeParam
                                                    ,'vector'       : VectorNodeParam
                                                    ,'matrix'       : MatrixNodeParam
#													,'surface'      : SurfaceNodeParam
#													,'displacement' : DisplacementNodeParam
#													,'volume'       : VolumeNodeParam
#													,'light'        : LightNodeParam
                                                    ,'rib'          : RibNodeParam
                                                    ,'text'         : TextNodeParam
                                                    ,'transform'    : TransformNodeParam
                                                    ,'image'        : ImageNodeParam
                                                    ,'control'      : ControlParam
                                                    ,'shader'       : ShaderNodeParam
                                                    ,'link'         : NodeParam
                                                    ,'geom'         : GeomNodeParam
                                             }
    param_type = str ( xml_param.attributes ().namedItem ( 'type' ).nodeValue () )
    if param_type in createParamTable.keys () :
        param = createParamTable [ param_type ]( xml_param, isRibParam )
        param.isInput = isInput
    else :
        print ( '* Error: unknown param type !' )
    return param
#
# translateOldType
#
def translateOldType ( old_node_type ) :
    #
    node_type = None
    node_format = None
    if old_node_type is None : old_node_type = ''
    print ( '!!!! old format node type = %s' % old_node_type )
    if old_node_type in [ '', 'surface', 'displacement', 'light', 'volume', 'rsl', 'rsl_code' ] :
        node_format = 'rsl'
        node_type = 'node'
    elif old_node_type == 'image' :
        node_format = 'image'
        node_type = 'node'
    elif old_node_type == 'rib' :
        node_format = 'rib'
        node_type = 'node'
    elif old_node_type == 'rib_code' :
        node_format = 'rib'
        node_type = 'node'
    elif old_node_type == 'geom' :
        node_format = 'geom'
        node_type = 'node'
    elif old_node_type == 'variable' :
        node_format = 'rsl'
        node_type = 'variable'
    elif old_node_type == 'note' :
        node_format = 'note'
        node_type = 'note'
    elif old_node_type == 'swatch' :
        node_format = 'image'
        node_type = 'swatch'
    elif old_node_type == 'connector' :
        node_format = 'connector'
        node_type = 'connector'
        
    print ( '!!!! converted to type = %s format = %s' % ( node_type, node_format ) )
    return ( node_type, node_format )
