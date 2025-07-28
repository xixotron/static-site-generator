import unittest

from md_parser import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link

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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_Extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            extract_markdown_images(text))

    def test_extract_only_images(self):
        text = "This is text with a image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ],
            extract_markdown_images(text))


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_Extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            extract_markdown_links(text))

    def test_extract_only_links(self):
        text = "This is text with a image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            [
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text))


class TestSplitNodesLink(unittest.TestCase):
    def test_unmodified_text_without_links(self):
        text_node = TextNode("This text contains no links", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text contains no links", TextType.TEXT)
            ],
            split_nodes_link([text_node])
        )

    def test_extract_one_link(self):
        text_node = TextNode("This text contains [one](url.link) link", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text contains ", TextType.TEXT),
                TextNode("one", TextType.LINK, "url.link"),
                TextNode(" link", TextType.TEXT)
            ],
            split_nodes_link([text_node])
        )

    def test_extract_two_different_links(self):
        text_node = TextNode("This text contains [one](url.link) link [or more](https://google.com)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text contains ", TextType.TEXT),
                TextNode("one", TextType.LINK, "url.link"),
                TextNode(" link ", TextType.TEXT),
                TextNode("or more", TextType.LINK, "https://google.com"),
            ],
            split_nodes_link([text_node])
        )

    def test_extract_all_text_as_link(self):
        text_node = TextNode("[this is a single link](https://www.freecatphotoapp.com/)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("this is a single link", TextType.LINK, "https://www.freecatphotoapp.com/"),
            ],
            split_nodes_link([text_node])
        )

    def test_extract_same_link_multiple_times(self):
        text_node = TextNode("This text's [link](https://www.google.com/search?q=recursion) is a recursive [link](https://www.google.com/search?q=recursion)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text's ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com/search?q=recursion"),
                TextNode(" is a recursive ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com/search?q=recursion"),
            ],
            split_nodes_link([text_node])
        )

    def test_extract_one_link_ignore_images(self):
        text_node = TextNode("This text contains ![one](url.image) image [or more](https://google.com)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text contains ![one](url.image) image ", TextType.TEXT),
                TextNode("or more", TextType.LINK, "https://google.com"),
            ],
            split_nodes_link([text_node])
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_unmodified_text_without_images(self):
        text_node = TextNode("This text contains no links", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text contains no links", TextType.TEXT)
            ],
            split_nodes_image([text_node])
        )

    def test_extract_one_image(self):
        text_node = TextNode("This text contains ![one](url.image) image", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text contains ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url.image"),
                TextNode(" image", TextType.TEXT)
            ],
            split_nodes_image([text_node])
        )

    def test_extract_two_different_images(self):
        text_node = TextNode("This text contains ![one](url.image) image ![or more](https://google.com)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text contains ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url.image"),
                TextNode(" image ", TextType.TEXT),
                TextNode("or more", TextType.IMAGE, "https://google.com"),
            ],
            split_nodes_image([text_node])
        )

    def test_extract_all_text_as_image(self):
        text_node = TextNode("![this is a single image](https://s3.amazonaws.com/freecodecamp/running-cats.jpg)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("this is a single image", TextType.IMAGE, "https://s3.amazonaws.com/freecodecamp/running-cats.jpg"),
            ],
            split_nodes_image([text_node])
        )

    def test_extract_same_image_multiple_times(self):
        text_node = TextNode("This text's ![image](https://imgs.xkcd.com/comics/loop.png) is a loop ![image](https://imgs.xkcd.com/comics/loop.png)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text's ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://imgs.xkcd.com/comics/loop.png"),
                TextNode(" is a loop ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://imgs.xkcd.com/comics/loop.png"),
            ],
            split_nodes_image([text_node])
        )

    def test_extract_one_image_ignore_link(self):
        text_node = TextNode("This text contains ![one](url.image) image [or more](https://google.com)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This text contains ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url.image"),
                TextNode(" image [or more](https://google.com)", TextType.TEXT),
            ],
            split_nodes_image([text_node])
        )


if __name__ == "__main__":
    unittest.main()

