import unittest

from markdown_to_html import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_single_line_code_block(self):
        md = "```Print('Hello, Worldo')```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><pre><code>Print('Hello, Worldo')</code></pre></div>",
            node.to_html()
        )

    def test_multi_line_code_block(self):
        md = "```Print('Hello, Worldo')\n# This is a comment\nif 1 == 2:\n    Print('WTF')```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><pre><code>Print('Hello, Worldo')\n# This is a comment\nif 1 == 2:\n    Print('WTF')</code></pre></div>",
            node.to_html()
        )

    def test_single_quote_block(self):
        md = "> This might be quoted in the future."
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><blockquote><p>This might be quoted in the future.</p></blockquote></div>",
            node.to_html()
        )

    def test_multi_line_quote_block(self):
        md = "> This quote\n> might be split\n> in multiple\n> lines"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><blockquote><p>This quote\nmight be split\nin multiple\nlines</p></blockquote></div>",
            node.to_html()
        )

    def test_single_header_block(self):
        md = "# Header for some document"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><h1>Header for some document</h1></div>",
            node.to_html()
        )

    def test_multiple_header_block(self):
        md = "# Header for some document\n\nParagraph says something\n\n## subsection 1"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><h1>Header for some document</h1><p>Paragraph says something</p><h2>subsection 1</h2></div>",
            node.to_html()
        )

    def test_single_line_unordered_list_block(self):
        md = "- Single line list"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><ul><li>Single line list</li></ul></div>",
            node.to_html()
        )

    def test_multi_line_unordered_list_block(self):
        md = "- First line\n- Second line\n- Third line"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><ul><li>First line</li><li>Second line</li><li>Third line</li></ul></div>",
            node.to_html()
        )

    def test_single_line_ordered_list_block(self):
        md = "1. Single line list"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><ol><li>Single line list</li></ol></div>",
            node.to_html()
        )

    def test_multi_line_ordered_list_block(self):
        md = "1. First line\n2. Second line\n3. Third line"
        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><ol><li>First line</li><li>Second line</li><li>Third line</li></ol></div>",
            node.to_html()
        )

if __name__ == "__main__":
    unittest.main()
