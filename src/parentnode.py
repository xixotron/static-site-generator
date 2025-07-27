from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag : str, children : list[HTMLNode], props : dict|None=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("invalid HTML: no tag")

        if not self.children:
            raise ValueError("invalid HTML: no children")

        children_html = []
        for children in self.children:
            children_html.append(children.to_html())

        return f"<{self.tag}{self.props_to_html()}>{"".join(children_html)}</{self.tag}>"

    def __repr__(self):
        return (
            "ParentNode("
            f"tag={repr(self.tag) if self.tag else None}, "
            f"children={repr(self.children) if self.children else None}, "
            f"props={repr(self.props) if self.props else None})"
        )
