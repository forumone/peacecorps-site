from xml.etree import ElementTree

from django.test import TestCase

from peacecorps import issue_icons


XML_HEADER = b'<?xml version="1.0" encoding="UTF-8"?>\n'


class ValidateTests(TestCase):
    def test_must_be_xml(self):
        svg_bytes = b'some text n stuff'
        self.assertIsNone(issue_icons.validate_svg(svg_bytes))

    def test_must_be_svg(self):
        svg_bytes = XML_HEADER + b'<SOMEOTHERTAG></SOMEOTHERTAG>'
        self.assertIsNone(issue_icons.validate_svg(svg_bytes))


class MakeSquareTests(TestCase):
    def test_missing_or_bad_attrs(self):
        svg = ElementTree.fromstring(XML_HEADER + b'<svg></svg>')
        self.assertIsNone(issue_icons.make_square(svg))

        svg = ElementTree.fromstring(
            XML_HEADER + b'<svg widTH="abc" height="2222px"></svg>')
        self.assertIsNone(issue_icons.make_square(svg))

    def test_resized_no_viewbox(self):
        svg = ElementTree.fromstring(
            XML_HEADER
            + b'<svg width="30" hEIght="15"></svg>')
        result = ElementTree.tostring(issue_icons.make_square(svg))
        self.assertTrue(b'width="80"' in result)
        self.assertTrue(b'hEIght="80"' in result)
        self.assertTrue(b'viewBox="0 -7 30 30"' in result)

    def test_resized_with_viewbox(self):
        svg = ElementTree.fromstring(
            XML_HEADER
            + b'<svg width="30" height="15" vIewBox="-15 10 60 30"></svg>')
        result = ElementTree.tostring(issue_icons.make_square(svg))
        self.assertTrue(b'width="80"' in result)
        self.assertTrue(b'height="80"' in result)
        self.assertTrue(b'vIewBox="-15 -5 60 60"' in result)


class ColorIconTests(TestCase):
    def test_color_fill(self):
        svg = ElementTree.fromstring(
            XML_HEADER + b'<svg width="10" height="10">'
            + b'<g strOKe="none" fill="#123"></g></svg>')
        with self.settings(SVG_COLORS={'white': '#fff', 'green': '#0f5'}):
            result = issue_icons.color_icon(svg)
            self.assertEqual(2, len(result))
            self.assertTrue('white' in result)
            self.assertTrue('green' in result)
            self.assertTrue(b'strOKe="none"' in
                            ElementTree.tostring(result['white']))
            self.assertFalse(b'fill="#0f5"' in
                             ElementTree.tostring(result['white']))
            self.assertTrue(b'fill="#0f5"' in
                            ElementTree.tostring(result['green']))

    def test_color_stroke(self):
        svg = ElementTree.fromstring(
            XML_HEADER + b'<svg width="10" height="10">'
            + b'<g stroke="#000" fill="noNE"></g></svg>')
        with self.settings(SVG_COLORS={'white': '#fff', 'green': '#0f5'}):
            result = issue_icons.color_icon(svg)
            self.assertEqual(2, len(result))
            self.assertTrue('white' in result)
            self.assertTrue('green' in result)
            self.assertTrue(b'fill="noNE"' in
                            ElementTree.tostring(result['white']))
            self.assertFalse(b'stroke="#0f5"' in
                             ElementTree.tostring(result['white']))
            self.assertTrue(b'stroke="#0f5"' in
                            ElementTree.tostring(result['green']))

    def test_color_style(self):
        svg = ElementTree.fromstring(
            XML_HEADER + b'<svg width="10" height="10">'
            + b'<g sTYle="strOKe: #123; fILL: none;"></g></svg>')
        with self.settings(SVG_COLORS={'white': '#fff', 'green': '#0f5'}):
            result = issue_icons.color_icon(svg)
            self.assertEqual(2, len(result))
            self.assertTrue('white' in result)
            self.assertTrue('green' in result)
            self.assertTrue(b'sTYle="stroke: #fff; fILL: none;"' in
                            ElementTree.tostring(result['white']))

    def test_color_embedded_stylesheet(self):
        svg = ElementTree.fromstring(
            XML_HEADER + b'<svg width="10" height="10">'
            + b'<stYLe>\n.some_class{\nfill: #123; STroke: grey;}\n</stYLe>\n'
            + b'<g class="some_class"></g></svg>')
        with self.settings(SVG_COLORS={'white': '#fff', 'green': '#0f5'}):
            result = issue_icons.color_icon(svg)
            self.assertEqual(2, len(result))
            self.assertTrue('white' in result)
            self.assertTrue('green' in result)
            self.assertTrue(b'fill: #fff;'
                            in ElementTree.tostring(result['white']))
            self.assertTrue(b'stroke: #0f5;'
                            in ElementTree.tostring(result['green']))
