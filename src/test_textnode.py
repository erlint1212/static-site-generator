import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    maxDiff = None

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
        delimiter_tests = {"code" : "`","code" : "```", "bold":"**", "italic":"*"}
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

    def test_split_nodes_image(self):
        node = TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                text_type_text,
                )
        new_nodes = split_nodes_image([node])
        expected_output = [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                    ),
                ]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_link(self):
        node = TextNode(
                "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                text_type_text,
                )
        new_nodes = split_nodes_link([node])
        expected_output = [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                    ),
                ]
        self.assertEqual(new_nodes, expected_output)

    def test_text_to_textnodes(self):
        expected_output = [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                ]
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        output = text_to_textnodes(text)
        self.assertEqual(output, expected_output)

    def test_markdown_to_blocks(self):
        expected_output = [
                [
                    "# This is a heading", 
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
                    "* This is a list item\n* This is another list item"
                ],
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                    "* This is a list\n* with items"
                ]
            ]
        inputs = [
                    """
                    # This is a heading

                    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                    * This is a list item
                    * This is another list item
                    """, """
                    This is **bolded** paragraph

                    This is another paragraph with *italic* text and `code` here
                    This is the same paragraph on a new line

                    * This is a list
                    * with items
                    """
                ]
        for i, input in enumerate(inputs):
            with self.subTest():    
                output = markdown_to_blocks(input)
                self.assertEqual(output, expected_output[i])
    
    def test_block_to_block_type(self):
        input_expected_output = {
                "##### Header test" : block_type_heading,
                "```\n test code \n ```" : block_type_code,
                "> 4chan\n> quotes\n>are all i see" : block_type_quote,
                "* thing1\n* thing2\n* thing3" : block_type_unordered_list,
                "- thing1\n- thing2\n- thing3" : block_type_unordered_list,
                "1. thing1\n2. thing2\n3. thing3" : block_type_ordered_list,
                "plain old text" : block_type_paragraph
                }
        for test in input_expected_output.keys():
            with self.subTest():
                output = block_to_block_type(test)
                self.assertEqual(output, input_expected_output[test])

if __name__ == "__main__":
    unittest.main()

