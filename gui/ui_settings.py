#
# ui_settings.py
#
import sys

CHECK_WIDTH = 20
if ( sys.platform == 'darwin' ) : 
  CHECK_WIDTH = 25
BROWSE_WIDTH = 24
LABEL_WIDTH = 140
NODE_LABEL_WIDTH = 80
EDIT_WIDTH = 160
FIELD_WIDTH = 60
if ( sys.platform == 'darwin' ) : 
  FIELD_WIDTH = 80
COLOR_WIDTH = 60

SPACING = 4
if ( sys.platform == 'darwin' ) : 
  SPACING = 2
  
HEIGHT = 20

COMBO_WIDTH = 120
COMBO_HEIGHT = 22
if ( sys.platform == 'darwin' ) : 
  COMBO_HEIGHT = 24
MAX = 16777215
LT_SPACE = CHECK_WIDTH
TAB_SIZE = 10

FONT_HEIGHT = 10
if ( sys.platform == 'darwin' ) : 
  FONT_HEIGHT = 12
  
SWATCH_SIZE = 64

