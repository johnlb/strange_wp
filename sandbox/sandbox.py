import pdb

import gdspy
from strange import HTML

# pdb.set_trace()
HTML("./script.html").write_gds(None)
# HTML("./test.html").write_gds(None)

# html = HTML('./fets.html')
# body = html.root_element.getchildren()[1]
# fet1 = body.getchildren()[1]



gdspy.LayoutViewer()