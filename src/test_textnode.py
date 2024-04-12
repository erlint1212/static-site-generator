import unittest

from textnode import *


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

    # split_nodes_delimter func tests
    def test_split_node_expected(self):
        delimiter_tests = {"code" : "`", "bold":"**", "italic":"*"}
        for text_type in delimiter_tests.keys():
            with self.subTest():    
                node = TextNode(f"This is text with a {delimiter_tests[text_type]}code block{delimiter_tests[text_type]} word", "text")
                new_nodes = split_nodes_delimiter([node], delimiter_tests[text_type], text_type)
                self.assertEqual(
                                new_nodes, 
                                [
                                    TextNode("This is text with a ", "text"),
                                    TextNode("code block", text_type),
                                    TextNode(" word", "text"),
                                ]
            
                            )
    
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        output = extract_markdown_images(text)
        self.assertEqual(output, [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        output = extract_markdown_links(text)
        self.assertEqual(output, [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

if __name__ == "__main__":
    unittest.main()

