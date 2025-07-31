import unittest


from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Title is here\n"
        self.assertEqual("Title is here", extract_title(md))

    def test_exception_without_title(self):
        md = "This has no title\nThere are multiple lines thoo\n\nNone has title\n"
        with self.assertRaises(Exception) as context:
            title = extract_title(md)
            self.assertIsNone(title)
        self.assertTrue("Header not found" in str(context.exception))

    def test_extract_only_first_title(self):
        md = "Why is a paragraph first?\n\n# First title\n\nParagraphs should be behind the title, right?\n\n# Title 2\n"
        self.assertEqual("First title", extract_title(md))


if __name__ == "__main__":
    unittest.main()

