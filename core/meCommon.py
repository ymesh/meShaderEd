"""
 
 meCommon.py

"""
import os, sys
from core.mePyQt import usePySide, usePyQt4, usePyQt5, QtCore
#
# findExecutable
#
def findExecutable ( executable, path = None ) :
	"""Try to find 'executable' in the directories listed in 'path' (a
	string listing directories separated by 'os.pathsep'; defaults to
	os.environ['PATH']).  Returns the complete filename or None if not
	found
	"""
	if path is None:
		path = os.environ [ 'PATH' ]
	paths = path.split(os.pathsep)
	extlist = [ '' ]
	if os.name == 'os2' :
		( base, ext ) = os.path.splitext ( executable )
		# executable files on OS/2 can have an arbitrary extension, but
		# .exe is automatically appended if no dot is present in the name
		if not ext:
			executable = executable + ".exe"
	elif sys.platform == 'win32' :
		pathext = os.environ [ 'PATHEXT' ].lower ().split ( os.pathsep )
		(base, ext) = os.path.splitext(executable)
		if ext.lower() not in pathext:
			extlist = pathext
	for ext in extlist:
		execname = executable + ext
		if os.path.isfile( execname ):
			return execname
		else:
			for p in paths:
				f = os.path.join(p, execname)
				if os.path.isfile(f):
					return f
	else:
		return None
#
# createMissingDirs
#
def createMissingDirs ( dirList = None ):   
	#
	for dirName in dirList :
		#print '-> Check dir %s' % dirName    
		if not os.path.exists ( dirName ) : 
			print '-> Create missing dir %s' % dirName    
			os.makedirs ( dirName )

#
# Use this hack, as os.path.normpath doesn't work on windooze,
# but QtCore.QDir works fine ...
#
def normPath ( pathName ) :
	result = ''
	if pathName != '' :
		if ( sys.platform == 'win32' ) :
			result = str ( QtCore.QDir( pathName ).absolutePath() )  
		else :
			result = os.path.normpath ( str( pathName ) )
	return result  
#
# replace C:/ with //C/ for RIB search path names
#
def sanitizeSearchPath ( pathName ) :
	#print ':: sanitizeSearchPath %s' %  pathName
	sanitizedPath = pathName
	if ( sys.platform == 'win32' ) :
		if pathName[1:2] == ':' :
			sanitizedPath = ( '//' + pathName[0:1] + pathName[2:] )
	return sanitizedPath
#
# is pathname relative ? 
#
def isRelativePath ( pathName ) :
	isRelative = True
	if ( sys.platform == 'win32' ) :
		if pathName[1:2] == ':' : isRelative = False
	if pathName[0:1] == '\\' or pathName[0:1] == '/' : 
		isRelative = False
	return isRelative     
#
# get pathName relative to rootPath 
#
def toRelativePath ( rootPath, pathName ) :
	#print ':: toRelativePath %s' %  pathName
	relativePath = pathName
	if not isRelativePath ( pathName ) :
		if pathName.find ( rootPath ) != -1 :
			relativePath = pathName[ len( rootPath ) + 1 :  ]  
		
	return relativePath
#
# get full pathName from relative to rootPath 
#
def fromRelativePath ( rootPath, pathName ) :
	#print ':: fromRelativePath %s' %  pathName
	fullPath = pathName
	if isRelativePath ( pathName ) :
		fullPath = os.path.join ( rootPath, pathName )
		
	return normPath ( fullPath )  
#
# launch process
#
def launchProcess ( cmdList, stdoutLog = None, stderrLog = None ) :
	#
	# subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None,
	#
	import subprocess, errno
	
	stdout = None
	stderr = None
	if stdoutLog is not None : stdout = file ( stdoutLog, 'w' )
	if stderrLog is not None : stderr = file ( stderrLog, 'w' )  
	
	try:
		if sys.platform.startswith ( 'linux' ) :
			( sysname, nodename, release, version, machine ) = os.uname()
			#print 'sysname = %s' % sysname
			#print 'release = %s' % release
			#print 'version = %s' % version
			if version.find ( 'Ubuntu' ) != -1 :
				print 'Ubuntu'
				#retval = os.popen ( ' '.join ( cmdList ), 0, None, None, stdout, stderr )
				retval = subprocess.Popen ( ' '.join ( cmdList ), 0, None, None, stdout, stderr )
			else :
				retval = subprocess.call ( cmdList, 0, None, None, stdout, stderr )  
		else:        
			retval = subprocess.call ( cmdList, 0, None, None, stdout, stderr )
	except OSError, e :
		if e.errno != errno.EINTR : raise
	
	if stdout is not None : stdout.close ()
	if stderr is not None : stderr.close ()

	return retval
#
# getUniqueName
#
def getUniqueName  ( name, nameList ) :
	#
	newName = name
	sfx = 0
	while newName in nameList :
		newName = name + str ( sfx )
		sfx += 1
	return str( newName )  
#
# getParsedLabel
#
def getParsedLabel ( text ) :
	#
	newLabel = str ( text ).strip ()
	newLabel = newLabel.replace ( ' ', "_" )
	return newLabel  
#
# parseGlobalVars
#
def parseGlobalVars ( inputStr ) :
	#
	from global_vars import app_global_vars, DEBUG_MODE
	#if DEBUG_MODE : print '-> parseGlobalVars in %s' % parsedStr
	resultStr = ''
	parserStart = 0
	parserPos = 0
	parsedStr = str ( inputStr )

	while parserPos != -1 :
		parserPos = parsedStr.find ( '$', parserStart )
		if parserPos != -1 :
			#
			if parserPos != 0 :
				resultStr += parsedStr [ parserStart : parserPos ]

			# check global vars first
			if parsedStr [ ( parserPos + 1 ) : ( parserPos + 2 ) ] == '{' :
				globStart = parserPos + 2
				parserPos = parsedStr.find ( '}', globStart )
				global_var_name = parsedStr [ globStart : ( parserPos ) ]

				#print '-> found global var %s' % global_var_name

				if global_var_name in app_global_vars.keys () :
					resultStr += app_global_vars [ global_var_name ]
			else :
				# keep $ sign for otheer, non ${...} cases
				resultStr += '$'

		#print 'parserPos = %d parserStart = %d' % ( parserPos, parserStart )
		if parserPos != -1 :
			parserStart = parserPos + 1

	resultStr += parsedStr [ parserStart: ]

	return resultStr