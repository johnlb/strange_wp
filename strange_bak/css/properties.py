# coding: utf-8
"""
    weasyprint.css.properties
    -------------------------

    Various data about known properties.

    :copyright: Copyright 2011-2014 Simon Sapin and contributors, see AUTHORS.
    :license: BSD, see LICENSE for details.

"""

from __future__ import division, unicode_literals
import collections

from tinycss.color3 import COLOR_KEYWORDS


Dimension = collections.namedtuple('Dimension', ['value', 'unit'])


# See http://www.w3.org/TR/CSS21/propidx.html
INITIAL_VALUES = {
    'bottom': 'auto',
    'caption_side': 'top',
    'clear': 'none',
    'clip': (),  # computed value for 'auto'
    'color': COLOR_KEYWORDS['black'],  # chosen by the user agent
    'content': 'normal',
    # Means 'none', but allow `display: list-item` to increment the
    # list-item counter. If we ever have a way for authors to query
    # computed values (JavaScript?), this value should serialize to 'none'.
    'counter_increment': 'auto',
    'counter_reset': [],  # parsed value for 'none'
    # 'counter_set': [],  # parsed value for 'none'
    'direction': 'ltr',
    'display': 'inline',
    'empty_cells': 'show',
    'float': 'none',
    'height': 'auto',
    'left': 'auto',
    'line_height': 'normal',
    'list_style_image': ('none', None),
    'list_style_position': 'outside',
    'list_style_type': 'disc',
    'margin_top': Dimension(0, 'px'),
    'margin_right': Dimension(0, 'px'),
    'margin_bottom': Dimension(0, 'px'),
    'margin_left': Dimension(0, 'px'),
    'max_height': Dimension(float('inf'), 'px'),  # parsed value for 'none'
    'max_width': Dimension(float('inf'), 'px'),
    'min_height': Dimension(0, 'px'),
    'min_width': Dimension(0, 'px'),
    'overflow': 'visible',
    'padding_top': Dimension(0, 'px'),
    'padding_right': Dimension(0, 'px'),
    'padding_bottom': Dimension(0, 'px'),
    'padding_left': Dimension(0, 'px'),
    'quotes': list('“”‘’'),  # chosen by the user agent
    'position': 'static',
    'right': 'auto',
    'table_layout': 'auto',
    'text_decoration': 'none',
    'top': 'auto',
    'unicode_bidi': 'normal',
    'vertical_align': 'baseline',
    'visibility': 'visible',
    'width': 'auto',
    'z_index': 'auto',

    # Backgrounds and Borders 3: https://www.w3.org/TR/css3-background/
    'background_attachment': ['scroll'],
    'background_clip': ['border-box'],
    'background_color': COLOR_KEYWORDS['transparent'],
    'background_image': [('none', None)],
    'background_origin': ['padding-box'],
    'background_position': [('left', Dimension(0, '%'),
                             'top', Dimension(0, '%'))],
    'background_repeat': [('repeat', 'repeat')],
    'background_size': [('auto', 'auto')],
    'border_bottom_color': 'currentColor',
    'border_bottom_left_radius': (Dimension(0, 'px'), Dimension(0, 'px')),
    'border_bottom_right_radius': (Dimension(0, 'px'), Dimension(0, 'px')),
    'border_bottom_style': 'none',
    'border_bottom_width': 3,
    'border_collapse': 'separate',
    'border_left_color': 'currentColor',
    'border_left_style': 'none',
    'border_left_width': 3,
    'border_right_color': 'currentColor',
    'border_right_style': 'none',
    'border_right_width': 3,
    'border_spacing': (0, 0),
    'border_top_color': 'currentColor',
    'border_top_left_radius': (Dimension(0, 'px'), Dimension(0, 'px')),
    'border_top_right_radius': (Dimension(0, 'px'), Dimension(0, 'px')),
    'border_top_style': 'none',
    'border_top_width': 3,  # computed value for 'medium'

    # Color 3: https://www.w3.org/TR/css3-color/
    'opacity': 1,

    # Multi-column Layout: https://www.w3.org/TR/css3-multicol/
    'column_width': 'auto',
    'column_count': 'auto',
    'column_gap': Dimension(1, 'em'),
    'column_rule_color': 'currentColor',
    'column_rule_style': 'none',
    'column_rule_width': 'medium',
    'column_fill': 'balance',
    'column_span': 'none',

    # Fonts 3: https://www.w3.org/TR/css-fonts-3/
    'font_family': ['serif'],  # depends on user agent
    'font_size': 16,  # actually medium, but we define medium from this
    'font_stretch': 'normal',
    'font_style': 'normal',
    'font_variant': 'normal',
    'font_weight': 400,

    # Fragmentation 3: https://www.w3.org/TR/css-break-3/
    'break_after': 'auto',
    'break_before': 'auto',
    'break_inside': 'auto',
    'orphans': 2,
    'widows': 2,

    # Generated Content for Paged Media: https://www.w3.org/TR/css-gcpm-3/
    'bookmark_label': [('content', 'text')],
    'bookmark_level': 'none',
    'string_set': 'none',

    # Images 3/4: https://www.w3.org/TR/css4-images/
    'image_resolution': 1,  # dppx
    'image_rendering': 'auto',

    # Paged Media 3: https://www.w3.org/TR/css3-page/
    'size': None,  # XXX set to A4 in computed_values

    # Text 3/4: https://www.w3.org/TR/css-text-4/
    'hyphenate_character': '‐',  # computed value chosen by the user agent
    'hyphenate_limit_chars': (5, 2, 2),
    'hyphenate_limit_zone': Dimension(0, 'px'),
    'hyphens': 'manual',
    'letter_spacing': 'normal',
    'tab_size': 8,
    'text_align': '-weasy-start',
    'text_indent': Dimension(0, 'px'),
    'text_transform': 'none',
    'white_space': 'normal',
    'word_spacing': 0,  # computed value for 'normal'

    # Transforms 1: https://www.w3.org/TR/css-transforms-1/
    'transform_origin': (Dimension(50, '%'), Dimension(50, '%')),
    'transform': (),  # computed value for 'none'

    # User Interface 3: https://www.w3.org/TR/css-ui-3/
    'box_sizing': 'content-box',
    'outline_color': 'currentColor',  # invert is not supported
    'outline_style': 'none',
    'outline_width': 3,  # computed value for 'medium'
    'overflow_wrap': 'normal',

    # Proprietary
    'anchor': None,  # computed value of 'none'
    'link': None,  # computed value of 'none'
    'lang': None,  # computed value of 'none'

    # Internal, to implement the "static position" for absolute boxes.
    '_weasy_specified_display': 'inline',
}


