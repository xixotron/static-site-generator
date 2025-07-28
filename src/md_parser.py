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
            new_nodes.append(TextNode(string, node.text_type if (i % 2 == 0) else text_type))

    return new_nodes


