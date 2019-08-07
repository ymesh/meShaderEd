#
# global_vars.py
#
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore, QtGui

if  not usePyQt5 :
    QtModule = QtGui
else :
    from core.mePyQt import QtWidgets
    QtModule = QtWidgets
    
app_global_vars = {
     'TempPath':''
    ,'RootPath':''
    ,'ProjectPath':''
    ,'ProjectShaders':'' 
    ,'ProjectTextures':''
    ,'ProjectNetworks':'' 
    ,'ProjectSources':''
    ,'ProjectSearchPath':''
    ,'ProjectSearchShaders':'' 
    ,'ProjectSearchTextures':'' 
    ,'NodesPath':''
    ,'LibPath':''
    ,'TexturePath':''
    ,'ShaderPath':'' 
    ,'IncludePath':''
    ,'RibPath':''
    ,'DisplaySearchPath':''
    ,'TextureSearchPath':''
    ,'ShaderSearchPath':''
    ,'ArchiveSearchPath':''
    ,'RendererPreset':''
    ,'RendererName':''
    ,'RendererFlags':''
    ,'ShaderCompiler':''
    ,'ShaderDefines':''
    ,'ShaderInfo':''
    ,'SLO':''
    ,'TextureMake':''
    ,'TextureInfo':''
    ,'TextureViewer':''  
    ,'TEX':''
}

app_colors = {
     'rsl_node_bg': QtGui.QColor ( 0, 128, 128 )
    ,'rib_node_bg': QtGui.QColor ( 255, 150, 50 )
    ,'image_node_bg': QtGui.QColor ( 128, 128, 128 )
    ,'group_node_bg': QtGui.QColor ( 0, 0, 128 )
}

DEBUG_MODE = True

GFX_NODE_TYPE           = QtModule.QGraphicsItem.UserType + 1
GFX_LINK_TYPE           = QtModule.QGraphicsItem.UserType + 2
GFX_NODE_LABEL_TYPE     = QtModule.QGraphicsItem.UserType + 3
GFX_NODE_CONNECTOR_TYPE = QtModule.QGraphicsItem.UserType + 4
GFX_SWATCH_NODE_TYPE    = QtModule.QGraphicsItem.UserType + 5
GFX_NOTE_TYPE           = QtModule.QGraphicsItem.UserType + 6
GFX_NODE_GROUP_TYPE     = QtModule.QGraphicsItem.UserType + 7

VALID_NODE_TYPES = [ 
    'rib', 
    'rib_code', 
    'rsl_code', 
    'image', 
    'surface', 
    'displacement', 
    'light', 
    'volume', 
    'variable', 
    'connector', 
    'note', 
    'swatch', 
    'geom' 
]

VALID_PARAM_TYPES = [ 
    'float', 
    'int', 
    'color', 
    'string', 
    'normal', 
    'point', 
    'vector', 
    'matrix',
    'surface', 
    'displacement', 
    'volume', 
    'light',
    'rib', 
    'text', 
    'transform',
    'image', 
    'control',
    'shader', 
    'geom'  
]

VALID_RIB_NODE_TYPES = [ 'rib', 'rib_code' ] #??? depricated

VALID_SCENE_TYPES = [ 'rib' ]

VALID_RSL_NODE_TYPES = [
    'rsl_code',
    'surface',
    'displacement',
    'light',
    'volume' 
] #??? depricated

VALID_RSL_SHADER_TYPES = [ 
    'surface', 
    'displacement', 
    'light', 
    'volume'
]

VALID_RSL_PARAM_TYPES = [
    'float',
    'color',
    'point',
    'normal',
    'vector',
    'matrix',
    'string','shader'
]
VALID_RSL_SPACES = [
    "current",
    "shader",
    "object",
    "camera",
    "world",
    "raster",
    "NDC","screen"
]

VALID_RSL_COLOR_SPACES = [ 
    "rgb",
    "hsv",
    "hsl",
    "xyz",
    "XYZ","YIQ"
]


