# coding: utf-8
"""
    strange.weasyprint_patches.draw
    ---------------

    patches for weasyprint.draw

"""

import gdspy


def draw_page_gds(page, cell, enable_hinting):
    """Draw the given PageBox."""
    stacking_context = scope.StackingContext.from_page(page)
    # draw_background(
    #     context, stacking_context.box.background, enable_hinting,
    #     clip_box=False)
    # draw_background(
    #     context, page.canvas_background, enable_hinting, clip_box=False)
    # draw_border(context, page, enable_hinting)
    draw_stacking_context_gds(cell, stacking_context, enable_hinting)


def draw_box_background_and_border_gds(cell, page, box, enable_hinting):
    # Background has no meaning in gds
    # draw_background_gds(cell, box.background, enable_hinting)
    if isinstance(box, scope.boxes.TableBox):
        ## No tables in layout!
        pass
        # draw_table_backgrounds(cell, page, box, enable_hinting)
        # if box.style.border_collapse == 'separate':
        #     draw_border_gds(cell, box, enable_hinting)
        #     for row_group in box.children:
        #         for row in row_group.children:
        #             for tcell in row.children:
        #                 if tcell.style.empty_cells == 'show' or not tcell.empty:
        #                     draw_border_gds(cell, tcell, enable_hinting)
        # else:
        #     draw_collapsed_borders_gds(cell, box, enable_hinting)
    else:
        draw_border_gds(cell, box, enable_hinting)



def draw_stacking_context_gds(cell, stacking_context, enable_hinting):
    """Draw a ``stacking_context`` on ``cell``."""

    # some things from scope
    boxes = scope.boxes


    # See http://www.w3.org/TR/CSS2/zindex.html

    # I think the two with statements are just a way to temp. work with clip()
    # TODO: check this

    
    # TODO: clipping?
    box = stacking_context.box
    if box.is_absolutely_positioned() and box.style.clip:
        top, right, bottom, left = box.style.clip
        if top == 'auto':
            top = 0
        if right == 'auto':
            right = 0
        if bottom == 'auto':
            bottom = box.border_height()
        if left == 'auto':
            left = box.border_width()
        cell.rectangle(
            box.border_box_x() + right,
            box.border_box_y() + top,
            left - right,
            bottom - top)
        # cell.clip()


    # We shouldn't be doing any transformations...
    # if box.transformation_matrix:
    #     try:
    #         box.transformation_matrix.copy().invert()
    #     except cairo.cairoerror:
    #         return
    #     else:
    #         context.transform(box.transformation_matrix)


    # point 1 is done in draw_page

    # point 2
    if isinstance(box, (boxes.BlockBox, boxes.MarginBox,
                        boxes.InlineBlockBox, boxes.TableCellBox)):
        # the canvas background was removed by set_canvas_background
        draw_box_background_and_border_gds(
            cell, stacking_context.page, box, enable_hinting)

    # No rounded box borders (for now?) or clipping...
    # if box.style.overflow != 'visible':
    #     # only clip the content and the children:
    #     # - the background is already clipped
    #     # - the border must *not* be clipped
    #     rounded_box_path_gds(cell, box.rounded_padding_box())
    #     context.clip()

    # point 3
    for child_context in stacking_context.negative_z_contexts:
        draw_stacking_context_gds(cell, child_context, enable_hinting)

    # point 4
    for block in stacking_context.block_level_boxes:
        draw_box_background_and_border_gds(
            cell, stacking_context.page, block, enable_hinting)

    # point 5
    for child_context in stacking_context.float_contexts:
        draw_stacking_context_gds(cell, child_context, enable_hinting)

    # point 6
    if isinstance(box, boxes.InlineBox):
        draw_inline_level_gds(
            cell, stacking_context.page, box, enable_hinting)

    # point 7
    for block in [box] + stacking_context.blocks_and_cells:
        marker_box = getattr(block, 'outside_list_marker', None)
        if marker_box:
            draw_inline_level_gds(
                cell, stacking_context.page, marker_box,
                enable_hinting)

        if isinstance(block, boxes.ReplacedBox):
            draw_replacedbox_gds(cell, block)
        else:
            for child in block.children:
                if isinstance(child, boxes.LineBox):
                    # todo: draw inline tables
                    draw_inline_level_gds(
                        cell, stacking_context.page, child,
                        enable_hinting)

    # point 8
    for child_context in stacking_context.zero_z_contexts:
        draw_stacking_context_gds(cell, child_context, enable_hinting)

    # point 9
    for child_context in stacking_context.positive_z_contexts:
        draw_stacking_context_gds(cell, child_context, enable_hinting)

    # point 10
    draw_outlines_gds(cell, box, enable_hinting)


