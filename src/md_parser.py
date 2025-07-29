import re

from textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes : list[TextNode], delimiter : str, text_type : TextType) -> list[TextNode]:
    new_nodes =[]
    for node in old_nodes:
        if delimiter not in node.text or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise SyntaxError(f"SyntaxError: Delimiter '{delimiter}' was never closed")

        strings = node.text.split(delimiter)
        for i, string in enumerate(strings):
            if string == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(string, TextType.TEXT))
            else:
                new_nodes.append(TextNode(string, text_type))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        old_text = old_node.text
        links = extract_markdown_links(old_text)
        if not links:
            new_nodes.append(old_node)
            continue

        index = 0
        for text, url in links:
            link_text = f"[{text}]({url})"
            link_index = old_text.find(link_text, index)
            if (link_index - index) > 0:
                new_nodes.append(TextNode(old_text[index:link_index], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            index = link_index + len(link_text)
        if old_text[index:] != "":
            new_nodes.append(TextNode(old_text[index:], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        old_text = old_node.text
        images = extract_markdown_images(old_text)
        if not images:
            new_nodes.append(old_node)
            continue

        index = 0
        for text, url in images:
            link_text = f"![{text}]({url})"
            link_index = old_text.find(link_text, index)
            if (link_index - index) > 0:
                new_nodes.append(TextNode(old_text[index:link_index], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.IMAGE, url))
            index = link_index + len(link_text)
        if old_text[index:] != "":
            new_nodes.append(TextNode(old_text[index:], TextType.TEXT))
    return new_nodes


def extract_markdown_images(text : str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text : str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

