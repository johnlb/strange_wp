"""Generic 40nm Planar CMOS technology setup.

Uses 'core_cmos' device library
"""

from techlibs.core_cmos import *
from techlibs.core_stackup import *
# import stackup


# # remove so import * doesn't pollute
# del(globals()[imp])
# del(globals()[core])