def draw_border_gds(cell, box, enable_hinting):
    """Draw the box border to a ``gdspy.Cell``."""
    # We need a plan to draw beautiful borders, and that's difficult, no need
    # to lie. Let's try to find the cases that we can handle in a smart way.


    # TO DO: Add more interesting border features (ie guard rings)


    # def draw_column_border():
    #     """Draw column borders."""
    #     columns = (
    #         box.style.column_width != 'auto' or
    #         box.style.column_count != 'auto')
    #     if columns and box.style.column_rule_width:
    #         border_widths = (0, 0, 0, box.style.column_rule_width)
    #         for child in box.children[1:]:
    #             position_x = (child.position_x - (
    #                 box.style.column_rule_width +
    #                 box.style.column_gap) / 2)
    #             border_box = (
    #                 position_x, child.position_y,
    #                 box.style.column_rule_width, box.height)
    #             clip_border_segment(
    #                 context, enable_hinting, box.style.column_rule_style,
    #                 box.style.column_rule_width, 'left', border_box,
    #                 border_widths)
    #             draw_rect_border(
    #                 context, border_box, border_widths,
    #                 box.style.column_rule_style, styled_color(
    #                     box.style.column_rule_style,
    #                     box.style.get_color('column_rule_color'), 'left'))

    # The box is hidden, easy.
    if box.style.visibility != 'visible':
        # draw_column_border()
        return

    widths = [getattr(box, 'border_%s_width' % side) for side in scope.SIDES]

    # No border, return early.
    if all(width == 0 for width in widths):
        # draw_column_border()
        return

    colors = [
        box.style.get_color('border_%s_color' % side) for side in scope.SIDES]
    styles = [
        colors[i].alpha and box.style['border_%s_style' % side]
        for (i, side) in enumerate(scope.SIDES)]

    # The 4 sides are solid or double, and they have the same color. Oh yeah!
    # We can draw them so easily!
    # if set(styles) in (set(('solid',)), set(('double',))) and (
    #         len(set(colors)) == 1):
    if set(styles) in (set(('solid',)), set(('double',))):
        draw_rounded_border_gds(cell, box, styles[0], box.style['layer'])
        # draw_column_border()
        return

    # # We're not smart enough to find a good way to draw the borders :/. We must
    # # draw them side by side.
    # for side, width, color, style in zip(SIDES, widths, colors, styles):
    #     if width == 0 or not color:
    #         continue
    #     with stacked(context):
    #         clip_border_segment(
    #             context, enable_hinting, style, width, side,
    #             box.rounded_border_box()[:4], widths,
    #             box.rounded_border_box()[4:])
    #         draw_rounded_border(
    #             context, box, style, styled_color(style, color, side))

    # draw_column_border()


def draw_rounded_border_gds(cell, box, style, layer):
    x,y,w,h, *_ = box.rounded_border_box()
    draw_rect_border_gds(cell, (x,y,w,h), [], style, layer)

    # TO DO: add rounded border feature?
    # context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    # rounded_box_path(context, box.rounded_padding_box())
    # if style in ('ridge', 'groove'):
    #     rounded_box_path(context, box.rounded_box_ratio(1 / 2))
    #     context.set_source_rgba(*color[0])
    #     context.fill()
    #     rounded_box_path(context, box.rounded_box_ratio(1 / 2))
    #     rounded_box_path(context, box.rounded_border_box())
    #     context.set_source_rgba(*color[1])
    #     context.fill()
    #     return
    # if style == 'double':
    #     rounded_box_path(context, box.rounded_box_ratio(1 / 3))
    #     rounded_box_path(context, box.rounded_box_ratio(2 / 3))
    # rounded_box_path(context, box.rounded_border_box())
    # context.set_source_rgba(*color)
    # context.fill()


