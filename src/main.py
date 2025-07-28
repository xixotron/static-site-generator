from textnode import *
from md_parser import extract_markdown_links, split_nodes_delimiter, extract_markdown_images

def main():

    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    text_node = TextNode("This is a _italic_ text with a `code block` in between", TextType.TEXT)
    nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    print(nodes)
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_links(text))

if __name__ == "__main__":
    main()
    print("hello world")
