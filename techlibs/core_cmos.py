"""
Drawing functions for basic, process agnostic devices.

Process-specific features should be added on top of these devices.
"""

import gdspy
import math

from . import core_stackup
from .containers import GeometryContainer




# TODO: move this somewhere else
def _validate_bool(token):
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


def _validate_number(token):
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



def _validate_layer(token):
    token = token[0]
    if token.type=="INTEGER":
        return token.value
    elif token.type=="STRING" or token.type=="IDENT":
        try:
            return getattr(core_stackup, token.value.upper())
        except:
            pass


def _compute_distance(computer, name, value):
    """Compute a property expecting ``distance`` type"""
    # TODO : add other computations?
    # if value.unit == '%':
    #     return value.value * parent_font_size / 100.
    # else:
    #     return value.value
    return value


def _compute_bool(computer, name, value):
    """Compute a property expecting ``boolean`` type"""
    # TODO: What do I have to do here?
    return value


def _compute_layer(computer, name, value):
    """Compute the ``layer`` property"""
    # TODO: What do I have to do here?
    return value


# def contactHelper( bbH, bbW, 
#                    COsize=0.04, COspace=0.03,
#                    COoffsetY=0, COoffsetX=0 ) :
#   """
#   Draws vertical column of contacts centered within an imaginary box
#   of height bbH and width bbW.

#   The origin of the result is at the upper left corner of the box.

#   Returns: list of gdspy geometry objects, following the standard 
#            layer stackup.
#   """

#   numCO       = math.floor((bbH - COspace)/(COspace + COsize))
#   COinsetY    = (bbH - COsize - (numCO-1)*(COspace + COsize))/2.0 - \
#                   COoffsetY;
#   # from top left of contact
#   COposX      = -(rxextleft/2.0 + COsize/2.0 + COoffsetX)
    
#   contacts = []
#   for ii in range(numCO):
#       thisY = -COinsetY - ii*(COsize+COspace) 
#       contacts = contacts + [
#                   gdspy.Rectangle( (COposX,thisY),
#                                    (COposX+COsize,thisY-COsize),
#                                    core_stackup.CO )]


