import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()

