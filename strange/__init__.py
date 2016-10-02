# coding: utf-8
"""
    strange
    ==========

    Working towards a modernized analog circuit design toolchain.

    This is an alpha development; the features will be pretty
    fluid as we start to look for the best solutions to design
    problems. A stable version will be released in a new repo
    with the release name ("strange" is just a project codename).

    The layout engine is largely based on WeasyPrint, with
    the renderer modified to support gds output. Also, the
    modifications are designed so that most updates from 
    WeasyPrint should translate very easily translate to this
    module.

"""

import pkgutil
import os
import sys

import weasyprint as wp
import gdspy

from . import weasyprint_patches as wp_patches


VERSION = '0.0'
__version__ = VERSION

# Used for 'User-Agent' in HTTP and 'Creator' in PDF
VERSION_STRING = 'strange %s ' % VERSION

__all__ = ['HTML', 'VERSION', 'VERSION_STRING']



###############################################################################
# Monkeypatch all the things
#
# So, WeasyPrint isn't built to allow us to inherit+override its methods,
# so we're accomplishing basically the same thing by monkeypatching.
#
# This sucks, but it allows us to keep getting updates from WeasyPrint
# without having to manually merge hacked files, which would suck more.
###############################################################################

wp_patches.patch(wp)



###############################################################################
# User Interface.
###############################################################################

HTML = wp.HTML



###############################################################################
# Tools for library creation.
###############################################################################

class LibTools(object):
    """Container class for strange's library creation tools."""

    stackup = None

    ### Device Tools
    @classmethod
    def generate_device_interface(cls, pins, nets, geometries):
        """Create an interface that associates a device's ``pins`` with the
        ``nets`` they connect to and the ``geometries`` that represent that
        interface.
        """

        interface = {}
        for ii, pin in enumerate(pins):
            interface[pin] = (nets[ii], geometries[ii])

        return interface


    ### CSS Validators
    @staticmethod
    def validate_bool(token):
        token = token[0]
        if token.type=='STRING':
            if token.value.lower() == 'true':
                return True
            elif token.value.lower() == 'false':
                return False
        elif token.type=='IDENT':
            if token.value.lower() == 'true':
                return True
            elif token.value.lower() == 'false':
                return False


    @staticmethod
    def validate_number(token):
        units_si = {
            'Y': 1e24,  # yotta
            'Z': 1e21,  # zetta
            'E': 1e18,  # exa
            'P': 1e15,  # peta
            'T': 1e12,  # tera
            'G': 1e9,   # giga
            'M': 1e6,   # mega
            'K': 1e3,   # kilo
            'c': 1e-2,  # centi
            'm': 1e-3,  # milli
            'u': 1e-6,  # micro
            'n': 1e-9,  # nano
            'p': 1e-12, # pico
            'f': 1e-15, # femto
            'a': 1e-18, # atto
            'z': 1e-21, # zepto
            'y': 1e-24  # yocto
        }

        token = token[0]
        if token.type == 'INTEGER' or token.type == 'NUMBER':
            return token.value

        # TODO: support dimension
        # elif token.type == 'DIMENSION':
        #     if token.unit == 'px':
        #         return token.value * (self.tech.precision/self.tech.units)
        #     else:
        #         return token.value * units_si[token.unit[0]]/self.tech.units



    ### CSS Computers
    @staticmethod
    def compute_distance(computer, name, value):
        """Compute a property expecting ``distance`` type"""
        # TODO : add other computations?
        # if value.unit == '%':
        #     return value.value * parent_font_size / 100.
        # else:
        #     return value.value
        return value


    @staticmethod
    def compute_bool(computer, name, value):
        """Compute a property expecting ``boolean`` type"""
        # TODO: What do I have to do here?
        return value

