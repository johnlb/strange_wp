import pdb

import gdspy
from strange import HTML

# pdb.set_trace()
HTML("./imirror.html").write_gds(None)


gdspy.LayoutViewer()