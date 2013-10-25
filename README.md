meShaderEd ("construct" branch)
==========

This is a node based shader editor. 
Besides only RSL nodes, it allows to build networks with RIB nodes.

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
