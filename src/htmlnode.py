from __future__ import annotations


class HTMLNode:
    def __init__(self,
                 tag : str|None=None,
                 value: str|None=None,
                 children: list[HTMLNode]|None=None,
                 props : dict[str, str]|None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(f"{self.__class__.__name__}.to_html method is not implemented")

    def props_to_html(self):
        if not self.props:
            return ""

        properties = []
        for prop, val in self.props.items():
            properties.append(f' {prop}="{val}"')
        return "".join(properties)

    def __repr__(self):
        string = (
            "HTMLNode("
            f"tag={repr(self.tag) if self.tag else None}, "
            f"value={repr(self.value) if self.value else None}, "
            f"children={repr(self.children) if self.children else None}, "
            f"props={repr(self.props) if self.props else None})"
        )
        return string


class LeafNode(HTMLNode):
    def __init__(self, tag : str|None, value : str, props : dict|None=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={repr(self.tag) if self.tag else None}, value={repr(self.value)}, props={repr(self.props) if self.props else None})"


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


