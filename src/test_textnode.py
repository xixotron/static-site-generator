import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq_text_and_type(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_eq_links(self):
        node1 = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node1, node2)

    def test_eq_empty_text_with_links(self):
        node1 = TextNode("", TextType.IMAGE, "https://youtu.be/dQw4w9WgXcQ")
        node2 = TextNode("", TextType.IMAGE, "https://youtu.be/dQw4w9WgXcQ")
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_neq_text_type(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_neq_empty_link(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, "httsp://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_neq_links(self):
        node1 = TextNode("This is a text node", TextType.TEXT, "https://youtu.be/dQw4w9WgXcQ")
        node2 = TextNode("This is a text node", TextType.TEXT, "httsp://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_repr_text_and_type(self):
        node = TextNode("This is a TextNode", TextType.TEXT) 
        self.assertEqual("TextNode(text='This is a TextNode', text_type='text', url=None)", repr(node))

    def test_repr_all(self):
        node = TextNode("This is a TextNode", TextType.LINK, "https://boot.dev")
        self.assertEqual("TextNode(text='This is a TextNode', text_type='link', url='https://boot.dev')", repr(node))


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_return_type(self):
        text_node = TextNode("This is a text Node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)

    def test_text_to_html(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(None, html_node.tag)
        self.assertEqual("This is a text node", html_node.value)

    def test_bold_to_html(self):
        text_node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual("b", html_node.tag)
        self.assertEqual("This is a bold text node", html_node.value)

    def test_italic_to_html(self):
        text_node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual("i", html_node.tag)
        self.assertEqual("This is a italic text node", html_node.value)

    def test_code_to_html(self):
        text_node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual("code", html_node.tag)
        self.assertEqual("This is a code text node", html_node.value)

    def test_link_to_html(self):
        text_node = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual("a", html_node.tag)
        self.assertIsNotNone(html_node.props)
        self.assertDictEqual({"href" : "https://boot.dev"}, html_node.props or {})
        self.assertEqual("This is a link node", html_node.value)

    def test_image_to_html(self):
        text_node = TextNode("This is a image node", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual("img", html_node.tag)
        self.assertIsNotNone(html_node.props)
        self.assertDictEqual({"src" : "https://boot.dev", "alt": "This is a image node"}, html_node.props or {})



if __name__ == "__main__":
    unittest.main()

