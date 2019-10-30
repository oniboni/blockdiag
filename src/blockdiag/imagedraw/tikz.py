# -*- coding: utf-8 -*-
'''
Created on Oct 29, 2019

@author: oni
'''
from blockdiag.imagedraw import base
from blockdiag.imagedraw.utils import textsize, memoize
from PIL.ImageColor import getrgb
from distutils import basestring


tikz_file_template = '''
\\usetikzlibrary{{calc,arrows,positioning}}

\\begin{{tikzpicture}}
{content}
\\end{{tikzpicture}}
'''


class TikZDraw(base.ImageDraw):
    tikz_content = list()  # list of tikz instructions (strings)
    tikz_dpi = 72

    supported_path = True
    baseline_text_rendering = True

    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.options = kwargs
        self.set_canvas_size((0, 0))

    def _get_inches(self, px):
        return round(px / self.tikz_dpi, 3)

    def path(self, pd, **kwargs):
        pass

    def rectangle(self, box, **kwargs):
        draw_filter = kwargs.get('filter', None)
        draw_fill = kwargs.get('fill', None)
        draw_outline = kwargs.get('outline', None)

        node_width = self._get_inches(box.width)
        node_height = self._get_inches(box.height)
        node_pos_x = self._get_inches(box.topleft.x)
        node_pos_y = -self._get_inches(box.topleft.y)

        node_options = ['shape=rectangle',
                        'anchor=north west',
                        'minimum width={}in'.format(node_width),
                        'minimum height={}in'.format(node_height)]

        if draw_filter and draw_filter == 'transp-blur':
            node_options.append('opacity=0.2')

        if draw_fill:
            if isinstance(draw_fill, basestring):
                draw_fill = getrgb(draw_fill)

            node_options.append(
                'fill={{rgb,255:red,{}; green,{}; blue,{}}}'.format(*draw_fill))

        if draw_outline:
            if isinstance(draw_outline, basestring):
                draw_fill = getrgb(draw_outline)

            node_options.append(
                'draw={{rgb,255:red,{}; green,{}; blue,{}}}'.format(*draw_outline))

        self.tikz_content.append(
            '\\node [{}] at ({}in,{}in) {{}};'
            .format(','.join(node_options), node_pos_x, node_pos_y))

    @memoize
    def textlinesize(self, string, font, **kwargs):
        return textsize(string, font)  # TODO: not applicable (?)

    def text(self, point, string, font, **kwargs):
        pass

    def textarea(self, box, string, font, **kwargs):
        alignment = kwargs.get('halign', 'center')
        node_width = self._get_inches(box.width)
        node_height = self._get_inches(box.height)
        node_pos_x = self._get_inches(box.topleft.x)
        node_pos_y = -self._get_inches(box.topleft.y)

        self.tikz_content.append(
            '\\node[minimum width={}in, minimum height={}in, align={}, anchor=north west] at ({}in,{}in) {{{}}};'
            .format(node_width, node_height, alignment, node_pos_x, node_pos_y, string))

    def rotated_textarea(self, box, string, font, **kwargs):
        pass

    def _draw_path(self, points, cycle, kwargs):
        draw_style = kwargs.get('style', None)
        draw_fill = kwargs.get('fill', None)
        draw_outline = kwargs.get('outlline', None)

        path_options = ['draw']
        if draw_style:
            if draw_style in ['dotted', 'dashed']:
                path_options.append(draw_style)
            elif draw_style == 'none':
                path_options.append('solid')
            else:
                path_options.append('dash pattern=on {}in off {}in'.format(
                    *[self._get_inches(int(a)) for a in draw_style.split(',')]))

        if draw_fill:
            if isinstance(draw_fill, basestring):
                draw_fill = getrgb(draw_fill)

            path_options.append(
                'fill={{rgb,255:red,{}; green,{}; blue,{}}}'.format(*draw_fill))

        if draw_outline:
            if isinstance(draw_outline, basestring):
                draw_outline = getrgb(draw_outline)

            path_options.append(
                'draw={{rgb,255:red,{}; green,{}; blue,{}}}'.format(*draw_outline))

        path_positions = ' -- '.join(['({}in,{}in)'.format(self._get_inches(p.x), -self._get_inches(p.y))
                                      for p in points])

        self.tikz_content.append('\\path [{}] {}{};'.format(
            ','.join(path_options), path_positions, ' -- cycle' if cycle else ''))

    def line(self, points, **kwargs):
        self._draw_path(points, False, kwargs)

    def arc(self, box, start, end, **kwargs):
        pass

    def ellipse(self, box, **kwargs):
        pass

    def polygon(self, points, **kwargs):
        self._draw_path(points, True, kwargs)

    def image(self, box, url):
        pass

    def anchor(self, url):
        pass

    def save(self, filename, size, _format):
        if self.filename:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.write(tikz_file_template.format(
                    content='\n'.join(self.tikz_content)))


def setup(self):
    from blockdiag.imagedraw import install_imagedrawer
    install_imagedrawer('tikz', TikZDraw)
