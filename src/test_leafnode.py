import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is only text")
        self.assertEqual("This is only text", node.to_html())

    def test_to_html_p(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual("<p>This is a paragraph</p>", node.to_html())

    def test_to_html_a(self):
        node = LeafNode("a", "This is a link", {"href":"https://boot.dev"})
        self.assertEqual('<a href="https://boot.dev">This is a link</a>', node.to_html())

    def test_to_html_no_value_Exception(self):

        node = LeafNode("p", None)  # type:ignore value should be a str
        with self.assertRaises(ValueError) as context:
            html = node.to_html()
            self.assertIsNone(html)

        self.assertNotIn("html", locals())
        self.assertTrue("invalid HTML: no value" in str(context.exception))


if __name__ == "__main__":
    unittest.main()

