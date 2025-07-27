
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            properties = []
            for k, v in self.props.items():
                properties.append(f' {k}="{v}"')
            return "".join(properties)
        return ""

    def __repr__(self):
        attributes = []
        if self.tag:
            attributes.append(f"tag={self.tag}")
        if self.value:
            attributes.append(f"value={self.value}")
        if self.children:
            attributes.append(f"children={self.children}")
        if self.props:
            attributes.append(f"props={self.props}")

        return "HTMLNode(" + ", ".join(attributes) + ")"