def draw_rect_border_gds(cell, box, widths, style, layer):
    PPU = scope.PPU


    bbx, bby, bbw, bbh = box
    # bt, br, bb, bl = widths

    # PPU is Pixels per Unit (UNITS/PRECISION)  
    bbx /= PPU
    bby /= PPU
    bbw /= PPU
    bbh /= PPU
    cell.add(  
        gdspy.Rectangle((bbx, -bby),
        (bbx+bbw, -(bby+bbh)), layer) )

    # TO DO: add more interesting border style features.
    # context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    # bbx, bby, bbw, bbh = box
    # bt, br, bb, bl = widths
    # context.rectangle(*box)
    # if style in ('ridge', 'groove'):
    #     context.rectangle(
    #         bbx + bl / 2, bby + bt / 2,
    #         bbw - (bl + br) / 2, bbh - (bt + bb) / 2)
    #     context.set_source_rgba(*color[0])
    #     context.fill()
    #     context.rectangle(
    #         bbx + bl / 2, bby + bt / 2,
    #         bbw - (bl + br) / 2, bbh - (bt + bb) / 2)
    #     context.rectangle(
    #         bbx + bl, bby + bt, bbw - bl - br, bbh - bt - bb)
    #     context.set_source_rgba(*color[1])
    #     context.fill()
    #     return
    # if style == 'double':
    #     context.rectangle(
    #         bbx + bl / 3, bby + bt / 3,
    #         bbw - (bl + br) / 3, bbh - (bt + bb) / 3)
    #     context.rectangle(
    #         bbx + bl * 2 / 3, bby + bt * 2 / 3,
    #         bbw - (bl + br) * 2 / 3, bbh - (bt + bb) * 2 / 3)
    # context.rectangle(bbx + bl, bby + bt, bbw - bl - br, bbh - bt - bb)
    # context.set_source_rgba(*color)
    # context.fill()



def draw_outlines_gds(cell, box, enable_hinting):
    boxes = scope.boxes

    width = box.style.outline_width
    # TO DO: make this 'layer'
    color = box.style.get_color('outline_color')
    style = box.style.outline_style
    if box.style.visibility == 'visible' and width != 0:
        outline_box = (
            box.border_box_x() - width, box.border_box_y() - width,
            box.border_width() + 2 * width, box.border_height() + 2 * width)
        draw_rect_border_gds(
            cell, outline_box, 4 * (width,), style,
            box.style['layer'])

    if isinstance(box, boxes.ParentBox):
        for child in box.children:
            if isinstance(child, boxes.Box):
                draw_outlines_gds(cell, child, enable_hinting)



def draw_replacedbox_gds(cell, box):
    """Draw the given :class:`boxes.ReplacedBox` to a ``gdspy.Cell``."""
    # if box.style.visibility != 'visible' or box.width == 0 or box.height == 0:
    #     return

    # rounded_box_path(cell, box.rounded_content_box())
    cbx = box.content_box_x()
    cby = box.content_box_y()
    box.replacement.translate_px( [cbx, -cby] )
    box.replacement.draw(cell)
    # box.replacement.draw(
    #     cell, box.width, box.height, box.style.image_rendering)



def draw_inline_level_gds(cell, page, box, enable_hinting):
    boxes = scope.boxes

    if isinstance(box, scope.StackingContext):
        stacking_context = box
        assert isinstance(stacking_context.box, boxes.InlineBlockBox)
        draw_stacking_context_gds(cell, stacking_context, enable_hinting)
    else:
        # draw_background(context, box.background, enable_hinting)
        draw_border_gds(cell, box, enable_hinting)
        if isinstance(box, (boxes.InlineBox, boxes.LineBox)):
            for child in box.children:
                if isinstance(child, boxes.TextBox):
                    # TO DO: add text labels
                    pass
                    # draw_text(context, child, enable_hinting)
                else:
                    draw_inline_level_gds(cell, page, child, enable_hinting)
        elif isinstance(box, boxes.InlineReplacedBox):
            draw_replacedbox_gds(cell, box)
        else:
            assert isinstance(box, boxes.TextBox)
            # Should only happen for list markers
            # draw_text(context, box, enable_hinting)
