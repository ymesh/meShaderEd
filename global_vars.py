#
# global_vars.py
#
from PyQt4 import QtCore, QtGui
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
  ,'Renderer':''
  ,'RendererFlags':''
  ,'ShaderCompiler':''
  ,'ShaderDefines':''
  ,'TEX':''
  ,'SLO':''
}
DEBUG_MODE = True

GFX_NODE_TYPE           = QtGui.QGraphicsItem.UserType + 1
GFX_LINK_TYPE           = QtGui.QGraphicsItem.UserType + 2
GFX_NODE_LABEL_TYPE     = QtGui.QGraphicsItem.UserType + 3
GFX_NODE_SWATCH_TYPE    = QtGui.QGraphicsItem.UserType + 4
GFX_NODE_CONNECTOR_TYPE = QtGui.QGraphicsItem.UserType + 5

