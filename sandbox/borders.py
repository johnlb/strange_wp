import gdspy
from strange import HTML


HTML('./borders.html').write_gds('./borders.gds')

gdspy.LayoutViewer()