class Devices(object):
    # TODO: can we make this dict automagically populate?
    parameters = {
            # fet
            'co_size'       : 0.04,
            'co_space'      : 0.03,
            'co_offsety'    : 0.,
            'co_offsetx'    : 0.,
            'co_existsl'    : True,
            'co_existsr'    : True,
            'ext_top'       : 0.1,
            'ext_bot'       : 0.1,
            'ext_left'      : 0.1,
            'ext_right'     : 0.1,

            # res_poly
            'ext'           : 0.1,

            # misc
            'layer'         : 0
    }
    validators = {
            # fet
            'co_size'       : _validate_number,
            'co_space'      : _validate_number,
            'co_offsety'    : _validate_number,
            'co_offsetx'    : _validate_number,
            'co_existsl'    : _validate_bool,
            'co_existsr'    : _validate_bool,
            'ext_top'       : _validate_number,
            'ext_bot'       : _validate_number,
            'ext_left'      : _validate_number,
            'ext_right'     : _validate_number,

            # res_poly
            'ext'           : _validate_number,

            # misc
            'layer'         : _validate_layer
    }
    computers = {
            # fet
            'co_size'       : _compute_distance,
            'co_space'      : _compute_distance,
            'co_offsety'    : _compute_distance,
            'co_offsetx'    : _compute_distance,
            'co_existsl'    : _compute_bool,
            'co_existsr'    : _compute_bool,
            'ext_top'       : _compute_distance,
            'ext_bot'       : _compute_distance,
            'ext_left'      : _compute_distance,
            'ext_right'     : _compute_distance,

            # res_poly
            'ext'           : _compute_distance,

            # misc
            'layer'         : _compute_layer
    }

    layer_replace = {
        #   tag name        : (outer_layer, nested_layer1, ...)
            'pch'           : ('pw','pimp'),
            'nch'           : ('nimp',)
    }



    def __init__(self, tech):
        self.tech = tech




    def fet(    self,
                l, w,
                co_size=0.04, co_space=0.03, co_offsety=0, co_offsetx=0,
                co_existsl=True,    co_existsr=True,
                ext_top=0.1,        ext_bot=0.1,
                ext_left=0.1,       ext_right=0.1,
                **kwargs
            ) :

        """
        Responsible for drawing a fundamental FET device.

        Meant to be process agnostic, this function returns only 
        active, poly, and contact geometries. Any process-specific
        requirements should be built on top of this geometry.

        Origin of returned geometries will be the top left intersection 
        of the gate and the active area. This ensures geometries stay
        on-grid after being built.

        **kwargs is ignored. It is included to allow for passing of a 
        style dictionary with more entries than those required by this
        function.

        Returns: geometryContainer
            A geometryContainer with all gdspy geometries for this device.
        """

        if l<=0:
            raise Exception("FATAL: Can't have negative legnth device.")
        if w<=0:
            raise Exception("FATAL: Can't have negative width device.")

        # Draw gate
        gate = gdspy.Rectangle((0,ext_top), (l,-(w+ext_bot)), core_stackup.PO);

        # Draw RX
        active = gdspy.Rectangle(
                        (-ext_left,0),
                        (l+ext_right,-w),
                        core_stackup.RX
                    );

        # Draw CO
        num_co        = int( math.floor((w - co_space)/(co_space + co_size)) )
        co_inset_y    = (w - co_size - (num_co-1)*(co_space + co_size))/2.0;
        # from bot left of contact
        co_pos_xleft  = -(ext_left/2.0 + co_size/2.0 + co_offsetx)
        co_pos_xright =   ext_right/2.0 - co_size/2.0 + co_offsetx + l
        contacts_left  = []
        contacts_right = []
        for ii in range(num_co):
            thisY = -w + co_inset_y + ii*(co_size+co_space)
            
            contacts_left = contacts_left + [
                    gdspy.Rectangle( (co_pos_xleft,thisY),
                                     (co_pos_xleft+co_size,thisY+co_size),
                                      core_stackup.CO   )]
            contacts_right = contacts_right + [
                    gdspy.Rectangle( (co_pos_xright,thisY),
                                     (co_pos_xright+co_size,thisY+co_size),
                                      core_stackup.CO )]

        # Build Container
        geometeries = [gate, active] + contacts_left + contacts_right
        extents = (+ext_top, l+ext_right, -(w+ext_bot), -ext_left)
        return GeometryContainer(geometeries, extents, self.tech).translate( \
                                    (-extents[3], -extents[0]) )


    def res_poly ( self, 
                   l, w, 
                   ext=0.1, co_size=0.04, co_space=0.03,
                   **kwargs ) :
        """
        Responsible for drawing a fundamental poly resistor.

        This function draws poly and contact layers for a poly resistor. The 
        length of the resistor is measured from the inside edges of the
        contacts.

        Origin of returned geometries will be the top left corner of the 
        resistor boundary (inside edge of left contacts)

        **kwargs is ignored. It is included to allow for passing of a style
        dictionary with more entries than those required by this function.

        Returns: geometryContainer
            A geometryContainer with all gdspy geometries for this device.
        """

        # Draw PO
        poly = gdspy.Rectangle((-ext,0), (l+ext,-w), core_stackup.PO);

        # Draw CO
        num_co       = int( math.floor((w - co_space)/(co_space + co_size)) )
        co_inset_y    = (w - co_size - (num_co-1)*(co_space + co_size))/2.0;
        co_pos_xleft  = -co_size   # from bot left of contact
        co_pos_xright = l
        contacts_left = []
        contacts_right = []
        for ii in range(num_co):
            thisY = -w + co_inset_y + ii*(co_size+co_space)
            
            contacts_left = contacts_left + [
                    gdspy.Rectangle( (co_pos_xleft,thisY),
                                     (co_pos_xleft+co_size,thisY+co_size),
                                      core_stackup.CO )]
            contacts_right = contacts_right + [
                    gdspy.Rectangle( (co_pos_xright,thisY),
                                     (co_pos_xright+co_size,thisY+co_size),
                                      core_stackup.CO )]

        # Build Container
        geometeries = [poly] + contacts_left + contacts_right
        extents = (0., l+ext, w, -ext)
        return GeometryContainer(geometeries, extents, self.tech).translate( \
                                    (-extents[3], -extents[0]) )


