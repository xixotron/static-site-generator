import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


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


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("# Heading block"))

    def test_singe_line_code_block(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("```CODE GOES HERE```"))

    def test_multi_line_code_block(self):
        self.assertEqual(
            BlockType.CODE,
            block_to_block_type("```main():\n    print('Hello, world!')\nmain() # writes to console```")
        )

    def test_single_line_quote_block(self):
        self.assertEqual(
            BlockType.QUOTE,
            block_to_block_type("> quotes say things someone previously said")
        )

    def test_multi_line_quote_block(self):
        self.assertEqual(
            BlockType.QUOTE,
            block_to_block_type(
"""> quotes say things someone previously said
> some quotes have more than one line
> others my be long
> spread over multiple lines"""
            )
        )

    def test_single_line_unordered_list_block(self):
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type("- There could be single entry lists")
        )

    def test_multi_line_unordered_list_block(self):
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type(
"""- This is part of a list
- Lists can have multiple entries
- List can be long
- This also is part of a list"""
            )
        )

    def test_single_line_ordered_list_block(self):
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type("1. There could be single entry lists")
        )

    def test_multi_line_ordered_list_block(self):
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type(
"""1. This is part of a list
2. Lists can have multiple entries
3. List can be long
4. This also is part of a list"""
            )
        )

    def test_single_line_paragraph_block(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("There can be single paragraphs")
        )

    def test_multi_line_paragraph_block(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(
"""There can also be paragraphs
That span multiple
lines of text"""
            )
        )

    def test_malformed_code_block(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("```This is not a valid code block")
        )

    def test_malformed_quote_block(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("> This is not a valid\n> quote block\nThe last line doesn't start with '> '")
        )

    def test_malformed_unordered_list_block(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("- This is not a valid\nunordered\n- list block")
        )

    def test_malformed_ordered_list_block(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("1. This is not a valid\n1. unordered\n1. list block")
        )

    def test_malformed_ordered_list_block2(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("1. This is not a valid\n2. unordered\nlist block")
        )

if __name__ == "__main__":
    unittest.main()

