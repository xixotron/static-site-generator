import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node1, node2)

        node3 = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        node4 = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node3, node4)

        node5 = TextNode("", TextType.IMAGE, "https://youtu.be/dQw4w9WgXcQ")
        node6 = TextNode("", TextType.IMAGE, "https://youtu.be/dQw4w9WgXcQ")
        self.assertEqual(node5, node6)

    def test_neq(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node1, node2)

        node3 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)

        node5 = TextNode("This is a text node", TextType.TEXT)
        node6 = TextNode("This is a text node", TextType.TEXT, "httsp://boot.dev")
        self.assertNotEqual(node5, node6)

        node7 = TextNode("This is a text node", TextType.TEXT, "https://youtu.be/dQw4w9WgXcQ")
        node8 = TextNode("This is a text node", TextType.TEXT, "httsp://boot.dev")
        self.assertNotEqual(node7, node8)

    def test_repr(self):
        expected1 = "TextNode(This is a TextNode, text, None)"
        node1 = TextNode("This is a TextNode", TextType.TEXT) 
        repr1 = repr(node1)
        self.assertEqual(expected1, repr1)

        expected2 = "TextNode(This is a TextNode, link, https://boot.dev)"
        node2 = TextNode("This is a TextNode", TextType.LINK, "https://boot.dev")
        node_repr = repr(node2)
        self.assertEqual(expected2, node_repr)



if __name__ == "__main__":
    unittest.main()

