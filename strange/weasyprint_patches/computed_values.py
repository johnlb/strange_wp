# coding: utf-8
"""
    strange.weasyprint_patches.computed_values
    -------------------

    patches for weasyprint.computed_values

"""

scope = None # gets set by patch() in weasyprint_patch


def register_computers(device_builder):

    # TODO: support 'layer' property
    # some standard properties to add-on
    # properties_gds = {
    #     'layer'     : ''
    # }


    computers = []
    for name, func in device_builder.computers.items():
        name = name.replace('_', '-')
        # can't use @decorator for dynamic functions :-/
        # decorator = scope.single_token(scope.validator(name))
        decorator = scope.register_computer(name)
        computers.append(decorator((func)))


