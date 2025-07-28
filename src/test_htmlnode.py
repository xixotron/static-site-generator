import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())
        node = HTMLNode(props={})
        self.assertEqual("", node.props_to_html())

    def test_single_props_to_html(self):
        node = HTMLNode(props={"href" : "boot.dev"})
        self.assertEqual(' href="boot.dev"', node.props_to_html())
        node = HTMLNode(props={"target" : "_blank"})
        self.assertEqual(' target="_blank"', node.props_to_html())

    def test_multiple_props_to_html(self):
        node = HTMLNode(props={"href": "boot.dev", "target": "_blank"})
        self.assertEqual(' href="boot.dev" target="_blank"', node.props_to_html())

    def test_empty_repr(self):
        node = HTMLNode()
        self.assertEqual("HTMLNode(tag=None, value=None, children=None, props=None)",repr(node))

    def test_tag_repr(self):
        node = HTMLNode("a")
        self.assertEqual("HTMLNode(tag='a', value=None, children=None, props=None)",repr(node))

    def test_value_repr(self):
        node = HTMLNode(value="Hello HTML!")
        self.assertEqual("HTMLNode(tag=None, value='Hello HTML!', children=None, props=None)",repr(node))

    def test_children_repr(self):
        node = HTMLNode(children=[None, None]) # type: ignore
        self.assertEqual("HTMLNode(tag=None, value=None, children=[None, None], props=None)",repr(node))


    def test_props_repr(self):
        node = HTMLNode(props={"href": "boot.dev", "target": "_blank"})
        self.assertEqual(
            "HTMLNode(tag=None, value=None, children=None, props={'href': 'boot.dev', 'target': '_blank'})",
            repr(node))


class TestLeafNode(unittest.TestCase):
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


class TestParentNode(unittest.TestCase):
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

