from copy import deepcopy
import re

from defusedxml import ElementTree
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile


def _case_insensitive_attr(node, lowercase_attr):
    """Find attribute name regardless of case"""
    lowercase_attr = lowercase_attr.lower()
    for attr in node.attrib:
        if attr.lower() == lowercase_attr:
            return attr


def validate_svg(svg_bytes):
    """Quick checks that a file is an svg. Returns the file as an xml tree"""
    try:
        tree = ElementTree.fromstring(svg_bytes)
        if tree.tag.upper().endswith('SVG'):    # endswith b/c namespaces
            return tree
    except ElementTree.ParseError:
        pass


def make_square(svg_xml):
    """Give the icon enough padding to be square. Resize to 80 x 80"""
    svg_xml = deepcopy(svg_xml)
    view_box_attr = _case_insensitive_attr(svg_xml, 'viewBox')
    width_attr = _case_insensitive_attr(svg_xml, 'width')
    height_attr = _case_insensitive_attr(svg_xml, 'height')

    if view_box_attr:
        view_box = svg_xml.get(view_box_attr)
    elif width_attr and height_attr:
        view_box = '0 0 %s %s' % (svg_xml.get(width_attr),
                                  svg_xml.get(height_attr))
        view_box_attr = 'viewBox'
    else:
        return  # Can't compute a height/width

    # Strip non-numbers
    view_box = re.sub(r"[^0-9\. -]", "", view_box)
    try:
        vX, vY, vWidth, vHeight = map(int, map(float, view_box.split(' ')))
        if vHeight > vWidth:
            svg_xml.set(view_box_attr, '%d %d %d %d' % (
                vX - (vHeight - vWidth)/2, vY, vHeight, vHeight))
        else:
            svg_xml.set(view_box_attr, '%d %d %d %d' % (
                vX, vY - (vWidth - vHeight)/2, vWidth, vWidth))
        svg_xml.set(width_attr or 'width', '80')
        svg_xml.set(height_attr or 'height', '80')
        return svg_xml
    except ValueError:
        pass


def full_validation(svg_file):
    xml = validate_svg(svg_file.read())
    if not xml:
        raise ValidationError('Icon must be an svg')
    square = make_square(xml)
    if not square:
        raise ValidationError('Icon is malformed')
    svg_file.seek(0, 0)


STROKE_STYLE = re.compile(r'stroke\s*:(?P<value>[^;]+)', re.IGNORECASE)
FILL_STYLE = re.compile(r'fill\s*:*(?P<value>[^;]+)', re.IGNORECASE)


def _color_attr(node, hex_val):
    """Color stroke/fill if they are attributes on an XML Node, e.g.
    <path stroke="#abc"... """
    stroke_attr = _case_insensitive_attr(node, 'stroke')
    fill_attr = _case_insensitive_attr(node, 'fill')

    if stroke_attr and node.get(stroke_attr).lower() != 'none':
        node.set(stroke_attr, hex_val)
    if fill_attr and node.get(fill_attr).lower() != 'none':
        node.set(fill_attr, hex_val)


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
    colored = {}
    for color, hex_val in settings.SVG_COLORS.items():
        colored_svg = deepcopy(svg_xml)
        for node in colored_svg.findall(".//*"):
            _color_attr(node, hex_val)

            # Inline styles, e.g. <path style="stroke: #abc; other: value"...
            style_attr = _case_insensitive_attr(node, 'style')
            if style_attr:
                node.set(style_attr,
                         _style_replacement(node.get(style_attr), hex_val))

            # Style tag, e.g. <style>.someClass{fill: #abc; other: value...
            if node.tag.lower().endswith('style'):
                node.text = _style_replacement(node.text or '', hex_val)

        colored[color] = colored_svg
    return colored


def as_file(svg_xml):
    """Converts the xml object into a django ContentFile"""
    return ContentFile(ElementTree.tostring(svg_xml))
