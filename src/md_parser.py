import re
from textnode import TextNode, TextType


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
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        old_text = old_node.text
        old_type = old_node.text_type
        index = 0
        for text, url in links:
            link_text = f"[{text}]({url})"
            link_index = old_text.find(link_text, index)
            if (link_index - index) > 0:
                new_nodes.append(TextNode(old_text[index:link_index], old_type))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            index = link_index + len(link_text)
        if old_text[index:] != "":
            new_nodes.append(TextNode(old_text[index:], old_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_images(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        old_text = old_node.text
        old_type = old_node.text_type
        index = 0
        for text, url in links:
            link_text = f"![{text}]({url})"
            link_index = old_text.find(link_text, index)
            if (link_index - index) > 0:
                new_nodes.append(TextNode(old_text[index:link_index], old_type))
            new_nodes.append(TextNode(text, TextType.IMAGE, url))
            index = link_index + len(link_text)
        if old_text[index:] != "":
            new_nodes.append(TextNode(old_text[index:], old_type))
    return new_nodes

def extract_markdown_images(text : str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text : str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


