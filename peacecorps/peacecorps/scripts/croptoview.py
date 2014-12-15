"""Given viewport coordinates, cuts out all elements not in view."""
import sys

from lxml import etree

from cropmap import ids_to_bboxes, crop_to


def croptoview(map_path, out_path, coords):
    """Crops the provided map to the given viewbox"""
    namespaces = {"svg": "http://www.w3.org/2000/svg"}
    doc = etree.parse(map_path)
    root = doc.getroot()
    # Remove all circles
    for xml_el in root.iterfind(".//svg:circle", namespaces):
        xml_el.getparent().remove(xml_el)
    bboxes = ids_to_bboxes(root)
    root.set('viewBox', ' '.join(coords))
    crop_to(doc, bboxes)
    doc.write(out_path)

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: python croptoview.py /path/to/insvg /path/to/outsvg"
              + " [view coords]")
    else:
        croptoview(sys.argv[1], sys.argv[2], sys.argv[3:])
