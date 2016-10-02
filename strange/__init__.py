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


    # @classmethod
    # def generate_netlist(cls, nets, geometries, interfaces):
    #     """Create a ``netlist`` dictionary which connects each net in ``nets``
    #     to the explicit geometry objects that act as said interface.
    #     """

    #     netlist = {}
    #     for net in nets:


    #     for ii, pin in enumerate(pins):
    #         netlist[pin] = (nets[ii], geometries[ii])

    #     return netlist