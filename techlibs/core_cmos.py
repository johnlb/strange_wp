# coding: utf-8
"""Drawing functions for basic, process agnostic devices.

Process-specific features should be added on top of these devices.
"""

import gdspy
import math

from . import core_stackup
from strange.containers import DeviceContainer
from strange import LibTools



def _validate_layer(token):
    token = token[0]
    if token.type=="INTEGER":
        return token.value
    elif token.type=="STRING" or token.type=="IDENT":
        try:
            return getattr(core_stackup, token.value.upper())
        except:
            pass


def _compute_layer(computer, name, value):
    """Compute the ``layer`` property"""
    # TODO: What do I have to do here?
    return value



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
            'ext_bottom'    : 0.1,
            'ext_left'      : 0.1,
            'ext_right'     : 0.1,

            # res_poly
            'ext'           : 0.1,

            # misc
            'layer'         : 0
    }
    validators = {
            # fet
            'co_size'       : LibTools.validate_number,
            'co_space'      : LibTools.validate_number,
            'co_offsety'    : LibTools.validate_number,
            'co_offsetx'    : LibTools.validate_number,
            'co_existsl'    : LibTools.validate_bool,
            'co_existsr'    : LibTools.validate_bool,
            'ext_top'       : LibTools.validate_number,
            'ext_bottom'    : LibTools.validate_number,
            'ext_left'      : LibTools.validate_number,
            'ext_right'     : LibTools.validate_number,

            # res_poly
            'ext'           : LibTools.validate_number,

            # misc
            'layer'         : _validate_layer
    }
    computers = {
            # fet
            'co_size'       : LibTools.compute_distance,
            'co_space'      : LibTools.compute_distance,
            'co_offsety'    : LibTools.compute_distance,
            'co_offsetx'    : LibTools.compute_distance,
            'co_existsl'    : LibTools.compute_bool,
            'co_existsr'    : LibTools.compute_bool,
            'ext_top'       : LibTools.compute_distance,
            'ext_bottom'    : LibTools.compute_distance,
            'ext_left'      : LibTools.compute_distance,
            'ext_right'     : LibTools.compute_distance,

            # res_poly
            'ext'           : LibTools.compute_distance,

            # misc
            'layer'         : _compute_layer
    }

    layer_replace = {
        #   tag name        : (outer_layer, nested_layer1, ...)
            'pch'           : ('pw','pimp'),
            'nch'           : ('nimp',),
            'ntap'          : ('pimp','rx')
    }



    def __init__(self, tech):
        self.tech = tech




    def fet(    self,
                l, w,
                co_size=0.04, co_space=0.03, co_offsety=0, co_offsetx=0,
                co_existsl=True,    co_existsr=True,
                ext_top=0.1,        ext_bottom=0.1,
                ext_left=0.1,       ext_right=0.1,
                g='',s='',d='',b='',
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

        Returns: (geometry_container, netlist)
            A DeviceContainer object with all gdspy geometries 
            for this device and the netlist 
        """

        if l<=0:
            raise Exception("FATAL: Can't have negative legnth device.")
        if w<=0:
            raise Exception("FATAL: Can't have negative width device.")

        # Draw gate
        gate = gdspy.Rectangle((0,ext_top), (l,-(w+ext_bottom)), core_stackup.PO);

        # Draw active area
        active = gdspy.Rectangle(
                        (-ext_left,0),
                        (l+ext_right,-w),
                        core_stackup.RX
                    );

        # Draw contacts
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

        # Build Netlist
        interface = LibTools.generate_device_interface( \
            ('g',  's',           'd',            'b'),
            ( g ,   s ,            d ,             b ),
            ( gate, contacts_left, contacts_right, []) \
        )

        # Build Container
        geometeries = [gate, active] + contacts_left + contacts_right
        extents = (+ext_top, l+ext_right, -(w+ext_bottom), -ext_left)
        return DeviceContainer(geometeries, interface, self.tech,
                                extents).translate(
                                               (-extents[3],
                                                -extents[0]) )



    def res_poly ( self, 
                   l, w, 
                   ext=0.1, co_size=0.04, co_space=0.03,
                   p='', n='',
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

        Returns: (geometry_container, interface)
            A DeviceContainer object with all gdspy geometries 
            for this device and the interface 
        """

        # Draw poly
        poly = gdspy.Rectangle((-ext,0), (l+ext,-w), core_stackup.PO);

        # Draw contacts
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

        # Build Netlist
        interface = LibTools.generate_device_interface( \
            ('p',           'n'),
            ( p ,            n ),
            ( contacts_left, contacts_right) \
        )

        # Build Container
        geometeries = [poly] + contacts_left + contacts_right
        extents = (0., l+ext, w, -ext)
        return DeviceContainer(geometeries, netlist, self.tech,
                                interface, extents).translate(
                                                        (-extents[3],
                                                         -extents[0]) )


