updated: 9/8/16

general
=======
- transfer to separate lib w/ WP as submodule
- build unit tests
- feature buildout

features
========
- library support
    + fix PRECISION/UNITS refs in computed_values.py, draw.py, containers.py, (any more?)
    + add call to techlib's css file
- figure out how to register all the extra properties needed for Devices
    + add layer property instead of using 'color'
    + list of props from techlib?
- add block replacement mechanism (ie pch -> NW + PIMP)
- <script> tag
- dummy device / device matching mechanism
- guard ring generation
- element rotation (using CSS3 transforms? or via object builders?)
- heirarchies
    + Use a tag to include external libraries (ie std cells)
        * <ref src="[path to src]">
        * figure out directory search for ref tags (I think WP has this?)
    + <port layer=M1 name=VIN location=NW??>
        * Need a way to describe location on boundary


wishlist
========
- write library system for gdspy
- add css variables to WeasyPrint?
- <!--[if TSMCN45]> ... some HTML here ... <![endif]-->
    + match with <tech> tag?
- em notation as "relative to min. property dimension"


draw.py
=======
- add layer property to box instead of using 'color'
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
- add precision mgmt