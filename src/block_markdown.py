import re
from enum import Enum
from typing import Any

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType




def markdown_to_blocks(markdown: str):
    lines = markdown.splitlines()
    blocks = []
    current: list[str] = []

    for line in lines:
        if line.strip() == "":
            if current:
                blocks.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)

    if current:
        blocks.append("\n".join(current).strip())

    return blocks

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


def markdown_to_html_node(markdown):
    new_nodes: list[Any] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        # Paragraph Formatting
        if block_type == BlockType.PARAGRAPH:
            # Strip each line, then join with a single space
            paragraph_text = " ".join(line.strip() for line in block.splitlines())
            children = text_to_children(paragraph_text)
            new_nodes.append(ParentNode(tag="p", children=children))
        # Code Formatting
        elif block_type == BlockType.CODE:
            lines = block.splitlines()
            inner_lines = lines[1:-1]

            # Strip leading spaces from each inner line (tests expect no indentation)
            stripped_lines = [line.lstrip() for line in inner_lines]

            # Join with a newline *between* lines, and add a final newline
            inner_code = "\n".join(stripped_lines) + "\n"

            nd = TextNode(text=inner_code, text_type=TextType.CODE)
            code_html = text_node_to_html_node(nd)
            new_nodes.append(ParentNode(tag="pre", children=[code_html]))
        # Heading Formatting
        elif block_type == BlockType.HEADING:
            level = 0
            for i in block:
                if i == "#":
                    level += 1
                if i != "#":
                    break
            stripped = block[level:].lstrip()
            children = text_to_children(stripped)
            new_nodes.append(ParentNode(tag=f"h{level}", children=children, props=None))
        # Quote formatting
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                if line.startswith(">"):
                    line = line[1:]
                    if line.startswith(" "):
                        line = line[1:]
                stripped_lines.append(line)

            formatted = "\n".join(stripped_lines).strip()
            new_nodes.append(
                ParentNode(
                    tag="blockquote",
                    children=text_to_children(formatted),
                    props=None,
                )
            )
        # UOList formatting
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                line = line.strip()
                if line.startswith("- "):
                    item_text = line[2:]
                elif line.startswith("* "):
                    item_text = line[2:]
                else:
                    continue
                children = text_to_children(item_text)
                li_nodes.append(
                    ParentNode(
                        tag="li",
                        children=children,
                        props=None,
                    )
                )
            new_nodes.append(
                ParentNode(
                    tag="ul",
                    children=li_nodes,
                    props=None,
                )
            )

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            oli_nodes = []
            for line in lines:
                line = line.strip()
                if "." in line:
                    prefix, rest = line.split(".", 1)
                    if prefix.isdigit():
                        item_text = rest.lstrip()  # remove the space after "1."
                    else:
                        continue  # skip malformed lines
                    children = text_to_children(item_text)

                    oli_nodes.append(
                        ParentNode(
                            tag="li",
                            children=children,
                            props=None,
                        )
                    )
            new_nodes.append(
                ParentNode(
                    tag="ol",
                    children=oli_nodes,
                    props=None,
                )
            )





    return ParentNode(tag="div", children=new_nodes)

