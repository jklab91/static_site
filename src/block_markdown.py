import re
from enum import Enum
from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType



def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


_HEADING_RE = re.compile(r"^(#{1,6})\s+\S")  # 1–6 #, followed by space, then some text
# For “every line …” patterns we validate all lines
_QUOTE_LINE_RE = re.compile(r"^>\s?.*$")     # allow "> " or ">"
_ULINE_RE = re.compile(r"^- .+$")            # "- " then something

def _is_code_block(block: str) -> bool:
    # Fence must start and end the block
    return block.startswith("```") and block.endswith("```")

def _is_heading(block: str) -> bool:
    # Single-line heading (spec implies a single heading line)
    return _HEADING_RE.match(block) is not None and "\n" not in block

def _is_quote_block(block: str) -> bool:
    return all(_QUOTE_LINE_RE.match(line) for line in block.splitlines())

def _is_unordered_list(block: str) -> bool:
    lines = block.splitlines()
    return len(lines) > 0 and all(_ULINE_RE.match(line) for line in lines)

def _is_ordered_list(block: str) -> bool:
    lines = block.splitlines()
    if not lines:
        return False
    # Must start at 1 and increment by 1; require a space after the dot
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            return False
    return True

def block_to_block_type(markdown_block: str) -> BlockType:
    # Order matters: code first so fenced code isn’t misclassified
    if _is_code_block(markdown_block):
        return BlockType.CODE
    if _is_heading(markdown_block):
        return BlockType.HEADING
    if _is_quote_block(markdown_block):
        return BlockType.QUOTE
    if _is_unordered_list(markdown_block):
        return BlockType.UNORDERED_LIST
    if _is_ordered_list(markdown_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

#todo Finish Quote, Ordered list, and Unordered List


def markdown_to_html_node(markdown):
    new_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        # Paragraph Formatting
        if block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(block.splitlines())
            children = text_to_children(paragraph_text)
            new_nodes.append(HTMLNode(tag="p", value=None, children=children, props=None))
        # Code Formatting
        elif block_type == BlockType.CODE:
            lines = block.splitlines()
            inner_lines = lines[1:-1]
            inner_code = "\n".join(inner_lines)
            nd = TextNode(text=inner_code, text_type=TextType.CODE)
            code_html = text_node_to_html_node(nd)
            new_nodes.append(HTMLNode(tag="pre", value=None, children=[code_html], props=None))
        # Heading Formatting
        elif block_type == BlockType.HEADING:
            level = 0
            for i in block:
                if i == "#":
                    level += 1
                if i != "#":
                    break
            stripped = block[level:].lstrip()
            print(stripped)
            children = text_to_children(stripped)
            new_nodes.append(HTMLNode(tag=f"h{level}", value=None, children=children, props=None))







    return HTMLNode(tag="div", children=new_nodes)

md_heading = "###### Smallest heading"
node = markdown_to_html_node(md_heading)
print(repr(node))


