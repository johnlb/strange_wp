
# coding: utf-8
"""
    weasyprint.html
    ---------------

    Specific handling for some HTML elements, especially replaced elements.

    Replaced elements (eg. <img> elements) are rendered externally and
    behave as an atomic opaque box in CSS. In general, they may or may not
    have intrinsic dimensions. But the only replaced elements currently
    supported in WeasyPrint are images with intrinsic dimensions.

    Adding support for gdspy geometery objects to be used as content.

    :copyright: Copyright 2011-2014 Simon Sapin and contributors, see AUTHORS.
    :license: BSD, see LICENSE for details.

"""

from __future__ import division, unicode_literals
import os.path
import logging
import sys
import re

from .css import get_child_text
from .formatting_structure import boxes
from .urls import get_url_attribute
from .compat import xrange, urljoin
from .logger import LOGGER
from . import CSS

import inspect
import gdspy
from techlibs.containers import geometryContainer
# from .technology import tech
import tinycss



# XXX temporarily disable logging for user-agent stylesheet
level = LOGGER.level
LOGGER.setLevel(logging.ERROR)

if hasattr(sys, "frozen"):
    root = os.path.dirname(sys.executable)
else:
    root = os.path.dirname(__file__)
HTML5_UA_STYLESHEET = CSS(filename=os.path.join(root, 'css', 'html5_ua.css'))
HTML5_PH_STYLESHEET = CSS(filename=os.path.join(root, 'css', 'html5_ph.css'))

LOGGER.setLevel(level)


# http://whatwg.org/C#space-character
HTML_WHITESPACE = ' \t\n\f\r'
HTML_SPACE_SEPARATED_TOKENS_RE = re.compile('[^%s]+' % HTML_WHITESPACE)


def ascii_lower(string):
    r"""Transform (only) ASCII letters to lower case: A-Z is mapped to a-z.

    :param string: An Unicode string.
    :returns: A new Unicode string.

    This is used for `ASCII case-insensitive
    <http://whatwg.org/C#ascii-case-insensitive>`_ matching.

    This is different from the :meth:`~py:str.lower` method of Unicode strings
    which also affect non-ASCII characters,
    sometimes mapping them into the ASCII range:

    >>> keyword = u'Bac\N{KELVIN SIGN}ground'
    >>> assert keyword.lower() == u'background'
    >>> assert ascii_lower(keyword) != keyword.lower()
    >>> assert ascii_lower(keyword) == u'bac\N{KELVIN SIGN}ground'

    """
    # This turns out to be faster than unicode.translate()
    return string.encode('utf8').lower().decode('utf8')


def element_has_link_type(element, link_type):
    """
    Return whether the given element has a ``rel`` attribute with the
    given link type.

    :param link_type: Must be a lower-case string.

    """
    return any(ascii_lower(token) == link_type for token in
               HTML_SPACE_SEPARATED_TOKENS_RE.findall(element.get('rel', '')))


# Maps HTML tag names to function taking an HTML element and returning a Box.
HTML_HANDLERS = {}


def handle_element(element, box, get_image_from_uri):
    """Handle HTML elements that need special care.

    :returns: a (possibly empty) list of boxes.
    """
    if box.element_tag in HTML_HANDLERS:
        return HTML_HANDLERS[element.tag](element, box, get_image_from_uri)
    else:
        return [box]


def handler(tag):
    """Return a decorator registering a function handling ``tag`` elements."""
    def decorator(function):
        """Decorator registering a function handling ``tag`` elements."""
        HTML_HANDLERS[tag] = function
        return function
    return decorator


def make_replaced_box(element, box, image):
    """Wrap an image in a replaced box.

    That box is either block-level or inline-level, depending on what the
    element should be.

    """
    if box.style.display in ('block', 'list-item', 'table'):
        type_ = boxes.BlockReplacedBox
    else:
        # TODO: support images with 'display: table-cell'?
        type_ = boxes.InlineReplacedBox
    return type_(element.tag, element.sourceline, box.style, image)


