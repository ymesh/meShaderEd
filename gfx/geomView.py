"""
 
 geomView.py

"""
import os, sys
import math

from OpenGL.GL import *
#from OpenGL.GLU import *

from PyQt4 import QtCore, QtGui, QtOpenGL
#from PyQt4.QtOpenGL import * #QGLFunctions

PI = 3.14159265
def DEGTORAD ( x ) : return ( float ( x ) * 0.01745329251994 ) # (x * PI ) / 180.0
def RADTODEG ( x ) : return ( float ( x ) / 0.01745329251994 ) # (x * 180.0) / PI
      
"""
GLfloat lightPosition[] = { 20.f, 50.f, 0.f, 1.f };

GLfloat lightAmbient[] = { .4f, .4f, .4f };
GLfloat lightDiffuse[] = { .8f, .8f, .8f };
GLfloat lightSpecular[] = { 1.f, 1.f, 1.f, 1.f };
GLint defaultShininess = 96;

GLfloat grayAmbient[] = { .3f, .3f, .3f, 1.f };
GLfloat grayDiffuse[] = { .8f, .8f, .8f, 1.f };
GLfloat whiteSpecular[] = { 1.f, 1.f, 1.f, 1.f };

bool _shouldDrawWireframe = false;
bool _shouldDrawFlat = false;
bool _shouldDrawSmooth = true;
bool _shouldDrawPoints = false;
bool _shouldDrawNormals = false;

"""
#
# GeomView
#
class GeomView ( QtOpenGL.QGLWidget ) : # , QGLFunctions
  #
  # __init__
  #
  def __init__ ( self, parent ) :
    #
    QtOpenGL.QGLWidget.__init__ ( self, 
                      QtOpenGL.QGLFormat ( QtOpenGL.QGL.SampleBuffers | QtOpenGL.QGL.DoubleBuffer ), # SingleBuffer | QtOpenGL.QGL.NoOverlay DoubleBuffer QtOpenGL.QGL.SampleBuffers | QtOpenGL.QGL.DirectRendering ),
                      parent ) # QtOpenGL.QGLFormat ( QtOpenGL.QGL.SampleBuffers ), 
    #self.makeCurrent ()
    
    self.state = 'idle'
    self.pressed = False
    self.startPos = None
    
    self.bgColor = [ .3, .3, .3, 0.0 ]
    self.fgColor = [ .45, .45, .45, 0.0 ]
    
    self.modelMatrix = QtGui.QMatrix4x4 ()
    self.projectionMatrix = QtGui.QMatrix4x4 ()
    
    self.fov = 45.0
    self.roll = 0.0
    self.zNear = 0.01
    self.zFar = 1000.0
    self.width = 0.0
    self.height = 0.0
    
    self.isProjDirty = True
    
    self.isGridVisible = True
    self.headLight = False

    self.modelMatrix.translate ( 0.0, 0.0, 10.0 )
    self.target = QtGui.QVector3D ( 0.0, 0.0, 0.0 )
    self.orbit ( 45, -45 )
    self.dolly ( 240 )
    
    self.geom_code = ''
    
    print '>> GeomView init'
  #
  # initializeGL
  #
  def initializeGL ( self ) :
    #
    print ">> GeomeView.initializeGL"
    
    glClearColor ( self.bgColor [0], self.bgColor [1], self.bgColor [2], 0 )
    glEnable ( GL_DEPTH_TEST )
    glDepthFunc ( GL_LEQUAL )
    glDepthMask ( GL_TRUE )
    glClearDepth ( 1.0 )
    #glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  
    glEnable ( GL_BLEND )
    glBlendFunc ( GL_SRC_ALPHA , GL_ONE_MINUS_SRC_ALPHA )
  
    # lighting
    #glEnable ( GL_LIGHT0 )
    #glLightfv ( GL_LIGHT0, GL_AMBIENT, lightAmbient )
    #glLightfv ( GL_LIGHT0, GL_DIFFUSE, lightDiffuse )
  
  #
  # resizeGL
  #
  def resizeGL ( self, w, h ) :
    #
    #print '>> GeomeView.resizeGL (%d, %d)' % ( w, h )
    self.width = w
    self.height = h
    if self.height == 0 : self.height = 1
    if self.width == 0 : self.width = 1
    self.isProjDirty = True
  #
  # prepareForDrawing
  #
  def prepareForDrawing ( self ) :
    #
    #print '>> GeomeView.prepareForDrawing'
    self.setupProjection ()
    glViewport ( 0, 0, self.width, self.height )
  
    glMatrixMode ( GL_MODELVIEW )
    
    ( invertedMatrix, invertible ) = self.modelMatrix.inverted ()
    # print invertedMatrix
    glLoadMatrixf ( invertedMatrix.data () )
  
    #// gray-shaded
    #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, grayAmbient);
    #glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, grayDiffuse);
    #glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, whiteSpecular);
    #glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, defaultShininess);
  #
  # setupProjection
  #
  def setupProjection ( self ) :
    #
    #print '>> GeomeView.setupProjection'
    glMatrixMode ( GL_PROJECTION )
    
    if self.isProjDirty :
      glLoadIdentity()
      height = float ( self.zNear * math.tan ( self.fov * PI / 360.0) )
      width = float ( height )
      aspect = float ( float ( self.width ) / float ( self.height ) )
      if aspect > 1.0 :
        height = float ( height / aspect )
      else :
        width = float ( height * aspect )
      # print width, height, aspect 
      glFrustum ( -width, width, -height, height, self.zNear, self.zFar )
      params = glGetFloatv ( GL_PROJECTION_MATRIX )
      self.projectionMatrix = QtGui.QMatrix4x4 ( params [0][0],  params [0][1],  params [0][2],  params [0][3], 
                                                 params [1][0],  params [1][1],  params [1][2],  params [1][3],
                                                 params [2][0],  params [2][1],  params [2][2],  params [2][3],
                                                 params [3][0],  params [3][1],  params [3][2],  params [3][3]
                                               )
      #print self.projectionMatrix
      #print self.projectionMatrix.data ()    
      self.isProjDirty = False
    else :
      pass
      #print '>> GeomeView.setupProjection ( glLoadMatrixf )'
      #glLoadMatrixf ( self.projectionMatrix.data () )
  #
  # updateGL
  #
  def updateGL ( self ) :
    #
    #print ">> GeomeView.updateGL"
    QtOpenGL.QGLWidget.updateGL ( self )
  #
  # paintGL
  #
  def paintGL ( self ) :
    #
    #print ">> GeomeView.paintGL"
    #glClearColor ( 0, 0, 0, 0 ) # ( self.bgColor [0], self.bgColor [1], self.bgColor [2], 0.0 )
    glClearColor ( self.bgColor [0], self.bgColor [1], self.bgColor [2], 0 )
    glClearDepth ( 1.0 )
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT ) # ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  
    self.prepareForDrawing ()
  
    #glDisable ( GL_LIGHTING )
    #glShadeModel ( GL_FLAT )
  
    if self.isGridVisible : self.drawGrid ()
  
    #self.drawAxis();
    #glShadeModel ( GL_SMOOTH )
    #glEnable ( GL_LIGHTING )
    
    if self.headLight :
      # constrain light to camera
      lightPosition[0] = self.modelMatrix [3][0]
      lightPosition[1] = self.modelMatrix [3][1] + 100.0;
      lightPosition[2] = self.modelMatrix [3][2]
      glLightfv ( GL_LIGHT0, GL_POSITION, lightPosition )
    
    #self.prepareForDrawing ()
    self.drawAll();
  #
  # drawAll
  #    
  def drawAll ( self ) :
    #
    self.drawSpiral ()
  #
  # drawSpiral ( self ) :
  #
  def drawSpiral ( self ) :
    #
    spiral_code = """
glEnableClientState ( GL_VERTEX_ARRAY )
spiral_array = []
# Second Spiral using "array immediate mode" (i.e. Vertex Arrays)
radius = 0.8
x = radius * math.sin ( 0 )
y = radius * math.cos ( 0 )
glColor ( 1.0, 0.0, 0.0 )
for deg in xrange ( 820 ):
  spiral_array.append ( [x, y] )
  rad = math.radians ( deg )
  radius -= 0.001
  x = radius * math.sin ( rad )
  y = radius * math.cos ( rad )

glVertexPointerf ( spiral_array )
glDrawArrays ( GL_LINE_STRIP, 0, len ( spiral_array ) )
glFlush ()



    """    
    exec spiral_code
    
    # Draw the spiral in 'immediate mode'
    # WARNING: You should not be doing the spiral calculation inside the loop
    # even if you are using glBegin/glEnd, sin/cos are fairly expensive functions
    # I've left it here as is to make the code simpler.
    radius = 1.0
    x = radius * math.sin ( 0 )
    y = radius * math.cos ( 0 )
    glColor ( 0.0, 1.0, 0.0 )
    glBegin ( GL_LINE_STRIP )
    for deg in xrange ( 1000 ) :
      glVertex ( x, y, 0.0 )
      rad = math.radians ( deg )
      radius -= 0.001
      x = radius * math.sin ( rad )
      y = radius * math.cos ( rad )
    glEnd ()
  #
  # drawGrid
  #
  def drawGrid ( self ) :
    #
    #print ">> GeomeView.drawGrid"
    count = 20
    scale = 1.0
    
    glColor3f ( 0.45, 0.45, 0.45 )
    glLineWidth ( 1.0 )
    glBegin ( GL_LINES )
    for w in range ( count + 1 ) :
      glVertex3f ( -count / 2 * scale, 0, ( w - count / 2 ) * scale )
      glVertex3f ( ( count - count / 2) * scale, 0, ( w - count / 2 ) * scale )
    for w in range ( count + 1 ) :
      glVertex3f ( ( w - count / 2 ) * scale, 0, -count / 2 * scale )
      glVertex3f ( ( w - count / 2 ) * scale, 0, ( count - count / 2 ) * scale )
    glEnd ()
    
    # draw 2 middle lines again
    glColor3f ( 0.9, 0.2, 0.2 )
    glLineWidth ( 1.0 )
    glBegin ( GL_LINES )
    glVertex3f ( -count / 2 * scale, 0, ( count / 2 - count / 2 ) * scale )
    glVertex3f ( ( count - ( count / 2 ) ) * scale, 0, ( count / 2 - count / 2 ) * scale )
    glVertex3f ( ( count / 2 - count / 2 ) * scale, 0, -count / 2 * scale )
    glVertex3f ( ( count / 2 - count / 2 ) * scale, 0, ( count - count / 2 ) * scale )
    glEnd ()
  #
  #
  #
  def drawAxis ( self ) :
    #
    pass
    """
    void Viewport::drawAxis(){
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    
    glOrtho(-1, 1, -1, 1, -1, 1);
    glViewport(0, 0, 50, 50);
    
    GLfloat mvm[16];
    glMatrixMode(GL_MODELVIEW);
    glGetFloatv(GL_MODELVIEW_MATRIX, mvm);
    mvm[12] = mvm[13] = mvm[14] = 0.f;
    glLoadMatrixf(mvm);
    
    glLineWidth(2.f);
    glBegin(GL_LINES);
    {
      // X
      glColor3f(1.f, 0.f, 0.f);
      glVertex3f(0.f, 0.f, 0.f);
      glVertex3f(1.f, 0.f, 0.f);
      // Y
      glColor3f(0.f, 1.f, 0.f);
      glVertex3f(0.f, 0.f, 0.f);
      glVertex3f(0.f, 1.f, 0.f);
      // Z
      glColor3f(0.f, 0.f, 1.f);
      glVertex3f(0.f, 0.f, 0.f);
      glVertex3f(0.f, 0.f, 1.f);
    }
    glEnd();
    """
  #
  #
  #
  def printModelMatrix ( self ) :
    #
    print '*** self.modelMatrix :'
    #print self.modelMatrix
    row0 = self.modelMatrix.row ( 0 )
    row1 = self.modelMatrix.row ( 1 )
    row2 = self.modelMatrix.row ( 2 ) 
    row3 = self.modelMatrix.row ( 3 ) 
    print row0.x (), '\t', row0.y (), '\t', row0.z (), '\t', row0.w ()
    print row1.x (), '\t', row1.y (), '\t', row1.z (), '\t', row1.w ()
    print row2.x (), '\t', row2.y (), '\t', row2.z (), '\t', row2.w ()
    print row3.x (), '\t', row3.y (), '\t', row3.z (), '\t', row3.w ()
    print '***'
  #
  # self.modelMatrix translation
  #
  # Matrix44<T>::translation () const
  # {
  #   return Vec3<T> (x[3][0], x[3][1], x[3][2]);
  # }
  #
  def translation0 ( self ) :
    #
    row3 = self.modelMatrix.row ( 3 ) 
    return QtGui.QVector3D ( row3.x (), row3.y (), row3.z () )
  #
  def translation ( self ) :
    #
    row0 = self.modelMatrix.row ( 0 )
    row1 = self.modelMatrix.row ( 1 )
    row2 = self.modelMatrix.row ( 2 ) 
    #row3 = self.modelMatrix.row ( 3 ) 
    return QtGui.QVector3D ( row0.w (), row1.w (), row2.w () )
    #return QtGui.QVector3D ( row3.x (), row3.y (), row3.z () )
  #
  # self.modelMatrix dollyVector
  #
  def dollyVector ( self ) :
    #
    # cam does dolly on its Z local axis (QtGui.QVector4D )
    row2 = self.modelMatrix.row ( 2 ) 
    return QtGui.QVector3D ( row2.x (), row2.y (), row2.z () )
  #
  # viewport pan
  #
  def pan ( self, deltaSide, deltaUp ) :
    #
    translation = self.translation ()
    lenDist = ( translation - self.target ).length() 
    factorX = lenDist * 0.001 * -deltaSide
    factorY = lenDist * 0.001 * deltaUp
    
    panVec = QtGui.QVector3D ( factorX, factorY, 0.0 )
    self.modelMatrix.translate ( panVec.x (), panVec.y (), panVec.z () )
    translation_new = self.translation ()
  #
  # viewport dolly
  #
  def dolly ( self, deltaSide ) :
    #
    if deltaSide != 0 :
      #print '* deltaSide = %d' % deltaSide
      dollyVec = self.dollyVector ()
      translation = self.translation ()
      dollyVec *= ( deltaSide * ( translation - self.target ).length() * 0.01 )
      self.modelMatrix.translate ( dollyVec.x (), dollyVec.y (), dollyVec.z () )
  #
  # viewport orbit
  #
  def orbit ( self, deltaSide, deltaUp ) :
    #
    #
    # setAxisAngle
    #
    # original code from OpenEXR library (ImathMatrix.h)
    # Matrix44<T>::setAxisAngle (const Vec3<S>& axis, S angle)
    #
    def setAxisAngle ( vec3, angle ) :
      #
      unit = vec3.normalized ()
      sine = math.sin ( angle )
      cosine = math.cos ( angle ) 
      
      m11 = unit.x () * unit.x () * ( 1 - cosine ) + cosine
      m12 = unit.x () * unit.y () * ( 1 - cosine ) + unit.z () * sine
      m13 = unit.x () * unit.z () * ( 1 - cosine ) - unit.y () * sine
      m14 = 0.0
      
      m21 = unit.x () * unit.y () * ( 1 - cosine ) - unit.z () * sine
      m22 = unit.y () * unit.y () * ( 1 - cosine ) + cosine
      m23 = unit.y () * unit.z () * ( 1 - cosine ) + unit.x () * sine
      m24 = 0.0
      
      m31 = unit.x () * unit.z () * ( 1 - cosine ) + unit.y () * sine
      m32 = unit.y () * unit.z () * ( 1 - cosine ) - unit.x () * sine
      m33 = unit.z () * unit.z () * ( 1 - cosine ) + cosine
      m34 = 0.0
      
      m41 = 0.0
      m42 = 0.0
      m43 = 0.0
      m44 = 1.0
      
      return QtGui.QMatrix4x4 ( m11, m12, m13, m14,
                                m21, m22, m23, m24,
                                m31, m32, m33, m34,
                                m41, m42, m43, m44
                              )
    cam = self.translation0 ()
    row3 = self.modelMatrix.row ( 3 ) 
    row3.setX ( 0 ) 
    row3.setY ( 0 )
    row3.setZ ( 0 )
    self.modelMatrix.setRow ( 3, row3 )
    
    mUp     = setAxisAngle ( QtGui.QVector3D ( 1.0, 0.0, 0.0 ),  DEGTORAD ( float ( -deltaUp ) * 0.05 ) ) 
    mSide   = setAxisAngle ( QtGui.QVector3D ( 0.0, 1.0, 0.0 ),  DEGTORAD ( float ( -deltaSide ) * 0.05 ) ) 
    mRoll   = setAxisAngle ( QtGui.QVector3D ( 0.0, 0.0, 1.0 ),  DEGTORAD ( self.roll ) ) 
    mUnroll = setAxisAngle ( QtGui.QVector3D ( 0.0, 0.0, -1.0 ), DEGTORAD ( self.roll ) ) 
    
    self.modelMatrix = ( mRoll * ( ( mUp * mUnroll * self.modelMatrix ) * mSide ) )
    
    # create a new cam (0,0,cam-target), mul it by cam matrix, add target
    camNew = QtGui.QVector3D ( 0.0, 0.0, ( cam - self.target ).length() )
    cam *= self.modelMatrix
    cam += self.target;
    
    row3 = self.modelMatrix.row ( 3 ) 
    row3.setX ( camNew.x () ) 
    row3.setY ( camNew.y () )
    row3.setZ ( camNew.z () )
    self.modelMatrix.setRow ( 3, row3 )
    
    """
    Imath::V3f cam(_modelMatrix.translation());
  _modelMatrix.x[3][0] = _modelMatrix.x[3][1] = _modelMatrix.x[3][2] = 0.f;
  
  Imath::M44f mUp, mSide, mRoll, mUnroll;
  mUp.setAxisAngle(Imath::V3f(1.f, 0.f, 0.f), (float)DEGTORAD((float)-deltaUp * 0.5f)); // setRotationX(deltaSide)
  mSide.setAxisAngle(Imath::V3f(0.f, 1.f, 0.f), (float)DEGTORAD((float)-deltaSide * 0.5f));// setRotationY(..)
  mRoll.setAxisAngle(Imath::V3f(0.f, 0.f, 1.f), (float)DEGTORAD(_roll));
  mUnroll.setAxisAngle(Imath::V3f(0.f, 0.f, -1.f), (float)DEGTORAD(_roll));
  
  _modelMatrix.setValue(mRoll *((mUp * mUnroll * _modelMatrix) * mSide));
  
  // create a new cam (0,0,cam-target), mul it by cam matrix, add target
  cam.setValue(0.f, 0.f, (cam - _target).length());
  cam *= _modelMatrix;
  cam += _target;
  
  _modelMatrix.x[3][0] = cam.x;
  _modelMatrix.x[3][1] = cam.y;
  _modelMatrix.x[3][2] = cam.z;
    """
    
  
  """
  void Viewport::zoom(int deltaSide){
  float newFov = _fov - (float)deltaSide * 0.5;

  if(newFov > 0){
    _fov = newFov;
    _isProjDirty = true;
  }
}

void Viewport::roll(int deltaSide){
  if(deltaSide != 0){
  
    _roll += deltaSide;
  
    Imath::M44f mRoll;
    mRoll.setAxisAngle(Imath::V3f(0.f, 0.f, 1.f), (float)DEGTORAD(deltaSide));
  
    _modelMatrix.setValue(mRoll * _modelMatrix);
  }
}
  """
  #
  # timerEvent
  #
  def timerEvent ( self, event ) :
    #
    print ">> GeomeView.timerEvent"
    self.updateGL ()  
  #
  # keyPressEvent
  #
  def keyPressEvent ( self, event ) :
    #
    print ">> GeomeView.keyPressEvent"
    QtGui.QWidget.keyPressEvent ( self, event)
  #
  # wheelEvent
  #
  def wheelEvent ( self, event ) :
    #
    print ">> GeomeView: wheelEvent ( event.delta = %f )" % event.delta ()
    if event.orientation() == QtCore.Qt.Vertical :
      self.dolly ( int ( event.delta () * -0.1 ) )
      self.isProjDirty = True
      self.updateGL ()
      
    #QtGui.QWidget.wheelEvent ( self, event)
  #
  # mousePressEvent
  #
  def mousePressEvent ( self, event ) :
    #
    #print ">> GeomeView: mousePressEvent"
    self.setFocus ()
    self.startPos = event.pos ()
    self.pressed = True
    button = event.button ()
    modifiers = event.modifiers ()
    
    if ( button == QtCore.Qt.LeftButton and modifiers == QtCore.Qt.AltModifier ) :
      self.state = 'orbit'
    elif ( button == QtCore.Qt.MidButton or ( button == QtCore.Qt.LeftButton and modifiers == QtCore.Qt.ShiftModifier ) ) :
      self.state = 'pan'
    elif ( button == QtCore.Qt.RightButton and modifiers == QtCore.Qt.ShiftModifier ) :
      self.state = 'zoom'
      print "* ZOOM from %f %f" % ( self.startPos.x(), self.startPos.y() )
    #else :
    #  QtGui.QWidget.mousePressEvent ( self, event )
  #
  # mouseDoubleClickEvent
  #
  def mouseDoubleClickEvent ( self, event ) :
    #
    #print ">> GeomeView.mouseDoubleClickEvent"
    self.emit ( QtCore.SIGNAL ( 'mouseDoubleClickEvent' ) )
    QtGui.QWidget.mouseDoubleClickEvent ( self, event )
  #
  # mouseMoveEvent
  #
  def mouseMoveEvent ( self, event ) :
    #
    #print ">> GeomeView.mouseMoveEvent"
    if self.pressed :
      currentPos = event.pos ()
      deltaPos = currentPos - self.startPos
      if self.state == 'pan' :
        self.pan ( deltaPos.x (), deltaPos.y () )
      elif self.state == 'orbit' :
        self.orbit ( deltaPos.x (), deltaPos.y () )
      elif self.state == 'zoom' :
        deltaSide = float ( deltaPos.x () * -0.1 ) # delta.x () * -0.01
        print "* zoom to %f %f (%f) " % ( currentPos.x(), currentPos.y(), deltaSide )
        self.dolly ( deltaSide )
      self.isProjDirty = True
      self.updateGL ()
      self.startPos = currentPos   
    #else :
    #  QtGui.QWidget.mouseMoveEvent ( self, event )
  #
  # mouseReleaseEvent
  #
  def mouseReleaseEvent ( self, event ) :
    #
    #print ">> GeomeView.mouseReleaseEvent"
    if self.state in [ 'pan', 'zoom', 'orbit' ] :
      self.state = 'idle'
      self.startPos = None
      self.pressed = False
    #QtGui.QWidget.mouseReleaseEvent ( self, event )
  #
  # viewportEvent
  #
  def viewportEvent ( self, event ) :
    #case QEvent::TouchBegin:
    # case QEvent::TouchUpdate:
    # case QEvent::TouchEnd:
    if event.type () == QtCore.QEvent.TouchBegin :
      print ">> ImageView: QEvent.TouchBegin"
    return QtGui.QWidget.viewportEvent ( self, event )
  #
  # resetView
  #
  def resetView ( self ) :
    #
    self.printModelMatrix ()
    self.modelMatrix.setToIdentity ()
    self.modelMatrix.translate ( 0.0, 0.0, 10.0 )
    self.target = QtGui.QVector3D ( 0.0, 0.0, 0.0 )
    self.orbit ( 45, -45 )
    self.dolly ( 240 )
    self.printModelMatrix ()
    
    self.isProjDirty = True
    self.updateGL ()



