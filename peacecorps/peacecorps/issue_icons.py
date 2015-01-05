from copy import deepcopy
from itertools import takewhile
import re

from defusedxml import ElementTree
from django.conf import settings


def validate_svg(svg_bytes):
    """Quick checks that a file is an svg. Returns the file as an xml tree"""
    try:
        tree = ElementTree.fromstring(svg_bytes)
        if tree.tag.upper() == 'SVG':
            return tree
    except ElementTree.ParseError:
        pass


def make_square(svg_xml):
    """Give the icon enough padding to be square. Resize to 80 x 80"""
    svg_xml = deepcopy(svg_xml)
    width, height = svg_xml.get('width', ''), svg_xml.get('height', '')
    width = ''.join(takewhile(lambda c: c.isdigit(), width))
    height = ''.join(takewhile(lambda c: c.isdigit(), height))
    try:
        width, height = int(width), int(height)
        # we will assume aspect ratio is preserved
        viewBox = svg_xml.get('viewBox', '%d %d %d %d' % (0, 0, width, height))
        vX, vY, vWidth, vHeight = map(int, viewBox.split(' '))

        if vHeight > vWidth:
            svg_xml.set('viewBox', '%d %d %d %d' % (
                vX - (vHeight - vWidth)/2, vY, vHeight, vHeight))
        else:
            svg_xml.set('viewBox', '%d %d %d %d' % (
                vX, vY - (vWidth - vHeight)/2, vWidth, vWidth))
        svg_xml.set('width', '80')
        svg_xml.set('height', '80')
        return svg_xml
    except ValueError:
        pass


STROKE_STYLE = re.compile(r'stroke\s*:(?P<value>[^;]+)', re.IGNORECASE)
FILL_STYLE = re.compile(r'fill\s*:*(?P<value>[^;]+)', re.IGNORECASE)


def _color_attr(node, hex_val):
    """Color stroke/fill if they are attributes on an XML Node, e.g.
    <path stroke="#abc"... """
    stroke, fill = node.get('stroke'), node.get('fill')
    if stroke and stroke != 'none':
        node.set('stroke', hex_val)
    if fill and fill != 'none':
        node.set('fill', hex_val)


def _style_replacement(haystack, hex_val):
    """Helper function to replace stroke and fill in a style string,
    `haystack`"""
    match = STROKE_STYLE.search(haystack)
    while match:
        if match.group('value').strip() != 'none':
            new_style = haystack[:match.start()] + 'stroke: ' + hex_val
            new_style += haystack[match.end():]
            haystack = new_style
        match = STROKE_STYLE.search(haystack, match.start() + 1)
    match = FILL_STYLE.search(haystack)
    while match:
        if match.group('value').strip() != 'none':
            new_style = haystack[:match.start()] + 'fill: ' + hex_val
            new_style += haystack[match.end():]
            haystack = new_style
        match = FILL_STYLE.search(haystack, match.start() + 1)
    return haystack


def color_icon(svg_xml):
    """Return a set of svg files where all elements are filled with predefined
    colors (e.g. grey)"""
    # first, convert it all to lower case
    svg_str = ElementTree.tostring(svg_xml)
    svg_xml = ElementTree.fromstring(svg_str.lower())
    colored = {}
    for color, hex_val in settings.SVG_COLORS.items():
        colored_svg = deepcopy(svg_xml)
        for node in colored_svg.findall("*"):
            _color_attr(node, hex_val)

            # Inline styles, e.g. <path style="stroke: #abc; other: value"...
            if node.get('style'):
                node.set('style',
                         _style_replacement(node.get('style'), hex_val))

            # Style tag, e.g. <style>.someClass{fill: #abc; other: value...
            if node.tag == 'style':
                node.text = _style_replacement(node.text or '', hex_val)

        colored[color] = colored_svg
    return colored
