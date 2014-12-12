"""Separates an SVG map into files to represent each of its component
countries, while retaining some context. This script is tied heavily into our
country map file, but the script could be modified to resize images, provide
more context, etc."""
import copy
import itertools
import logging
import os
import sys

from lxml import etree
import svg


def highlight(doc, el_id):
    """Modify the document to add a highlight class on the country with the
    provided code"""
    parent = doc.find(".//*[@id='%s']" % el_id)
    for el in itertools.chain([parent], parent.iterfind(".//*")):
        if el.get('class'):
            el.set('class', 'world_map-is_selected ' + el.get('class'))
    return doc


def zoom_with_context(doc, el_id):
    """Zoom to the given boundary. Adds a margin of 90% the boundary size or
    20% of the whole map, whichever is smaller"""
    parent = doc.find(".//*[@id='%s']" % el_id)
    boundary = bbox(parent)
    margin = 0.9
    root = doc.getroot()
    # The SVG file initially contains the whole map
    svgWidth, svgHeight = map(float, root.get('viewBox').split()[-2:])
    bndWidth = boundary[1].x - boundary[0].x
    bndHeight = boundary[1].y - boundary[0].y
    if bndWidth * margin > svgWidth * 0.1:
        margin = svgWidth * 0.1 / bndWidth
    if bndHeight * margin > svgHeight * 0.1:
        margin = svgHeight * 0.1 / bndHeight

    factor = 1 + (2 * margin)
    zoomPercent = factor * bndWidth / svgWidth
    if zoomPercent < 0.05:
        root.set('class', root.get('class') + ' zoom4')
    elif zoomPercent < 0.1:
        root.set('class', root.get('class') + ' zoom3')
    elif zoomPercent < 0.2:
        root.set('class', root.get('class') + ' zoom2')
    else:
        root.set('class', root.get('class') + ' zoom1')

    root.set('viewBox', '%d %d %d %d' % (
        (boundary[0].x - margin*bndWidth),
        (boundary[0].y - margin*bndHeight),
        factor * bndWidth, factor * bndHeight))


def overlaps(left1, top1, right1, bottom1, left2, top2, right2, bottom2):
    """Check for overlaps between the left and right rectangles"""
    return not (left2 > right1 or right2 < left1
                or top2 > bottom1 or bottom2 < top1)


def crop_to(doc, bboxes):
    """Delete any elements that are not in view"""
    root = doc.getroot()
    namespaces = {"svg": "http://www.w3.org/2000/svg"}
    left, top, width, height = map(float, root.get('viewBox').split())
    right, bottom = left + width, top + height
    # Delete any path not on screen (even if another portion of the country
    # is visible)
    for key, bbox in bboxes.items():
        if not overlaps(left, top, right, bottom,
                        bbox[0].x, bbox[0].y, bbox[1].x, bbox[1].y):
            parent = root.find(".//*[@id='%s']/.." % key)
            parent.remove(parent.find("./*[@id='%s']" % key))
    # Delete any groups which no longer have children. We run this five times
    # to account for nesting
    for _ in range(5):
        for parent in root.iterfind(".//svg:g/..", namespaces):
            for child in parent.iterfind("svg:g", namespaces):
                if len(child) == 0 or (len(child) == 1
                                       and child[0].tag.endswith('title')):
                    parent.remove(child)


def ids_to_bboxes(root):
    """Run through all paths, generating a mapping between xml id and bounding
    box"""
    namespaces = {"svg": "http://www.w3.org/2000/svg"}
    mapping = {}
    for path in itertools.chain(
            root.iterfind(".//svg:path[@id]", namespaces),
            root.iterfind(".//svg:circle[@id]", namespaces)):
        mapping[path.get('id')] = bbox(path)
    return mapping


def bbox(svg_el):
    """Bounding box for this svg element. Accounts for transformations"""
    if svg_el.tag.endswith("path"):
        return svg.Path(svg_el).bbox()
    elif svg_el.tag.endswith("circle"):
        return svg.Circle(svg_el).bbox()
    else:
        group = svg.Group(svg_el)
        group.append(svg_el)
        group.transform()
        return group.bbox()


def country_code(xml_el, namespaces):
    """Find the country code for this element"""
    if xml_el.get("class"):
        return xml_el.get("class").split()[-1]
    elif xml_el.find("svg:path", namespaces) is not None:
        return country_code(xml_el.find("svg:path", namespaces), namespaces)
    else:
        return country_code(xml_el.find("svg:g", namespaces), namespaces)


def write_file(doc, outputdir, code):
    """Serialize the xml tree and write it to disk"""
    doc.write(os.path.join(outputdir, code + ".svg"))


def cropmap(map_path, outputdir):
    """For each country in the map, create a new map file zoomed to that
    highlighted country"""
    namespaces = {"svg": "http://www.w3.org/2000/svg"}
    doc = etree.parse(map_path)
    root = doc.getroot()
    bboxes = ids_to_bboxes(root)
    for xml_el in itertools.chain(root.iterfind("svg:path", namespaces),
                                  root.iterfind("svg:g", namespaces)):
        if "oceanxx" not in xml_el.get('class', ''):   # skip the ocean paths
            code = country_code(xml_el, namespaces)
            copy_doc = copy.deepcopy(doc)
            highlight(copy_doc, xml_el.get('id'))
            zoom_with_context(copy_doc, xml_el.get('id'))
            crop_to(copy_doc, bboxes)

            write_file(copy_doc, outputdir, code)
            logging.info("Wrote %s", code)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cropmap.py /path/to/svg /path/to/outputdir")
    else:
        logging.basicConfig(level=logging.INFO)
        cropmap(sys.argv[1], sys.argv[2])
