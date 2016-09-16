import pdb

import gdspy
from strange import HTML

# pdb.set_trace()
# HTML('./borders.html').write_gds(None)
HTML("./fets.html").write_gds(None)
# pdb.run('HTML("./fets.html").write_gds(None)')

# html = HTML('./fets.html')
# body = html.root_element.getchildren()[1]
# fet1 = body.getchildren()[1]



gdspy.LayoutViewer()