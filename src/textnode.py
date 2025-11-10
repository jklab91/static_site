from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        if not isinstance(text_type, TextType):
            raise TypeError("text_type must be an instance of TextType")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return (
            isinstance(node, TextNode)
            and self.text == node.text
            and self.text_type == node.text_type
            and self.url == node.url
    )    

    
    def __repr__(self):
        if self.url is not None:
            return f'TextNode("{self.text}", {self.text_type}, "{self.url}")'
        return f'TextNode("{self.text}", {self.text_type})'
    

def text_node_to_html_node(text_node):
        if not isinstance(text_node.text_type, TextType):
            raise TypeError("The nodes text type must bean instance of TextType")
        else:
            match text_node.text_type:
                case TextType.TEXT:
                    return LeafNode(tag=None, value=text_node.text)
                
            match text_node.text_type:
                case TextType.BOLD:
                    return LeafNode(tag="b", value=text_node.text)

            match text_node.text_type:
                case TextType.ITALIC:
                    return LeafNode(tag="i", value=text_node.text)
                
            match text_node.text_type:
                case TextType.CODE:
                    return LeafNode(tag="code", value=text_node.text)

            match text_node.text_type:
                case TextType.LINK:
                    return LeafNode(tag="a", value=text_node.text, props="href")

            match text_node.text_type:
                case TextType.IMAGE:
                    return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})




