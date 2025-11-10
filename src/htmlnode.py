from __future__ import annotations


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html


    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


def text_node_to_html(text_node):
    print(text_node)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
       super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        
        elif self.tag is None:
            return f"{self.value}"
    
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Cannot render an HTMLNode without a tag.")
        
        elif self.children is None:
            raise ValueError("Missing Children")
        
        output = f"<{self.tag}{self.props_to_html()}>"
        count = 0
        while count != len(self.children):
            output += self.children[count].to_html()
            count += 1
        
        output += f"</{self.tag}>"

        return output

