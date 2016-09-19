# coding: utf-8
"""
    strange.weasyprint_patches.document
    -------------------

    patches for weasyprint.document

"""

# Page.paint_gds
def paint_gds(self, cell, left_x=0, top_y=0, scale=1, clip=False):
    """Paint the page in gdspy.

    :param cell:
        Any :class:`gdspy.Cell` object.
    :param left_x:
        X coordinate of the left of the page, in gdspy user units.
    :param top_y:
        Y coordinate of the top of the page, in gdspy user units.
    :param scale:
        Ignored. Here is the orig. description:
        Zoom scale in cairo user units per CSS pixel.
    :param clip:
        Whether to clip/cut content outside the page. If false or
        not provided, content can overflow.
    :type left_x: float
    :type top_y: float
    :type scale: float
    :type clip: bool

    """
    # TO DO: add translation based on x,y coords
    # TO DO: add hinting based on precision?
    # TO DO: add clipping?
    draw_page_gds(self._page_box, cell, self._enable_hinting)

    # with stacked(cairo_context):
    #     if self._enable_hinting:
    #         left_x, top_y = cairo_context.user_to_device(left_x, top_y)
    #         # Hint in device space
    #         left_x = int(left_x)
    #         top_y = int(top_y)
    #         left_x, top_y = cairo_context.device_to_user(left_x, top_y)

    #     # Make (0, 0) the top-left corner:
    #     cairo_context.translate(left_x, top_y)
    #     # Make user units CSS pixels:
    #     cairo_context.scale(scale, scale)
    #     if clip:
    #         width = self.width
    #         height = self.height
    #         if self._enable_hinting:
    #             width, height = (
    #                 cairo_context.user_to_device_distance(width, height))
    #             # Hint in device space
    #             width = int(math.ceil(width))
    #             height = int(math.ceil(height))
    #             width, height = (
    #                 cairo_context.device_to_user_distance(width, height))
    #         cairo_context.rectangle(0, 0, width, height)
    #         cairo_context.clip()
    #     draw_page(self._page_box, cairo_context, self._enable_hinting)




# Document.write_gds
def write_gds(self, target=None, zoom=1, attachments=None):
    """Paint the pages in a GDS file, with meta-data.

    :param target:
        A filename, file-like object, or :obj:`None`.
    :type zoom: float
    :param zoom:
        This is ignored, for now. Not sure if I'll implement it. Here is
        description from original write_pdf():

        The zoom factor in PDF units per CSS units.
        **Warning**: All CSS units (even physical, like ``cm``)
        are affected.
        For values other than 1, physical CSS units will thus be “wrong”.
        Page size declarations are affected too, even with keyword values
        like ``@page { size: A3 landscape; }``
    :param attachments: A list of additional file attachments for the
        generated GDS document or :obj:`None`. The list's elements are
        :class:`Attachment` objects, filenames, URLs or file-like objects.
    :returns:
        list of gdspy.Cell objects, each corresponding to one page. 
    """
    # TODO: add control over unit/precision
    cells = []
    for ii, page in enumerate(self.pages):
        this_cell = gdspy.Cell('page ' + str(ii))
        page.paint_gds(this_cell)
        cells += [this_cell]
        # cells = cells.append(this_cell)

    # Don't think I need this...
    # write_pdf_metadata(self, file_obj, scale, self.metadata, attachments,
    #                    self.url_fetcher)

    if target is None:
        return cells
    else:
        # Cells are already a part of gdspy, don't need to add them.
        # FINISH ME: add multi-lib support in gdspy
        gdspy.gds_print(target, unit=1.0e-6, precision=5.0e-9)
