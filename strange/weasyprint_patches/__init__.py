# coding: utf-8
"""Patch WeasyPrint methods to support gds output.

	Provides patch() function. Usage:
	patch(weasyprint_module_instance)
"""

################################################################################
# Notes on mokeypatching:
#
# - I'm sorry.
# - functions retain the scope they were defined in *after* patching.
#     Therefore, in every module there is a global "scope" variable
#     that is soft-patched (inside patch() fn) to the global scope
#     the function is patched into. That variable is assumed valid
#     at runtime and can be used to read/modify variables in the new
#     scope.
# - Also, I'm sorry.
################################################################################


__all__ = ['patch', 'tech']


import imp
from lxml import etree
from copy import deepcopy

import techlibs.containers as containers

geometryContainer = containers.GeometryContainer

scope   = None      # set inside patch()


###############################################################################
# Helper methods
###############################################################################

def load_local_module(name):
    return imp.load_module(name, *imp.find_module(name,__path__))

def load_global_module(name):
    return imp.load_module(name, *imp.find_module(name))



###############################################################################
# Load everything what needs patching
###############################################################################

draw        = load_local_module('draw')
doc         = load_local_module('document')
html        = load_local_module('html')
css         = load_local_module('css')
technology  = load_local_module('technology')
validation  = load_local_module('validation')
header_script_sandbox   = load_local_module('header_script_sandbox')
body_script_sandbox     = load_local_module('body_script_sandbox')
computed_values         = load_local_module('computed_values')



###############################################################################
# Main Method
###############################################################################

def patch(wp):
    """Runs all patches needed to teach WeasyPrint about gds."""

    global scope
    scope = wp

    # Give each module access to the scope they're patched into...
    #   For the life of me, I can't find a better way to do this.
    draw.scope          = wp.draw
    doc.scope           = wp.document
    html.scope          = wp.html
    css.scope           = wp.css
    validation.scope    = wp.css.validation
    computed_values.scope = wp.css.computed_values


    # __init__.py
    wp.technology 					= technology
    wp.HTML._update_tech_params     = _update_tech_params
    wp.HTML._update_device_handlers = _update_device_handlers
    wp.HTML._update_css_properties  = _update_css_properties
    wp.HTML._replace_layer_hook     = _replace_layer_hook
    wp.HTML.write_gds 				= write_gds


    # draw.py
    wp_draw = wp.draw

    # wp_draw.gdspy                       = load_global_module('gdspy')
    wp_draw.draw_page_gds               = draw.draw_page_gds
    wp_draw.draw_stacking_context_gds   = draw.draw_stacking_context_gds
    wp_draw.draw_border_gds             = draw.draw_border_gds
    wp_draw.draw_rounded_border_gds     = draw.draw_rounded_border_gds
    wp_draw.draw_rect_border_gds        = draw.draw_rect_border_gds
    wp_draw.draw_outlines_gds           = draw.draw_outlines_gds
    wp_draw.draw_replacedbox_gds        = draw.draw_replacedbox_gds
    wp_draw.draw_inline_level_gds       = draw.draw_inline_level_gds
    wp_draw.draw_box_background_and_border_gds = \
            draw.draw_box_background_and_border_gds

    # document.py
    wp_doc = wp.document

    # wp_doc.gdspy                        = load_global_module('gdspy')
    doc.draw_page_gds                   = wp_draw.draw_page_gds
    wp_doc.Page.paint_gds               = doc.paint_gds
    wp_doc.Document.write_gds           = doc.write_gds


    # css.py
    # (updated by __init__.py)


    # html.py
    wp_html = wp.html

    wp_html.make_fn                     = html.make_fn
    wp_html.register_device_handlers    = html.register_device_handlers
    wp_html.generate_args 				= html.generate_args
    wp_html.sanitize_attrib 			= html.sanitize_attrib
    wp_html.parse_value 				= html.parse_value





###############################################################################
# for __init__.py
###############################################################################

