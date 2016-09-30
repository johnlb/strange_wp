# coding: utf-8
"""
    strange.weasyprint_patches.header_script_sandbox
    -------------------

    A simple sandbox for any user code to run in.

    This is not meant to be particularly secure (to some degree,
    user code can never be terribly secure in Python), but instead
    it is meant to provide a user namespace that won't pollute
    other namespaces.
"""


root_element = None 	#