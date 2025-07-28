import unittest

from md_parser import split_nodes_delimiter

from textnode import TextNode, TextType

class TestMDParser(unittest.TestCase):
    def test_non_delimited_text_unmodified(self):
        nodes = split_nodes_delimiter([TextNode("This node does not contain a delimiter", TextType.TEXT, None)], "_", TextType.ITALIC)
        self.assertEqual(1, len(nodes))
        self.assertEqual(TextNode("This node does not contain a delimiter",TextType.TEXT), nodes[0])

    def test_other_text_types_unmodified(self):
        nodes = split_nodes_delimiter([TextNode("This node does _contain_ a delimiter", TextType.BOLD)], "_", TextType.ITALIC)
        self.assertEqual(1, len(nodes))
        self.assertEqual(TextNode("This node does _contain_ a delimiter", TextType.BOLD), nodes[0])

    def test_text_into_italic(self):
        nodes = split_nodes_delimiter([TextNode("This node does _contain_ a delimiter", TextType.TEXT)], "_", TextType.ITALIC)
        self.assertEqual(3, len(nodes))
        self.assertEqual(TextNode("This node does ", TextType.TEXT), nodes[0])
        self.assertEqual(TextNode("contain",TextType.ITALIC), nodes[1])
        self.assertEqual(TextNode(" a delimiter", TextType.TEXT), nodes[2])


    def test_text_into_bold(self):
        nodes = split_nodes_delimiter([TextNode("This node does **contain** a delimiter", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(3, len(nodes))
        self.assertEqual(TextNode("This node does ", TextType.TEXT), nodes[0])
        self.assertEqual(TextNode("contain",TextType.BOLD), nodes[1])
        self.assertEqual(TextNode(" a delimiter", TextType.TEXT), nodes[2])

    def test_text_starts_with_delimiter(self):
        nodes = split_nodes_delimiter([TextNode("**Bold** text first", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(2, len(nodes))
        self.assertEqual(TextNode("Bold", TextType.BOLD), nodes[0])
        self.assertEqual(TextNode(" text first", TextType.TEXT), nodes[1])

    def test_text_ends_with_delimiter(self):
        nodes = split_nodes_delimiter([TextNode("The last word is **Bold**", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(2, len(nodes))
        self.assertEqual(TextNode("The last word is ", TextType.TEXT), nodes[0])
        self.assertEqual(TextNode("Bold", TextType.BOLD), nodes[1])

    def test_text_starts_and_ends_width_delimiter(self):
        nodes = split_nodes_delimiter([TextNode("**This text is Bold**", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(1, len(nodes))
        self.assertEqual(TextNode("This text is Bold", TextType.BOLD), nodes[0])

    def test_multiple_identical_delimiters(self):
        nodes = split_nodes_delimiter([TextNode("**This** text contains **Bold** parts", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(4, len(nodes))
        self.assertEqual(TextNode("This", TextType.BOLD), nodes[0])
        self.assertEqual(TextNode(" text contains ", TextType.TEXT), nodes[1])
        self.assertEqual(TextNode("Bold", TextType.BOLD), nodes[2])
        self.assertEqual(TextNode(" parts", TextType.TEXT), nodes[3])

    def test_multiple_different_delimiters(self):
        nodes = split_nodes_delimiter([TextNode("**This** text contains _Italic_ parts", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(2, len(nodes))
        self.assertEqual(TextNode("This", TextType.BOLD), nodes[0])
        self.assertEqual(TextNode(" text contains _Italic_ parts", TextType.TEXT), nodes[1])

        nodes2 = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(4, len(nodes2))
        self.assertEqual(TextNode("This", TextType.BOLD), nodes2[0])
        self.assertEqual(TextNode(" text contains ", TextType.TEXT), nodes2[1])
        self.assertEqual(TextNode("Italic", TextType.ITALIC), nodes2[2])
        self.assertEqual(TextNode(" parts", TextType.TEXT), nodes2[3])

    def test_unterminated_delimiters_raise(self):
        with self.assertRaises(Exception) as context:
            nodes = split_nodes_delimiter([TextNode("This contains **unterminated delimiters",TextType.TEXT)], "**", TextType.BOLD)

        self.assertIsInstance(context.exception, SyntaxError)
        self.assertEqual("SyntaxError: Delimiter '**' was never closed", str(context.exception))


if __name__ == "__main__":
    unittest.main()

