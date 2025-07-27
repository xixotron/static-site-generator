from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    TEXT    = "text"
    BOLD    = "bold"
    ITALIC  = "italic"
    CODE    = "code"
    LINK    = "link"
    IMAGE   = "image"

class TextNode:
    def __init__(self, text : str, text_type : TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            # isinstance(other, TextNode)
            self.text_type == other.text_type
            and self.url == other.url
            and self.text == other.text
        )

    def __repr__(self) -> str:
        return (
            "TextNode("
            f"text={repr(self.text)}, "
            f"text_type={repr(self.text_type.value)}, "
            f"url={repr(self.url) if self.url else None})"
        )


def text_node_to_html_node(text_node : TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text,{"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt" : text_node.text})
        case _:
            raise TypeError("Unknow TextType in LeafNode")
