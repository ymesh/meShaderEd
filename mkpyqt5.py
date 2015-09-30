#!/usr/bin/python
##################################################################################
#
#  Shaderlink 0.4 - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2009 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################


# Copyright (c) 2007-9 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import os
import platform
import stat
import sys
from core.mePyQt import QtCore, PythonQtType

if QtCore.QT_VERSION < 0x50000 : pass

__version__ = "1.0.4"

print '* Python %s' % sys.version
print '* QT_VERSION = %0X' % QtCore.QT_VERSION
print '* PYQT_VERSION = %0X' % QtCore.PYQT_VERSION

if PythonQtType != 'PyQt5' :
	print ( '! This script supposed to work with PyQt5 only ...' )
	sys.exit()

if sys.platform.startswith("win"):
	#PATH = os.path.join(os.path.dirname(sys.executable), "Lib/site-packages/PyQt4")
	PATH = os.path.dirname ( sys.executable )
else:
	app = QtCore.QCoreApplication ( [] )
	PATH = unicode ( app.applicationDirPath () )
	del app
if sys.platform.startswith ( "darwin" ):
	i = PATH.find ("Resources" )
	if i > -1:
		PATH = PATH[:i] + "bin"
	PYUIC5 = "/System/Library/Frameworks/Python.framework/Versions/2.7/bin/pyuic4"
else :
	PYUIC5 = os.path.join ( PATH, "pyuic5" ) # e.g. PYUIC5 = "/usr/bin/pyuic5"

if sys.platform.startswith ( "darwin" ):
# PYUIC5 = os.path.dirname(sys.executable)
# i = PYUIC5.find("Resources")
# if i > -1:
# 	PYUIC5 = PYUIC5[:i] + "Lib/python2.5/site-packages/PyQt4/uic/pyuic.py"
	PYRCC5 = "/System/Library/Frameworks/Python.framework/Versions/2.7/bin/pyrcc4"
	PYLUPDATE5 = "/System/Library/Frameworks/Python.framework/Versions/2.7/bin/pylupdate4"
else :
	PYRCC5 = os.path.join ( PATH, "pyrcc5" )
	PYLUPDATE5 = os.path.join ( PATH, "pylupdate5" )

LRELEASE = "lrelease"
if platform.system () == "Windows" :
	PYUIC5 = PYUIC5.replace ( "/", "\\" ) + ".bat"
	PYRCC5 = PYRCC5.replace ( "/", "\\" ) + ".exe"
	PYLUPDATE5 = PYLUPDATE5.replace ( "/", "\\" ) + ".exe"

msg = []
if not os.access ( PYUIC5, os.F_OK ) :
	msg.append ( "failed to find pyuic5; tried %s" % PYUIC5 )
if not os.access(PYRCC5, os.F_OK):
	msg.append ( "failed to find pyrcc5; tried %s" % PYRCC5 )
if not os.access ( PYLUPDATE5, os.F_OK ):
	msg.append ( "failed to find pylupdate5; tried %s" % PYLUPDATE5 )
if msg :
	print "\n".join ( msg )
	print "try manually editing this program to put the correct " + \
				"paths in place"
	sys.exit()
#if sys.platform.startswith("darwin"):
#  PYUIC5 = "/usr/bin/pyuic5"
#  PYRCC5 = "/usr/bin/pyrcc5"
	
print "PYUIC5 = %s" % PYUIC5 
print "PYRCC5 = %s" % PYRCC5
print "PYLUPDATE5 = %s" % PYLUPDATE5 

Debug = False
Verbose = False

def usage () :
	print """usage: mkpyqt5.py [options] [path]

Options (which can be given in any of the forms shown):
-b  --build      build [default]
-c  --clean      clean
-f  --force      force
-t  --translate  translate
-r  --recurse    recurse
-v  --verbose    verbose
-D  --debug      debug
path defaults to .

If executed with no arguments (or with a build argument) it does a
build, i.e., it looks for all *.ui and *.qrc files and makes sure that
the corresponding ui_*.py and qrc_*.py files exist and are up-to-date.

If executed with clean, deletes all ui_*.py and qrc_*.py files that have
corresponding *.ui and *.qrc files, and all *.pyc and *.pyo files.

If executed with force, it does a clean followed by a build.

If building and the translate option is given, after building, it runs
pylupdate4 on all .py and .pyw files it encounters, and then runs lrelease
on all .ts files it encounters. It does not use a .pro file so the .ts
files must be created in the first place, e.g., using pylupdate4 on one
of the source files and using its -ts option.

WARNING: Do not give any hand-coded files names that match ui_*.py or
qrc_*.py since these will be deleted by mkpyqt.py clean!

NOTE: If any tool fails to run, e.g., pyuic5, then edit this program and
hard-code the path; the variables with the tool paths are near the top
of the file.

mkpyqt.py v %s. Copyright (c) 2007-9 Qtrac Ltd. All rights reserved.
""" % __version__
	sys.exit()


def report_failure ( command, args, process ) :
	msg = ""
	ba = process.readAllStandardError ()
	if not ba.isEmpty () :
		msg = ": " + str ( ba )
	print "failed", command, " ".join ( args ), msg

