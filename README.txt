 
meShaderEd.py is a node based shader editor. 
Besides only RSL nodes, it allows to build networks with RIB nodes.
 
Written by Yuri.Meshalkin (mesh@kpp.kiev.ua)

 Initial version -- 0.0.1 (5 Mar 2011)

 Initial code and data structure was based on 
 ShaderLink of Libero Spagnolini (Libe)
   http://libe.ocracy.org/shaderlink.html
   http://code.google.com/p/shaderlink/

 And idea of open source RSL tool belongs to Alexei Puzikov (Kidd)
   http://code.google.com/p/shaderman/


 To start this program -- run: python ./meShaderEd.py
 
 Supported OS: Windows, MacOSX, Linux
 (Tested on : Win7(Win8), OSX Lion 10.7(10.8), Ubuntu 12.04)  
 
 Software requirements:
 
 Python (2.5 - 2.7)
 PyQt 
 PIL (only for Windows)
  
meShaderEd supports all Renderman compliant renderers and shader compilers,
that are accessible by PATH environment variable in your system. 
Currently it was tested with PRMan, 3Delight, Air (partly with Pixie and RenderDotC)

Main features:

* All nodes are in XML format 
* Node networks also stored in XML format
* Clipboard Copy/Paste operations use XML format also. 
  You can copy any nodes to clipboard, paste them to text editor, edit and paste back to meShaderEd
* Inside XML code nodes can contain Python code for further functionality enhancement. 
  This allows to write dynamic nodes with ability to control parameters and node behaviour.
