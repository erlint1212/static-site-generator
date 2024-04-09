import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_PROPS_TO_HTML_None(self):
        node = HTMLNode()
        with self.assertRaises(ValueError):
            node.PROPS_TO_HTML()
        
    def test_PROPS_TO_HTML_NotDict(self):
        node = HTMLNode(PROPS=['Not','a', 'dict'])
        with self.assertRaises(ValueError):
            node.PROPS_TO_HTML()

    def test_PROPS_TO_HTML_works(self):
        node = HTMLNode(PROPS={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.PROPS_TO_HTML(), "href=\"https://www.google.com\" target=\"_blank\"")

    def test_REPR(self):
        node = HTMLNode("h1", "test text", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), "HTMLNode(h1, test text, None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_TO_HTML(self):        
        node = HTMLNode("h1", "test text", None, {"href": "https://www.google.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.TO_HTML()

if __name__ == "__main__":
    unittest.main()
