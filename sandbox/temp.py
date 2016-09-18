import strange as wp
import gdspy
import imp

precision = 5e-9
# print(wp.css.computed_values)

wp.css.computed_values.LENGTHS_TO_PIXELS = {
    'px': 1,
    'pt': 1. / 0.75,
    'pc': 16.,  # LENGTHS_TO_PIXELS['pt'] * 12
    'in': .0254/ precision,
    'cm': 1e-2 / precision,
    'mm': 1e-3 / precision,
    'nm': 1e-9 / precision,
    'um': 1e-6 / precision,
    'q': 96. / 25.4 / 4.,  # LENGTHS_TO_PIXELS['mm'] / 4
}
wp.css.computed_values.NEW_VAR = 2
wp.css.validation = imp.reload(wp.css.validation)

wp.HTML("./fets.html").write_gds(None)

gdspy.LayoutViewer()