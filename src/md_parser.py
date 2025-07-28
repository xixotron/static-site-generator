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

def extract_markdown_images(text : str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text : str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches
