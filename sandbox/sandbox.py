import gdspy
from strange import HTML


# HTML('./borders.html').write_gds('-')
HTML('./fets.html').write_gds('-')

# html = HTML('./fets.html')
# body = html.root_element.getchildren()[1]
# fet1 = body.getchildren()[1]



# gdspy.LayoutViewer()