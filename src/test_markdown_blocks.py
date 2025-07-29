import unittest

from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            markdown_to_blocks(md)
        )

    def test_markdown_to_block(self):
        md = """
This is **bolded** paragraph
This is the same paragraph with _italic_ text and `code` here
This is still the same paragraph on a new line
"""
        self.assertListEqual(
            [
                "This is **bolded** paragraph\n"
                "This is the same paragraph with _italic_ text and `code` here\n"
                    "This is still the same paragraph on a new line",
            ],
            markdown_to_blocks(md)
        )

    def test_markdown_with_blank_lines(self):
        md = """
This is a paragraph


This is another paragraph



This is a third paragraph




This is a fourth paragraph
"""

        self.assertListEqual(
            [
                "This is a paragraph",
                "This is another paragraph",
                "This is a third paragraph",
                "This is a fourth paragraph",
            ],
            markdown_to_blocks(md)
        )


    def test_markdown_with_blank_spares(self):
        md = """
    This is a paragraph
This is the same paragraph    


\tThis is another paragraph
With tabs at the start and end of it\t
"""

        self.assertListEqual(
            [
                "This is a paragraph\nThis is the same paragraph",
                "This is another paragraph\nWith tabs at the start and end of it"
            ],
            markdown_to_blocks(md)
        )


if __name__ == "__main__":
    unittest.main()

