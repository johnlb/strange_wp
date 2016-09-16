updated: 9/8/16

general
=======
- build unit tests
- add content handling (layout module)
- add pcell library interface (html.py)
- feature buildout
- write library system for gdspy
- why does inline border give wrong size?

features
========
- library support
- add block replacement mechanism (ie pch -> NW + PIMP)
- add important tags to default stylesheet
- add css variables to WeasyPrint?
- Use a tag to include external libraries (ie std cells)
    + <ref src="[path to src]">
- <!--[if TSMCN45]> ... some HTML here ... <![endif]-->
- <script> tag
- <port layer=M1 name=VIN location=NW??>
    + Need a way to describe location on boundary


draw.py
=======
- add layer property to box instead of using 'color'
- good way to manage precision

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