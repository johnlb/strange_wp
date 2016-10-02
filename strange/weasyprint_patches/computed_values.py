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
    computer_dict = device_builder.computers
    # add builtins
    computer_dict['net'] = _compute_net


    computers = []
    for name, func in computer_dict.items():
        name = name.replace('_', '-')
        # can't use @decorator for dynamic functions :-/
        decorator = scope.register_computer(name)
        computers.append(decorator((func)))


def _compute_net(computer, name, value):
    return value