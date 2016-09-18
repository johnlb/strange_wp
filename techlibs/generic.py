"""Generic 40nm Planar CMOS technology setup.

Uses 'core_cmos' device library
"""

###############################################################################
# Import external libraries
###############################################################################
from techlibs.core_cmos import *
from techlibs.core_stackup import *
# import stackup


###############################################################################
# Find location of the default stylesheet.
# This is required for all techlibs.
###############################################################################
import os
default_stylesheet = os.path.abspath(__file__)
default_stylesheet = os.path.dirname(default_stylesheet) + '/generic.css'


###############################################################################
# Define primary gds dimensions.
# - 'precision' specifies the grid size (typ. 5nm)
# - 'units' specifies the dimension everything is normalized to (typ. 1um)
###############################################################################
precision 	= 5e-9
units 		= 1e-6