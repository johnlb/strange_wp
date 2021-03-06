updated: 9/8/16

general
=======
- fix 1-px errors in box drawing
- build unit tests
- feature buildout
- make example designs
    + current mirror
    + Yong's cap array
    + opamp
    + DAC

features
========

high-priority
-------------
- autorouting interface
- dummy device / device matching mechanism
- finger mechanism
- guard ring generation
- element rotation
    + How to input? <fet rot=90> I guess?
    + L-R flip needed too... <fet flip=lr> or <fet flip=ud> I guess?
    + CSS3 transform support would be nice, but not primary use case
- add em (as relative to init value) to validators
- figure out what sort of interfaces an autorouter would need
    + How to encode keepout zones?
    + How to encode preferred routing zones?


low-priority
------------
- hooks
    + make separate hook locations?
        * default location + user locations?
        * how to specify user locations - env variable?
    + Should I allow the <head> to talk to the <body>?
- more powerful layer_replace mechanism?
- properties
    + move validators outside of core_cmos.py -- could auto-assign based on init values?
    + other computers?
- finish changeover to monkeypatched architecture
    + do thorough unit tests to be sure we got all the "scope" additions we need.
- heirarchies
    + Use a tag to include external libraries (ie std cells)
        * <ref src="[path to src]">
        * figure out directory search for ref tags (I think WP has this?)
    + <port layer=M1 name=VIN location=NW??>
        * Need a way to describe location on boundary
- <!--[if TSMCN45]> ... some HTML here ... <![endif]-->
    + match with <tech> tag?
- add better cell naming


Auto Routing
============
- via tool
- auto connect overlapping layers on same net
- simple metal extension routing



Architecture
============
- is there a better way to maintain all the validate and compute functions?
    + sep. lib?
- am I doing validation/computing correctly?
- encapsulate netlist creation so implementation details are not needed.
    + need to put it in strange's __init__.py so user libs can import it.
        * any other things this can be used for?


wishlist
========
- fix header parsing bug in html5lib
- write library system for gdspy
- add css variables to WeasyPrint?
- em notation as "relative to min. property dimension"


draw.py
=======
- add text labels
- add better border features (ie guard rings)
- rounded borders?

document.py
===========
- add translation based on x,y coords
- add hinting based on precision?
- clipping?

html.py
=======
- include style in args

containers.py
=============
- add automatic extents calculation
- finish update_extents()

core_cmos.py
============
- can we make parameters dict auto-populate?
- maybe we should make it inherit from a base class?
- move exception checks to validation functions

validation.py
=============
- support different types of tokens?