@handler('img')
def handle_img(element, box, get_image_from_uri):
    """Handle ``<img>`` elements, return either an image or the alt-text.

    See: http://www.w3.org/TR/html5/embedded-content-1.html#the-img-element

    """
    src = get_url_attribute(element, 'src')
    alt = element.get('alt')
    if src:
        image = get_image_from_uri(src)
        if image is not None:
            return [make_replaced_box(element, box, image)]
        else:
            # Invalid image, use the alt-text.
            if alt:
                return [box.copy_with_children(
                    [boxes.TextBox.anonymous_from(box, alt)])]
            elif alt == '':
                # The element represents nothing
                return []
            else:
                assert alt is None
                # TODO: find some indicator that an image is missing.
                # For now, just remove the image.
                return []
    else:
        if alt:
            return [box.copy_with_children(
                [boxes.TextBox.anonymous_from(box, alt)])]
        else:
            return []


@handler('embed')
def handle_embed(element, box, get_image_from_uri):
    """Handle ``<embed>`` elements, return either an image or nothing.

    See: https://www.w3.org/TR/html5/embedded-content-0.html#the-embed-element

    """
    src = get_url_attribute(element, 'src')
    type_ = element.get('type', '').strip()
    if src:
        image = get_image_from_uri(src, type_)
        if image is not None:
            return [make_replaced_box(element, box, image)]
    # No fallback.
    return []


@handler('object')
def handle_object(element, box, get_image_from_uri):
    """Handle ``<object>`` elements, return either an image or the fallback
    content.

    See: https://www.w3.org/TR/html5/embedded-content-0.html#the-object-element

    """
    data = get_url_attribute(element, 'data')
    type_ = element.get('type', '').strip()
    if data:
        image = get_image_from_uri(data, type_)
        if image is not None:
            return [make_replaced_box(element, box, image)]
    # The element’s children are the fallback.
    return [box]


#####################################################
# GDS Stuff.
#####################################################

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
            return [make_replaced_box(element, box, geometries)]
        except AttributeError:
            # The element’s children are the fallback.
            return [box]

    return handle_device


def register_device_handlers():
    device_handlers = []
    for member in inspect.getmembers(tech.Devices):
        if inspect.ismethod(member[1]):
            # can't use @decorator for dynamic functions :-/
            decorator = handler(member[0])
            device_handlers.append(decorator(make_fn(member[1])))


