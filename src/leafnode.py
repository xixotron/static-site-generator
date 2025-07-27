from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag : str|None, value : str, props : dict|None=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={repr(self.tag) if self.tag else None}, value={repr(self.value)}, props={repr(self.props) if self.props else None})"
