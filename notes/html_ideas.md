Using HTML DOM. This opens us up for some broken-HTML-type drawbacks, but I would rather have that than the overly-strict XML style (eg all parameters in quotes, empty tags closed, etc.)


## <head>
- <!DOCTYPE netlist>
- <meta> -- Can put metadata about design in header
- Use a tag to include external libraries (ie std cells)
    + <ref src="[path to src]">
    + similar to <img>
- Default char encoding = UTF-8 (don't require encoding tag)


## How does technology support work?
- $TECHPATH defualts to the tech dir in install, but is overridden by env var.
- Multiple dir search would be nice?

### Dir structure
- $TECHPATH/
    + TSMCN45/
        * __init__.css
            - defines minimums/defualts
        * TSMCN45.py
            - defines layer replacements (pch -> NW+PIMP)
            - defines layer assignments
            - defines PRECISION & UNITS
    + IBM180/
        * (same as above)
    + CORE_CMOS/
        * __init__.py
            - basic device definitions
            - referenced library, not technology definition itself

### Invocation
Inside <head>:
- <tech value="tech_name">
- "tech_name" matches name of folder in $TECHPATH

### Usage
- objects in tech_name.py can be imported from anywhere in code via "technology.py" (this is module that handles external import)
    + html.py uses technology.py to register all the tags tech_name.py needs to register
    + 
- tech_name.py can reference other device libraries (ie a "core" device lib) and/or add its own custom devices
- tech_name.css gets cascaded with current ua.css (maybe via same external stylesheet import in HTML() call? -- need to figure this out)



## Styles
- Inline -- not high priority, but possible
- <link rel="stylesheet" href="styles_analog.css">


## Tags
- <!-- This is a comment -->
- <!--[if TSMCN45]> ... some HTML here ... <![endif]-->
- <[primitive name] [attributes]> i/o connections </[primitive name]>
    + ex: <fet w=1u l=40n id=M1@1 class=ana> g=n1 d=n1 s=vss b=vss </fet>
    + all primitives default to a class called "minsize"
- cell-wide styles could exist in <body> tag?
- <port layer=M1 name=VIN location=NW??>
    + Need a way to describe location on boundary
- use <div></div> to define large blocks
    + Wells, IMP layers, guard rings, etc.
    + Use border property to define the layer / structure
- use empty tags inside primitive tag to define i/o connections
    + <io vdd=vdd vss=vss> for inouts
    + <i vin=net1> for inputs
    + <o vout=net2> for outputs
    + This is nice because
        a. don't need extra parser
        b. allows for port direction declarations -- helpful with auto import?
        c. forces explicit port:net pairing -- better readability


## <script></script>
- native-run python
- need to expose internal namespace via "document" object 
    + getElementById(), etc.
- 


## Responsive Design
- Should be able to make styles that work well even if cell boundary is resized / content is changed around
- 