# wp.HTML.write_gds
def write_gds(self, target=None, stylesheets=None, zoom=1,
              attachments=None, presentational_hints=False):
    """Render the document to a GDS file.

    This is a shortcut for calling :meth:`render`, then
    :meth:`Document.write_gds() <document.Document.write_gds>`.

    :param target:
        A filename, file-like object, or :obj:`None`.
    :param stylesheets:
        An optional list of user stylesheets. (See
        :ref:`stylesheet-origins`\.) The list’s elements are
        :class:`CSS` objects, filenames, URLs, or file-like objects.
    :type zoom: float
    :param zoom:
        This is ignored, for now. Not sure if I'll implement it. Here is
        description from original write_pdf():

        The zoom factor in PDF units per CSS units.
        **Warning**: All CSS units (even physical, like ``cm``)
        are affected.
        For values other than 1, physical CSS units will thus be “wrong”.
        Page size declarations are affected too, even with keyword values
        like ``@page { size: A3 landscape; }``
    :param attachments: A list of additional file attachments for the
        generated GDS document or :obj:`None`. The list's elements are
        :class:`Attachment` objects, filenames, URLs or file-like objects.
    :type presentational_hints: bool
    :param presentational_hints: Whether HTML presentational hints are
        followed.
    :returns:
        GDS library as gdspy.Cell instance.
    """
    
    # Initialize techfile first...
    for elt in self.root_element.iter('tech'):
        technology.init_techfile(elt.values()[0])
        break
    else:
        raise Exception("Please specify a techfile by placing the <tech> "+
            "tag inside <head>")
    self.tech = technology.tech
    
    # Call hooks that update everything we learned about from the techfile
    self._update_tech_params()
    self._update_device_handlers()
    self._update_css_properties()

    # Call builtin hooks
    self._replace_layer_hook(self.root_element, self.tech.Devices.layer_replace)

    # Call user code in <head>
    header_script_sandbox.root_element = self.root_element
    header_script_sandbox.tech         = self.tech
    for elt in self.root_element[0].iter('script'):
        header_script_sandbox.execute(elt.text)



    # Do layout.
    if not stylesheets:
        stylesheets = [self.tech.default_stylesheet]
    else:
        stylesheets.append(self.tech.default_stylesheet)
    
    layout = self.render(stylesheets, presentational_hints).write_gds(
        target, zoom, attachments)



    # Call user code in <body>
    body_script_sandbox.root_element  = self.root_element
    body_script_sandbox.layout        = layout
    body_script_sandbox.tech          = self.tech
    for elt in self.root_element[1].iter('script'):
        body_script_sandbox.execute(elt.text)

    return layout






def _update_tech_params(self):
    # computed_values.LENGTHS_TO_PIXELS
    scope.css.computed_values.LENGTHS_TO_PIXELS = {
        'px': 1,
        'pt': 1. / 0.75,
        'pc': 16.,  # LENGTHS_TO_PIXELS['pt'] * 12
        'in': .0254/ self.tech.precision,
        'cm': 1e-2 / self.tech.precision,
        'mm': 1e-3 / self.tech.precision,
        'nm': 1e-9 / self.tech.precision,
        'um': 1e-6 / self.tech.precision,
        'q' : 1e-3 / self.tech.precision / 4.,  # LENGTHS_TO_PIXELS['mm'] / 4
    }

    # draw.py
    scope.draw.UNITS       = self.tech.units
    scope.draw.PRECISION   = self.tech.precision
    scope.draw.PPU         = self.tech.units / self.tech.precision


    # html.py
    scope.html.UNITS       = self.tech.units
    scope.html.PRECISION   = self.tech.precision
    scope.html.PPU         = self.tech.units / self.tech.precision



    # These files generate globals based on values we just updated,
    # so we need to reload them.
    scope.css.validation = imp.reload(scope.css.validation)





def _update_device_handlers(self):
    scope.html.tech = self.tech
    scope.html.register_device_handlers()





def _update_css_properties(self):
    prop_scope = scope.css.properties
    val_scope  = scope.css.validation
    comp_scope = scope.css.computed_values


    # Define appropriate initial values
    device_builder = scope.html.device_builder
    prop_scope.INITIAL_VALUES.update(device_builder.parameters)

    # Recalculate this from INITIAL_VALUES
    prop_scope.KNOWN_PROPERTIES = set(name.replace('_', '-') \
            for name in prop_scope.INITIAL_VALUES)



    # Update INITIAL_VALUES in computed_values.py
    comp_scope.INITIAL_VALUES = prop_scope.INITIAL_VALUES
    comp_scope.COMPUTING_ORDER = comp_scope._computing_order()


    # Reload 'validation' module to cascade earlier changes.
    scope.css.validation = imp.reload(scope.css.validation)


    # Register properties' methods with validation.py
    # TODO: add expanders
    validation.register_validators(device_builder)


    # Register properties' methods with computed_values.py
    # TODO: investigate what we can do with this
    computed_values.register_computers(device_builder)




def _replace_layer_hook(self, element, replace):
    """Replace any tags matching keys in "replace" with tags in the
    corresponding value.

    Values in "replace" are expected to be tuples. Resulting tags are
    nested in order of tuple, with `replace['key'](0)` as the parent.

    Each new child tag is a copy of the original (with any style, etc.),
    but with layer set to the corresponding Value in "replace"
    """
    def copy_without_children(element):
        new_elt = deepcopy(element)
        for e in new_elt.getchildren():
            new_elt.remove(e)
        return new_elt

    # Replace any child tags first.
    for e in element.getchildren():
        self._replace_layer_hook(e, replace)

    # Replace current tag, if necessary
    if element.tag in replace:
        blank_elt = copy_without_children(element)
        
        new_elt  = deepcopy(blank_elt)
        new_root = new_elt
        parent   = None
        for layer in replace[element.tag]:
            try:
                orig_style = new_elt.attrib['style']
            except KeyError:
                orig_style = ''
            new_elt.attrib['style'] = 'layer:' + layer + ';' + orig_style

            if not parent is None:
                parent.append(new_elt)
            parent = new_elt
            new_elt = deepcopy(blank_elt)

        # Add original children to last element.
        for child in element.getchildren():
            parent.append(child)

        element.getparent().replace(element, new_root)