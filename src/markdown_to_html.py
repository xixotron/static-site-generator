from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from md_parser import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


    # PARAGRAPH       = "paragraph"
    # HEADING         = "heading"
    # CODE            = "code"
    # QUOTE           = "quote"
    # UNORDERED_LIST  = "unordered_list"
    # ORDERED_LIST    = "ordered_list"

def markdown_to_html_node(markdown : str) -> HTMLNode:
    html_nodes = []

    for md_block in markdown_to_blocks(markdown):
        match block_to_block_type(md_block):

            case BlockType.HEADING:
                for line in md_block.split("\n"):
                    level, text = line.split(" ", 1)
                    text_nodes = text_to_textnodes(text)
                    html_nodes.append(
                        ParentNode(
                            f"h{len(level)}",
                            text_nodes_to_html_nodes(text_nodes)
                        )
                    )
            case BlockType.CODE:
                code_nodes = ParentNode("pre", [LeafNode("code", md_block.strip("```").lstrip())])
                html_nodes.append(code_nodes)

            case BlockType.QUOTE:
                lines = [line.strip("> ") for line in md_block.split("\n")]
                text_nodes = text_to_textnodes("\n".join(lines))
                html_nodes.append(
                    ParentNode("blockquote", [*text_nodes_to_html_nodes(text_nodes)])
                )

            case BlockType.UNORDERED_LIST:
                html_nodes.append(
                    ParentNode(
                        "ul",
                        markdown_list_block_to_HTMLNodes(md_block)
                    )
                )

            case BlockType.ORDERED_LIST:
                html_nodes.append(
                    ParentNode(
                        "ol",
                        markdown_list_block_to_HTMLNodes(md_block)
                    )
                )

            case BlockType.PARAGRAPH | _:
                text_nodes = text_to_textnodes(" ".join(md_block.split("\n")))
                paragraph = ParentNode("p", text_nodes_to_html_nodes(text_nodes))
                html_nodes.append(paragraph)

    return ParentNode("div", html_nodes) 

def markdown_list_block_to_HTMLNodes(markdown: str):
    list_items = []
    for line in markdown.split("\n"):
        text_start = line.find(" ")
        text_nodes = text_to_textnodes(line[text_start:].strip())

        list_item = ParentNode("li",
            text_nodes_to_html_nodes(text_nodes)
        )

        list_items.append(list_item)
    return list_items


def text_nodes_to_html_nodes(text_nodes: list[TextNode]) -> list[HTMLNode]:
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(
            text_node_to_html_node(text_node)
        )
    return html_nodes
