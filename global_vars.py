#
# global_vars.py
#
from core.mePyQt import QtCore, QtGui
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

if QtCore.QT_VERSION < 50000 :
	GFX_NODE_TYPE           = QtGui.QGraphicsItem.UserType + 1
	GFX_LINK_TYPE           = QtGui.QGraphicsItem.UserType + 2
	GFX_NODE_LABEL_TYPE     = QtGui.QGraphicsItem.UserType + 3
	GFX_NODE_CONNECTOR_TYPE = QtGui.QGraphicsItem.UserType + 4
	GFX_SWATCH_NODE_TYPE    = QtGui.QGraphicsItem.UserType + 5
	GFX_NOTE_TYPE           = QtGui.QGraphicsItem.UserType + 6
else	:
	UserType = 65536
	GFX_NODE_TYPE           = UserType + 1
	GFX_LINK_TYPE           = UserType + 2
	GFX_NODE_LABEL_TYPE     = UserType + 3
	GFX_NODE_CONNECTOR_TYPE = UserType + 4
	GFX_SWATCH_NODE_TYPE    = UserType + 5
	GFX_NOTE_TYPE           = UserType + 6

VALID_NODE_TYPES = [ 'rib', 
                     'rib_code', 
                     'rsl_code', 
                     'image', 
                     'surface', 
                     'displacement', 
                     'light', 
                     'volume', 
                     'variable', 
                     'connector', 
                     'swatch', 
                     'geom' ]
                     
VALID_PARAM_TYPES = [ 'float', 
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
                      'geom'  ]
                      
VALID_RIB_NODE_TYPES = [ 'rib', 'rib_code' ]
VALID_RSL_NODE_TYPES = [ 'rsl_code', 'surface', 'displacement', 'light', 'volume' ]
VALID_RSL_SHADER_TYPES = [ 'surface', 'displacement', 'light', 'volume' ]

VALID_RSL_PARAM_TYPES = [ 'float', 'color', 'point', 'normal', 'vector', 'matrix', 'string', 'shader' ]


