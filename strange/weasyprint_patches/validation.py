# coding: utf-8
"""
    strange.weasyprint_patches.validation
    -------------------

    patches for weasyprint.validation

"""

def make_fn(fn_to_use):
    """Return a new version of handle_device using fn_to_use."""
    def handle_device(element, box, style):
        """Handle appropriate element, return a geometryContainer with 
        the content.

        Treated similar to ``object`` element.
        """
        elt_attrib = sanitize_attrib(element.attrib) 
        kwargs = generate_args(elt_attrib, box.style)
        # if 'fet' in lib:
        try:
            geometries = fn_to_use(**kwargs)
            return [scope.make_replaced_box(element, box, geometries)]
        except AttributeError:
            # The element’s children are the fallback.
            return [box]

    return handle_device


def register_validators(device_builder):

    # TODO: support 'layer' property
    # some standard properties to add-on

    validator_dict = device_builder.validators
    # add builtins
    validator_dict['net'] = _validate_net

    validators = []
    for name, func in validator_dict.items():
        name = name.replace('_', '-')
        # can't use @decorator for dynamic functions :-/
        decorator = scope.validator(name)
        validators.append(decorator((func)))



def _validate_net(token):
    token = token[0]
    if token.type=="STRING" or token.type=="IDENT":
        try:
            return str(token)
        except:
            pass 