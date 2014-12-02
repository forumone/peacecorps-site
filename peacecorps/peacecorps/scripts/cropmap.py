"""Separates an SVG map into files to represent each of its component
countries, while retaining some context. This script is tied heavily into our
country map file, but the script could be modified to resize images, provide
more context, etc."""
import copy
import itertools
import os
import sys
import xml.etree.ElementTree as ET

import svg


def highlight(doc, el_id):
    """Modify the document to add a highlight class on the country with the
    provided code"""
    root = doc.find(".//*[@id='%s']" % el_id)
    for el in itertools.chain([root], root.iterfind(".//*")):
        if el.get('class'):
            el.set('class', 'world_map-is_selected ' + el.get('class'))
    return doc


def zoom_with_context(doc, boundary):
    """Zoom to the given boundary. Adds a margin of 90% the boundary size or
    20% of the whole map, whichever is smaller"""
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
    for xml_el in itertools.chain(root.iterfind("svg:path", namespaces),
                                  root.iterfind("svg:g", namespaces)):
        code = country_code(xml_el, namespaces)
        el_bb = bboxes[code]
        if not overlaps(left, top, right, bottom,
                        el_bb[0].x, el_bb[0].y, el_bb[1].x, el_bb[1].y):
            root.remove(xml_el)


def code_to_bbox(root):
    """Run through all countries, generating a mapping between country code
    and bounding box"""
    namespaces = {"svg": "http://www.w3.org/2000/svg"}
    mapping = {}
    for xml_el in itertools.chain(root.iterfind("svg:path", namespaces),
                                  root.iterfind("svg:g", namespaces)):
        code = country_code(xml_el, namespaces)
        if xml_el.tag.endswith("path"):
            mapping[code] = svg.Path(xml_el).bbox()
        else:
            group = svg.Group(xml_el)
            group.append(xml_el)
            group.transform()
            mapping[code] = group.bbox()
    return mapping


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
    doc = ET.parse(map_path)
    root = doc.getroot()
    bboxes = code_to_bbox(root)
    for xml_el in itertools.chain(root.iterfind("svg:path", namespaces),
                                  root.iterfind("svg:g", namespaces)):
        if "landxx" in xml_el.get('class', ''):   # skip the ocean paths
            code = country_code(xml_el, namespaces)
            copy_doc = copy.deepcopy(doc)
            highlight(copy_doc, xml_el.get('id'))
            zoom_with_context(copy_doc, bboxes[code])
            crop_to(copy_doc, bboxes)

            write_file(copy_doc, outputdir, code)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cropmap.py /path/to/svg /path/to/outputdir")
    else:
        cropmap(sys.argv[1], sys.argv[2])
