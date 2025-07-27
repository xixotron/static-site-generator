import unittest

from htmlnode import LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_to_html_single_child(self):
        node = ParentNode("p", [LeafNode("","text")])
        self.assertEqual("<p>text</p>", node.to_html())

    def test_to_html_multiple_child(self):
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text")
            ])
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
            node.to_html())

    def test_to_html_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode("span", [LeafNode("p", "Normal Text"), LeafNode("b","Bold Text")]),
                LeafNode("i", "Italic Text")
            ])
        self.assertEqual(
            "<div><span><p>Normal Text</p><b>Bold Text</b></span><i>Italic Text</i></div>",
            node.to_html())

    def test_to_html_props(self):
        node = ParentNode("p", [LeafNode(None, "text")], {"color" : "red"})
        self.assertEqual('<p color="red">text</p>', node.to_html())

    def test_to_html_no_child_raises(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("invalid HTML: no children" in str(context.exception))

    def test_to_html_no_tag_raises(self):
        node = ParentNode("", [LeafNode("","text")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("invalid HTML: no tag" in str(context.exception))

if __name__ == "__main__":
    unittest.main()

