# coding: utf-8
"""
    strange.weasyprint_patches.html
    -------------------

    patches for weasyprint.html

"""
import inspect
import gdspy
import tinycss

tech = None

###############################################################################
# This is for __init__.py
###############################################################################

def create_hook(wp):
    @staticmethod
    def update_device_handlers(tech_):
        global tech
        tech = tech_
        wp.html.register_device_handlers()

    return update_device_handlers



###############################################################################
# The rest go into html.py
###############################################################################


def make_fn(fn_to_use):
    """Return a new version of handle_device using fn_to_use."""
    def handle_device(element, box, get_image_from_uri):
        """Handle appropriate element, return a geometryContainer with 
        the content.

        Treated similar to ``object`` element.
        """
        io = element.find('io').attrib
        elt_attrib = sanitize_attrib(element.attrib)
        try:
            elt_attrib.update(io)
        except AttributeError:
            pass
        kwargs = generate_args(elt_attrib, box.style)
        
        try:
            geometries = fn_to_use(**kwargs)
            return [scope.make_replaced_box(element, box, geometries)]
        except AttributeError:
            # The element’s children are the fallback.
            return [box]

    return handle_device


def register_device_handlers():
    scope.device_builder = scope.tech.Devices(scope.tech)
    device_handlers = []
    for member in inspect.getmembers(scope.device_builder):
        if member[0] in ['__init__']:
            continue
        if inspect.ismethod(member[1]):
            # can't use @decorator for dynamic functions :-/
            decorator = scope.handler(member[0])
            device_handlers.append(decorator(make_fn(member[1])))


def generate_args(attributes, style):
    args = attributes
    args.update( make_style_dict(style) )
    return args

def make_style_dict(style):
    properties = scope.device_builder.parameters.keys()
    style['margin_bottom']
    style_dict = {}
    for prop in properties:
        style_dict[prop] = style[prop]
    return style_dict



def sanitize_attrib(attributes):
    """
    Sanitizes raw attributes dictionary from lxml.
    
    - Numeric values are parsed in the same way
      CSS declarations are parsed.

    Parameters
    ----------
    attributes : dictionary
        Dictionary of attributes, direct from lxml

    Modifies
    --------
    attributes

    Returns
    -------
    out : dictionary
        same dictionary, sanitized.
    """
    attributes = dict(attributes)
    for key in attributes.keys():
        if key in ['id', 'class', 'style']:
            continue
        thisToken = tinycss.tokenizer.tokenize_flat(attributes[key])[0]
        attributes[key] = parse_value(thisToken)

    return attributes



def parse_value(value):
    """
    Converts tinycss Token into appropriate Pythonic value

    Parameters
    ----------
    value : tinycss Token
        value being assigned to a property

    Returns
    -------
    out : string | boolean | float (depending on Token's value)
        Appropriate Pythonic datatype, with unit conversion.
        Percentages are returned as strings of the form: "90%"
        (since this function cannot know about the value's default)
    """

    # Note: both 'PRECISION' & 'UNITS' are defined in HTML.write_gds
    #       after the techfile has been parsed.
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



    if value.type == 'DIMENSION':
        if value.unit == 'px':
            return value.value * (scope.tech.precision/scope.tech.units)
        else:
            return value.value * units_si[value.unit[0]]/scope.tech.units



    elif value.type == 'INTEGER' or value.type == 'NUMBER':
        return value.value



    elif value.type == 'PERCENTAGE':
        return str(value.value) + '%'



    elif value.type == 'STRING':
        if value.value.lower() == 'true':
            return True
        elif value.value.lower() == 'false':
            return False
        else:
            return value.value



    elif value.type == 'IDENT':
        if value.value.lower() == 'true':
            return True
        elif value.value.lower() == 'false':
            return False
        else:
            return value.value



    else:
        raise Warning("Illegal value (" + str(value.value) + 
                        ") in css at line " + str(value.line) +
                        ", column " + str(value.column) )