KNOWN_PROPERTIES = set(name.replace('_', '-') for name in INITIAL_VALUES)

# Not applicable to the print media
NOT_PRINT_MEDIA = set([
    # Aural media:
    'azimuth',
    'cue',
    'cue-after',
    'cue-before',
    'cursor',
    'elevation',
    'pause',
    'pause-after',
    'pause-before',
    'pitch-range',
    'pitch',
    'play-during',
    'richness',
    'speak-header',
    'speak-numeral',
    'speak-punctuation',
    'speak',
    'speech-rate',
    'stress',
    'voice-family',
    'volume',

    # outlines are not just for interactive but any visual media in css3-ui
])


# Do not list shorthand properties here as we handle them before inheritance.
#
# text_decoration is not a really inherited, see
# http://www.w3.org/TR/CSS2/text.html#propdef-text-decoration
#
# link: click events normally bubble up to link ancestors
#   See http://lists.w3.org/Archives/Public/www-style/2012Jun/0315.html
INHERITED = set("""
    border_collapse
    border_spacing
    caption_side
    color
    direction
    empty_cells
    font_family
    font_size
    font_style
    font_stretch
    font_variant
    font_weight
    hyphens
    hyphenate_character
    hyphenate_limit_chars
    hyphenate_limit_zone
    image_rendering
    image_resolution
    lang
    letter_spacing
    line_height
    link
    list_style_image
    list_style_position
    list_style_type
    orphans
    overflow_wrap
    quotes
    tab_size
    text_align
    text_decoration
    text_indent
    text_transform
    visibility
    white_space
    widows
    word_spacing
""".split())

# Inherited but not applicable to print:
#    azimuth
#    cursor
#    elevation
#    pitch_range
#    pitch
#    richness
#    speak_header
#    speak_numeral
#    speak_punctuation
#    speak
#    speech_rate
#    stress
#    voice_family
#    volume


# http://www.w3.org/TR/CSS21/tables.html#model
# See also http://lists.w3.org/Archives/Public/www-style/2012Jun/0066.html
# Only non-inherited properties need to be included here.
TABLE_WRAPPER_BOX_PROPERTIES = set('''
    bottom
    break_after
    break_before
    break_inside
    clear
    counter_increment
    counter_reset
    float
    left
    margin_top
    margin_bottom
    margin_left
    margin_right
    opacity
    position
    right
    top
    transform
    transform_origin
    vertical_align
    z_index
'''.split())
