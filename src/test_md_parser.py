import unittest

from md_parser import split_nodes_delimiter

from textnode import TextNode, TextType

class TestMDParser(unittest.TestCase):
    def test_non_delimited_text_unmodified(self):
        new_nodes = split_nodes_delimiter([TextNode("This node does not contain a delimiter", TextType.TEXT, None)], "_", TextType.ITALIC)
        self.assertEqual(1, len(new_nodes))
        self.assertEqual(TextNode("This node does not contain a delimiter",TextType.TEXT), new_nodes[0])

    def test_other_text_types_unmodified(self):
        new_nodes = split_nodes_delimiter([TextNode("This node does _contain_ a delimiter", TextType.BOLD)], "_", TextType.ITALIC)
        self.assertEqual(1, len(new_nodes))
        self.assertEqual(TextNode("This node does _contain_ a delimiter", TextType.BOLD), new_nodes[0])

    def test_text_into_italic(self):
        new_nodes = split_nodes_delimiter([TextNode("This node does _contain_ a delimiter", TextType.TEXT)], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This node does ", TextType.TEXT),
                TextNode("contain",TextType.ITALIC),
                TextNode(" a delimiter", TextType.TEXT)
            ],
            new_nodes
        )


    def test_text_into_bold(self):
        new_nodes = split_nodes_delimiter([TextNode("This node does **contain** a delimiter", TextType.TEXT)], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This node does ", TextType.TEXT),
                TextNode("contain",TextType.BOLD),
                TextNode(" a delimiter", TextType.TEXT)
            ],
            new_nodes
        )

    def test_text_starts_with_delimiter(self):
        new_nodes = split_nodes_delimiter([TextNode("**Bold** text first", TextType.TEXT)], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" text first", TextType.TEXT)
            ],
            new_nodes
        )

    def test_text_ends_with_delimiter(self):
        nodes = split_nodes_delimiter([TextNode("The last word is **Bold**", TextType.TEXT)], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("The last word is ", TextType.TEXT),
                TextNode("Bold", TextType.BOLD)
            ],
            nodes
        )

    def test_text_starts_and_ends_width_delimiter(self):
        nodes = split_nodes_delimiter([TextNode("**This text is Bold**", TextType.TEXT)], "**", TextType.BOLD)
        self.assertListEqual([TextNode("This text is Bold", TextType.BOLD)], nodes)

    def test_multiple_identical_delimiters(self):
        nodes = split_nodes_delimiter([TextNode("**This** text contains **Bold** parts", TextType.TEXT)], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" text contains ", TextType.TEXT),
                TextNode("Bold", TextType.BOLD),
                TextNode(" parts", TextType.TEXT)
            ],
            nodes
        )

    def test_multiple_different_delimiters(self):
        nodes = split_nodes_delimiter([TextNode("**This** text contains _Italic_ parts", TextType.TEXT)], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" text contains _Italic_ parts", TextType.TEXT)
            ],
            nodes
        )

        nodes2 = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" text contains ", TextType.TEXT),
                TextNode("Italic", TextType.ITALIC),
                TextNode(" parts", TextType.TEXT)
            ],
            nodes2
        )

    def test_unterminated_delimiters_raise(self):
        with self.assertRaises(Exception) as context:
            nodes = split_nodes_delimiter([TextNode("This contains **unterminated delimiters",TextType.TEXT)], "**", TextType.BOLD)
            self.assertIsNone(nodes)

        self.assertIsInstance(context.exception, SyntaxError)
        self.assertEqual("SyntaxError: Delimiter '**' was never closed", str(context.exception))


if __name__ == "__main__":
    unittest.main()

