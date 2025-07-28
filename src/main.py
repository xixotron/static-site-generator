from textnode import *
from md_parser import split_nodes_delimiter

def main():

    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    text_node = TextNode("This is a _italic_ text with a `code block` in between", TextType.TEXT)
    nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    print(nodes)

if __name__ == "__main__":
    main()
    print("hello world")
