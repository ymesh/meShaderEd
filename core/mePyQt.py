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
usePySide = False
usePyQt4 = False
usePyQt5 = False

try:
	PythonQt = __import__( 'PySide', globals(), locals(), List )
	PythonQtType = 'PySide'
	usePySide = True
except ImportError:
	try:
		PythonQt = __import__( 'PyQt5', globals(), locals(), List )
		PythonQtType = 'PyQt5'
		usePyQt5 = True
	except ImportError:
		try:
			PythonQt = __import__( 'PyQt4', globals(), locals(), List )
			PythonQtType = 'PyQt4'
			usePyQt4 = True
		except ImportError:
			pass

print ( '* ' + PythonQtType + ' module imported' )

if usePySide :
	print ( '* ' + 'PySide.qVersion = %s' % PythonQt.QtCore.qVersion() )	
else :
	print ( '* ' + 'QT_VERSION = %x' % PythonQt.QtCore.QT_VERSION )

#if not PySide :
#	Qt = PythonQt.Qt
QtCore 		= PythonQt.QtCore
QtGui 		= PythonQt.QtGui
QtXml 		= PythonQt.QtXml
#QtNetwork = PythonQt.QtNetwork
if usePyQt5 :
	QtWidgets = PythonQt.QtWidgets



