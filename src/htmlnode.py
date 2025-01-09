class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        props_string = ""
        for prop in self.props:
            props_string = props_string + f' {prop}="{self.props[prop]}"'
        return props_string
    
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag} value:{self.value} children:{self.children} props:{self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No Value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no parent tag")
        if self.children == None:
            raise ValueError("no children")
        between_tags = ""
        for child in self.children:
            between_tags = between_tags + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{between_tags}</{self.tag}>"