"""
 geomData.py

"""
import os, sys
from PyQt4 import QtCore

from global_vars import app_global_vars, DEBUG_MODE

GEOM_GROUP_TYPE = 0
GEOM_SMOOTH_GROUP_TYPE = 1
GEOM_OBJECT_TYPE = 2

#
# Vertex
#
class Vertex () :
  #
  # __init__
  #
  def __init__ ( self, x, y, z, w = 1.0 ) :
    self.x = x
    self.y = y
    self.z = z
    self.w = w
#
# VertexNormal
#
class VertexNormal () :
  #
  # __init__
  #
  def __init__ ( self, i, j, k ) :
    self.i = i
    self.j = j
    self.k = k
#
# VertexParameter
#
class VertexParameter () :
  #
  # __init__
  #
  def __init__ ( self, u, v, w = 1.0 ) :
    self.u = u
    self.v = v
    self.w = w
#
# VertexTexture
#
class VertexTexture () :
  #
  # __init__
  #
  def __init__ ( self, u, v = 0.0, w = 0.0 ) :
    self.u = u
    self.v = v
    self.w = w
#
# Face
#
class Face () :
  #
  # __init__
  #
  def __init__ ( self ) :
    self.vertexIdxes = []
    self.textureIdxes = []
    self.normalIdxes = []

#
# GeomData
#
class GeomData () :
  #
  # __init__
  #
  def __init__ ( self ) :
    #
    self.verts = []
    self.texcoord = []
    self.normals = []

#
# GeomGroup
#
class GeomGroup () :
  #
  # __init__
  #
  def __init__ ( self ) :
    #
    self.type = GEOM_GROUP_TYPE   # 'g', 's', 'o'
    self.faces = []
    self.material = ''
    self.name = ''

