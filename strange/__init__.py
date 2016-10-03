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
import itertools

import weasyprint as wp
import gdspy
import numpy as np

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


    @classmethod
    def via_fill_simple(cls, polygon, dimension, spacing, layer):
        """Generate standard via pattern inside ``polygon``.

        ``polygon`` is a numpy.ndarray object of this form:
                [[x1 y1]
                 [x2 y2]
                 ...    ]
        
        Vias are placed on up to the edges of ``polygon`` with
        rectangular size ``dimension`` and distance ``spacing``
        between inside edges.
        """
        step_size = dimension + spacing

        # lay down a grid.
        min_x, min_y = polygon.min(axis=0)
        max_x, max_y = polygon.max(axis=0)

        columns_x = np.arange(min_x, max_x - spacing, step_size)
        rows_y = np.arange(min_y, max_y - spacing, step_size)

        # only draw if grid points are inside ``polygon``
        offset1 = np.array([0,          dimension])
        offset2 = np.array([dimension,  0        ])
        offset3 = np.array([dimension,  dimension])
        geos = []
        for point in itertools.product(columns_x, rows_y):
            # This is a lot of checking... is there a better way?
            if cls.point_inside_shape(point, polygon) and \
               cls.point_inside_shape(point + offset1, polygon) and \
               cls.point_inside_shape(point + offset2, polygon) and \
               cls.point_inside_shape(point + offset3, polygon) :
               geos.append(gdspy.Rectangle(
                                    (point[0],           point[1]),
                                    (point[0]+dimension, point[1]+dimension),
                                    layer ))

        return geos


    @staticmethod
    def point_inside_shape(p, verts, edges=None):
        """Test whether the point p is inside the specified shape.
        The shape is specified by 'verts' and 'edges'
        Arguments:
        p - the 2d point
        verts - (N,2) array of points
        edges - (N,2) array of vert indices indicating edges
                If edges is None then assumed to be in order. I.e.
                  [[0,1], [1,2], [2,3] ... [N-1,0]]

        Returns:
        - True/False based on result of in/out test.

        Uses the 'ray to infinity' even-odd test.
        Let the ray be the horizontal ray starting at p and going to +inf in x.
        """

        ################################################
        # This method originally written by Bill Baxter,
        # posted on scipy mailing list.
        #
        # I'm using this to avoid an extra dependency,
        # but another (more optimized) option is to use
        # matplotlib as follows:
        #
        # mplPath(shape).contains_points(test_point)
        #
        # TODO: benchmark this.
        ################################################
        
        verts = np.asarray(verts)
        if edges is None:
            N = verts.shape[0]
            edges = np.column_stack([np.c_[0:N],np.append(np.c_[1:N],0)])

        inside = False
        x,y=p[0],p[1]
        for e in edges:
            v0,v1 = verts[e[0]],verts[e[1]]
            # Check if both verts to the left of ray
            if v0[0]<x and v1[0]<x:
                continue
            # check if both on the same side of ray
            if (v0[1]<y and v1[1]<y) or (v0[1]>y and v1[1]>y):
                continue
            #check for horizontal line - another horz line can't intersect it
            if (v0[1]==v1[1]):
                continue
            # compute x intersection value
            xisect = v0[0] + (v1[0]-v0[0])*((y-v0[1])/(v1[1]-v0[1]))
            if xisect >= x:
                inside = not inside
        return inside



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

