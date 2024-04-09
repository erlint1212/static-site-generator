import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node), repr(node2))
    
    def test_urlNone(self):
        node = TextNode("This is a text node", "bold") 
        self.assertEqual(node.url, None)

    def test_text_type_diff(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertEqual(node == node2, False)

if __name__ == "__main__":
    unittest.main()

