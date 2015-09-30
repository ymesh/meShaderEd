"""
	
	mePyQt.py
	
	PyQt wrapper allows to use the same code (almost) with different
	PyQt implementation: PySide, PyQt4, PyQt5
	
	This code is based on cgrupyqt.py from CGRU project
"""
List = [ 'QtCore', 
				 'QtGui', 
				 #'QtNetwork', 
				 'QtXml', 
				 'QtWidgets', 
				 'Qt' 
			 ]

PythonQtType = None
PySide = True

try:
	PythonQt = __import__( 'PySide', globals(), locals(), List )
	PythonQtType = 'PySide'
except ImportError:
	try:
		PythonQt = __import__( 'PyQt5', globals(), locals(), List )
		PythonQtType = 'PyQt5'
	except ImportError:
		PythonQt = __import__( 'PyQt4', globals(), locals(), List )
		PythonQtType = 'PyQt4'

print ( '* ' + PythonQtType + ' module imported' )
print ( '* ' + 'QT_VERSION = %x' % PythonQt.QtCore.QT_VERSION )

Qt 				= PythonQt.Qt
QtCore 		= PythonQt.QtCore
QtGui 		= PythonQt.QtGui
QtXml 		= PythonQt.QtXml
if QtCore.QT_VERSION >= 0x50000 :
	QtWidgets = PythonQt.QtWidgets
#QtNetwork = PythonQt.QtNetwork



if PythonQtType == 'PyQt4' or PythonQtType == 'PyQt5':
	#print('You can install PySide if interested in LGPL license.')
	PySide = False
#
# GetOpenFileName
#
def GetOpenFileName ( i_qwidget, i_title, i_path = None ) :
	if i_path is None :
		i_path = '.'
	if PySide :
		afile, filter = \
			QtGui.QFileDialog.getOpenFileName ( i_qwidget, i_title, i_path )
		return afile
	return str ( QtGui.QFileDialog.getOpenFileName ( i_qwidget, i_title, i_path ) )
#
# GetSaveFileName
#
def GetSaveFileName ( i_qwdget, i_title, i_path = None ) :
	if i_path is None :
		i_path = '.'
	if PySide :
		afile, filter = \
			QtGui.QFileDialog.getSaveFileName ( i_qwdget, i_title, i_path )
		return afile
	return str ( QtGui.QFileDialog.getSaveFileName ( i_qwdget, i_title, i_path ) )
