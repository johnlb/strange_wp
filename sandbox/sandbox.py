import gdspy
from strange import HTML


HTML('./simple.html').write_gds('./simple.gds')

gdspy.LayoutViewer()