def generate_args(attributes, style):
    args = attributes
    # TODO: include style
    print('--------')
    print(attributes)
    # print((style.rxextleft))
    # print((style.rxextleft))
    return args


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

    # TODO: link precision/units to techfile
    # precision = tech.PRECISION
    # units = tech.UNITS
    precision = 5e-9
    units = 1e-6
    unitsSI = {
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
            return value.value * (precision/units)
        else:
            return value.value * unitsSI[value.unit[0]]/units



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


#####################################################


def integer_attribute(element, box, name, minimum=1):
    """Read an integer attribute from the HTML element and set it on the box.

    """
    value = element.get(name, '').strip()
    if value:
        try:
            value = int(value)
        except ValueError:
            pass
        else:
            if value >= minimum:
                setattr(box, name, value)


@handler('colgroup')
def handle_colgroup(element, box, _get_image_from_uri):
    """Handle the ``span`` attribute."""
    if isinstance(box, boxes.TableColumnGroupBox):
        if any(child.tag == 'col' for child in element):
            box.span = None  # sum of the children’s spans
        else:
            integer_attribute(element, box, 'span')
            box.children = (
                boxes.TableColumnBox.anonymous_from(box, [])
                for _i in xrange(box.span))
    return [box]




@handler('col')
def handle_col(element, box, _get_image_from_uri):
    """Handle the ``span`` attribute."""
    if isinstance(box, boxes.TableColumnBox):
        integer_attribute(element, box, 'span')
        if box.span > 1:
            # Generate multiple boxes
            # http://lists.w3.org/Archives/Public/www-style/2011Nov/0293.html
            return [box.copy() for _i in xrange(box.span)]
    return [box]


@handler('th')
@handler('td')
def handle_td(element, box, _get_image_from_uri):
    """Handle the ``colspan``, ``rowspan`` attributes."""
    if isinstance(box, boxes.TableCellBox):
        # HTML 4.01 gives special meaning to colspan=0
        # http://www.w3.org/TR/html401/struct/tables.html#adef-rowspan
        # but HTML 5 removed it
        # http://www.w3.org/TR/html5/tabular-data.html#attr-tdth-colspan
        # rowspan=0 is still there though.
        integer_attribute(element, box, 'colspan')
        integer_attribute(element, box, 'rowspan', minimum=0)
    return [box]


@handler('a')
def handle_a(element, box, _get_image_from_uri):
    """Handle the ``rel`` attribute."""
    box.is_attachment = element_has_link_type(element, 'attachment')
    return [box]


def find_base_url(html_document, fallback_base_url):
    """Return the base URL for the document.

    See http://www.w3.org/TR/html5/urls.html#document-base-url

    """
    first_base_element = next(iter(html_document.iter('base')), None)
    if first_base_element is not None:
        href = first_base_element.get('href', '').strip()
        if href:
            return urljoin(fallback_base_url, href)
    return fallback_base_url


def get_html_metadata(html_document):
    """
    Relevant specs:

    http://www.whatwg.org/html#the-title-element
    http://www.whatwg.org/html#standard-metadata-names
    http://wiki.whatwg.org/wiki/MetaExtensions
    http://microformats.org/wiki/existing-rel-values#HTML5_link_type_extensions

    """
    title = None
    description = None
    generator = None
    keywords = []
    authors = []
    created = None
    modified = None
    attachments = []
    for element in html_document.iter('title', 'meta', 'link'):
        if element.tag == 'title' and title is None:
            title = get_child_text(element)
        elif element.tag == 'meta':
            name = ascii_lower(element.get('name', ''))
            content = element.get('content', '')
            if name == 'keywords':
                for keyword in map(strip_whitespace, content.split(',')):
                    if keyword not in keywords:
                        keywords.append(keyword)
            elif name == 'author':
                authors.append(content)
            elif name == 'description' and description is None:
                description = content
            elif name == 'generator' and generator is None:
                generator = content
            elif name == 'dcterms.created' and created is None:
                created = parse_w3c_date(name, element.sourceline, content)
            elif name == 'dcterms.modified' and modified is None:
                modified = parse_w3c_date(name, element.sourceline, content)
        elif element.tag == 'link' and element_has_link_type(
                element, 'attachment'):
            url = get_url_attribute(element, 'href')
            title = element.get('title', None)
            if url is None:
                LOGGER.warning('Missing href in <link rel="attachment">')
            else:
                attachments.append((url, title))
    return dict(title=title, description=description, generator=generator,
                keywords=keywords, authors=authors,
                created=created, modified=modified,
                attachments=attachments)


def strip_whitespace(string):
    """Use the HTML definition of "space character",
    not all Unicode Whitespace.

    http://www.whatwg.org/html#strip-leading-and-trailing-whitespace
    http://www.whatwg.org/html#space-character

    """
    return string.strip(' \t\n\f\r')


# YYYY (eg 1997)
# YYYY-MM (eg 1997-07)
# YYYY-MM-DD (eg 1997-07-16)
# YYYY-MM-DDThh:mmTZD (eg 1997-07-16T19:20+01:00)
# YYYY-MM-DDThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00)
# YYYY-MM-DDThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00)

W3C_DATE_RE = re.compile('''
    ^
    [ \t\n\f\r]*
    (?P<year>\d\d\d\d)
    (?:
        -(?P<month>0\d|1[012])
        (?:
            -(?P<day>[012]\d|3[01])
            (?:
                T(?P<hour>[01]\d|2[0-3])
                :(?P<minute>[0-5]\d)
                (?:
                    :(?P<second>[0-5]\d)
                    (?:\.\d+)?  # Second fraction, ignored
                )?
                (?:
                    Z |  # UTC
                    (?P<tz_hour>[+-](?:[01]\d|2[0-3]))
                    :(?P<tz_minute>[0-5]\d)
                )
            )?
        )?
    )?
    [ \t\n\f\r]*
    $
''', re.VERBOSE)


def parse_w3c_date(meta_name, source_line, string):
    """http://www.w3.org/TR/NOTE-datetime"""
    if W3C_DATE_RE.match(string):
        return string
    else:
        LOGGER.warning('Invalid date in <meta name="%s"> line %i: %r',
                       meta_name, source_line, string)