def build ( path ) :
	for name in os.listdir ( path ) :
		source = os.path.join ( path, name )
		target = None
		if source.endswith ( ".ui" ) :
			target = os.path.join ( path, name.replace (".ui", ".py") )
			command = PYUIC5
		elif source.endswith ( ".qrc" ) :
			( fname, fext ) = os.path.splitext ( name )
			target = os.path.join ( path, fname + "_rc.py" )
			#target = os.path.join ( path, "qrc_" + name.replace(".qrc", ".py" ) )
			command = PYRCC5
		process = QtCore.QProcess ()
		if target is not None :
			if not os.access ( target, os.F_OK) or (
			 os.stat ( source ) [ stat.ST_MTIME ] > \
			 os.stat ( target ) [ stat.ST_MTIME ] ):
				args = [ "-o", target, source ]
				if sys.platform.startswith ( "darwin") and command == PYUIC5 :
					#command = sys.executable
					#args = [PYUIC4] + args
					command = PYUIC5
				if Debug:
					print "# %s %s" % ( command, " ".join ( args ) )
				else:
					if Verbose :
						print "# %s %s" % ( command, " ".join ( args ) )
					process.start ( command, args )
					if not process.waitForFinished (2 * 60 * 1000) :
						report_failure ( command, args, process )
					else :
						print source, "->", target
			elif Verbose :
				print source, "is up-to-date"

def clean ( path ) :
	deletelist = []
	for name in os.listdir ( path ) :
		target = os.path.join ( path, name )
		source = None
		if target.endswith ( ".py" ) or target.endswith ( ".pyc" ) or \
			target.endswith ( ".pyo" ) :
			if name.startswith ( "ui_" ) and not name [ -1 ] in "oc" :
				source = os.path.join ( path, name [ 3:-3 ] + ".ui" )
			elif name.startswith ("qrc_" ) :
				if target [ -1 ] in "oc" :
					source = os.path.join ( path, name [ 4:-4 ] + ".qrc" )
				else:
					source = os.path.join ( path, name [ 4:-3 ] + ".qrc" )
			elif target [ -1 ] in "oc":
				source = target [ :-1 ]
			if source is not None :
				if os.access ( source, os.F_OK ) :
					if Debug :
						print "# delete ", target
					else:
						deletelist.append ( target )
				else:
					print "will not remove '%s' since `%s' not found" % (	target, source )
	if not Debug :
		for target in deletelist :
			if Verbose:
				print "deleted", target
			os.remove(target)

def translate ( path ) :
	files = []
	tsfiles = []
	for name in os.listdir ( path ) :
		if name.endswith ( (".py", ".pyw" ) ) :
			files.append(os.path.join(path, name))
		elif name.endswith ( ".ts" ) :
			tsfiles.append ( os.path.join ( path, name ) )
	if not tsfiles :
		return
	verbose = "-verbose" if Verbose else ""
	silent = "-silent" if not Verbose else ""
	process = QtCore.QProcess ()
	for ts in tsfiles :
		qm = ts [ :-3 ] + ".qm"
		command1 = PYLUPDATE5
		args1 = [ verbose ] + files + [ "-ts", ts ]
		command2 = LRELEASE
		args2 = [ silent, ts, "-qm", qm ]
		if Debug :
			print "updated", ts
			print "generated", qm
		else:
			process.start ( command1, args1 )
			if not process.waitForFinished ( 2 * 60 * 1000 ) :
				report_failure ( command1, args1, process )
			process.start ( command2, args2 )
			if not process.waitForFinished ( 2 * 60 * 1000 ) :
				report_failure ( command2, args2, process )

def apply ( recurse, function, path ):
	if not recurse :
		function ( path )
	else:
		for root, dirs, files in os.walk ( path ) :
			for dir in dirs :
				function ( os.path.join ( root, dir ) )

def main () :
	global Debug, Verbose
	function = build
	recurse = False
	trans = False
	force = False
	path = "."
	args = sys.argv [1:]
	while args:
		arg = args.pop ( 0 )
		if arg in ( "-D", "--debug", "debug" ) :
			Debug = True
		elif arg in ( "-b", "--build", "build" ):
			pass # This is the default
		elif arg in ( "-c", "--clean", "clean" ) :
			function = clean
		elif arg in ( "-f", "--force", "force" ) :
			force = True
		elif arg in ( "-t", "--translate", "translate" ) :
			trans = True
		elif arg in ( "-r", "--recurse", "recurse" ) :
			recurse = True
		elif arg in ( "-v", "--verbose", "verbose" ) :
			Verbose = True
		elif arg in ( "-h", "--help", "help" ):
			usage ()
		else:
			path = arg
	if not force:
		apply (recurse, function, path )
	else:
		apply ( recurse, clean, path )
		apply ( recurse, build, path )
	if trans and ( function == build or force ):
		apply ( recurse, translate, path )

main()

# 1.0.1 Fixed bug reported by Brian Downing where paths that contained
#       spaces were not handled correctly.
# 1.0.2 Changed default path on Windows to match PyQt 4.4
# 1.0.3 Tried to make the paths work on Mac OS X
# 1.0.4 modified for work with PyQt5 (by Yuri Meshalkin)
