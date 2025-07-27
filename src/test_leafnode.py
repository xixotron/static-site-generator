import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_value_to_html(self):
        node = LeafNode(None, "This is only text")
        self.assertEqual("This is only text", node.to_html())

    def test_value_and_tag_to_html(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual("<p>This is a paragraph</p>", node.to_html())

    def test_value_tag_and_props_to_html(self):
        node = LeafNode("a", "This is a link", {"href":"https://boot.dev"})
        self.assertEqual('<a href="https://boot.dev">This is a link</a>', node.to_html())

    def test_to_html_empty_value_raisesError(self):

        node = LeafNode("p", None)  # type:ignore value should be a str
        with self.assertRaises(Exception) as context:
            html = node.to_html()
            self.assertIsNone(html)

        self.assertNotIn("html", locals())
        self.assertTrue("LeafNode" in str(context.exception))


if __name__ == "__main__":
    unittest.main()

