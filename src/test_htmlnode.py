import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_PROPS_TO_HTML_None(self):
        node = HTMLNode()
        self.assertEqual(node.PROPS_TO_HTML(), None)
        
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

    # Test leafnode
    def test_TO_HTML(self):
        node = LeafNode("h1", "test text", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.TO_HTML(), "<h1 href=\"https://www.google.com\" target=\"_blank\">test text</h1>")

    def test_TO_HTML_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.TO_HTML(), "<p>This is a paragraph of text.</p>")
    
    # Test ParentNode
    def test_ParentNode_TO_HTML_expected(self):
        node = LeafNode("h1", "test1", {"href": "www.link.com"})
        node1 = LeafNode("b", "test2")
        node2 = LeafNode("p", "test3")
        parent_node = ParentNode("div", CHILDREN=[node, node1, node2])
        self.assertEqual(parent_node.TO_HTML(), "<div><h1 href=\"www.link.com\">test1</h1><b>test2</b><p>test3</p></div>")

    def test_ParentNode_TO_HTML_nested(self):
        with self.subTest():
            node = LeafNode("h1", "test1", {"href": "www.link.com"})
            node1 = LeafNode("b", "test2")
            node2 = ParentNode("p", [node, node1])
            parent_node = ParentNode("div", CHILDREN=[node2])
            self.assertEqual(parent_node.TO_HTML(), "<div><p><h1 href=\"www.link.com\">test1</h1><b>test2</b></p></div>")

        with self.subTest():
            node = LeafNode("h1", "test1", {"href": "www.link.com"})
            node1 = LeafNode("b", "test2")
            node2 = ParentNode("p", [node, node1])
            node3 = ParentNode("i", [node2])
            parent_node = ParentNode("div", CHILDREN=[node3])
            self.assertEqual(parent_node.TO_HTML(), "<div><i><p><h1 href=\"www.link.com\">test1</h1><b>test2</b></p></i></div>")

    def test_ParentNode_NoChildren(self):
        with self.assertRaises(ValueError):
            node = ParentNode()

    def test_ParentNode_EmptyChildren(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, None, [])

    # TextNode to HTMLNode function tests
    def test_TextNode_tags(self):
        supported_tags = {
                    "text" : None,
                    "bold" : "b",
                    "italic" : "i",
                    "image" : "img",
                    "link" : "a",
                    "code" : "```"
                }
        for text_type in supported_tags.keys():
            with self.subTest():
                node = text_node_to_html_node(TextNode(f"testing {text_type}", text_type))
                if text_type not in ["link", "image", "code"]:
                    self.assertEqual(node.TO_HTML(), LeafNode(supported_tags[text_type], f"testing {text_type}").TO_HTML())
                match text_type:
                    case "link":
                        self.assertEqual(node.TO_HTML(), f"<a href=\"None\">testing {text_type}</a>")
                    case "image":
                        self.assertEqual(node.TO_HTML(), f"<img src=\"None\" alt=\"testing {text_type}\">")
                    case "code":
                        self.assertEqual(node.TO_HTML(), f"```testing {text_type}```")

if __name__ == "__main__":
    unittest.main()
