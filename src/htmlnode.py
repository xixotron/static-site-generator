
class HTMLNode:
    def __init__(self,
                 tag : str|None=None,
                 value: str|None=None,
                 children: list|None=None,
                 props : dict|None=None):
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
