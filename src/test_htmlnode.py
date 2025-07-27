import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
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
        node = HTMLNode(children=["div","p"])
        self.assertEqual("HTMLNode(tag=None, value=None, children=['div', 'p'], props=None)",repr(node))


    def test_props_repr(self):
        node = HTMLNode(props={"href": "boot.dev", "target": "_blank"})
        self.assertEqual(
            "HTMLNode(tag=None, value=None, children=None, props={'href': 'boot.dev', 'target': '_blank'})",
            repr(node))


if __name__ == "__main__":
    unittest.main()

