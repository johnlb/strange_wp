# coding: utf-8
"""
    strange.weasyprint_patches.body_script_sandbox
    -------------------

    A simple sandbox for any user code to run in.

    This is not meant to be particularly secure (to some degree,
    user code can never be terribly secure in Python), but instead
    it is meant to provide a user namespace that won't pollute
    other namespaces.
"""



from textwrap import dedent


root_element = None     # Monkeypatched by HTML.write_gds()
layout       = None     # Monkeypatched by HTML.write_gds()
tech         = None 	# Monkeypatched by HTML.write_gds()


def execute(user_code):

	# First, remove initial indent level.
	user_code = dedent(user_code)

	# Now, run the code!
	exec(user_code)