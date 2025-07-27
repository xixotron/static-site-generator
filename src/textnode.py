from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_FORMAT = "link"
    IMAGE_FORMAT = "image"

class TextNode:
    def __init__(self, text : str, text_type : TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        if self.text != other.text:
            return False
        return True

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

