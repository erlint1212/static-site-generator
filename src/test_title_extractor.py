import unittest

from title_extractor import *


class TestTitleExtractor(unittest.TestCase):
    maxDiff = None

    def test_oneLine(self):
        expected_output = "Test"
        output = extract_title("# Test")
        self.assertEqual(expected_output, output)

    def test_multLine(self): 
        expected_output = "Test"
        output = extract_title("# Test\n<div>\n<p>Test string</p>\n</div>")
        self.assertEqual(expected_output, output)

    def test_multTitle(self):
        expected_output = "Test\nTest2"
        output = extract_title("# Test\n<div>\n<p>Test string</p>\n</div>\n# Test2")
        self.assertEqual(expected_output, output)

if __name__ == "__main__":
    unittest.main()
