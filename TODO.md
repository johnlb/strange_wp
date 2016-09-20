updated: 9/8/16

general
=======
- build unit tests
- feature buildout

features
========
- figure out how to register all the extra properties needed for Devices
    + add layer property instead of using 'color'
    + list of props from techlib?
- add block replacement mechanism (ie pch -> NW + PIMP)
- <script> tag
- dummy device / device matching mechanism
- guard ring generation
- element rotation
    + How to input? <fet rot=90> I guess?
    + L-R flip needed too... <fet flip=lr> or <fet flip=ud> I guess?
    + CSS3 transform support would be nice, but not primary use case
- finish changeover to monkeypatched architecture
    + do thorough unit tests to be sure we got all the "scope" additions we need.
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