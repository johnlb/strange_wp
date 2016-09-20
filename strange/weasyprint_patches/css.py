# coding: utf-8
"""
    strange.weasyprint_patches.css
    -------------------

    patches for weasyprint.css

"""
import imp
import os
# scope = 'scope'

# This one's tricky, b/c we don't know what 'precision'	or 'units'
# should be until we parse the html file (and thus, the techfile).
#
# So, we're creating a hook that can be called to do the patching
# once we have the data.

directory = [os.path.dirname(__file__)]
patching = imp.load_module('patching', *imp.find_module('patching',directory))

# We have to define these in-package
scope = None


# def create_hook(scope,wp):
# @patching.append_scope
def update_tech_params(self,tech):
	# computed_values.LENGTHS_TO_PIXELS
	wp.css.computed_values.LENGTHS_TO_PIXELS = {
	    'px': 1,
	    'pt': 1. / 0.75,
	    'pc': 16.,  # LENGTHS_TO_PIXELS['pt'] * 12
	    'in': .0254/ tech.precision,
	    'cm': 1e-2 / tech.precision,
	    'mm': 1e-3 / tech.precision,
	    'nm': 1e-9 / tech.precision,
	    'um': 1e-6 / tech.precision,
	    'q': 96. / 25.4 / 4.,  # LENGTHS_TO_PIXELS['mm'] / 4
	}

	# draw.py
	wp.draw.UNITS 		= tech.units
	wp.draw.PRECISION 	= tech.precision
	wp.draw.PPU 		= tech.units / tech.precision


	# containers.py


	# html.py
	wp.html.UNITS 		= tech.units
	wp.html.PRECISION 	= tech.precision
	wp.html.PPU 		= tech.units / tech.precision



	# These files generate globals based on updated values,
	# so we need to reload them.
	wp.css.validation = imp.reload(wp.css.validation)

# return update_tech_params