import re
from enum import Enum


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

# assert block_to_block_type("# Title") == BlockType.HEADING
# assert block_to_block_type("####### too many") == BlockType.PARAGRAPH
# assert block_to_block_type("###NoSpace") == BlockType.PARAGRAPH
#
# assert block_to_block_type("```\ncode\n```") == BlockType.CODE
#
# assert block_to_block_type("> a\n> b") == BlockType.QUOTE
# assert block_to_block_type("> a\nb") == BlockType.PARAGRAPH
#
# assert block_to_block_type("- a\n- b") == BlockType.UNORDERED_LIST
# assert block_to_block_type("-a") == BlockType.PARAGRAPH
#
# assert block_to_block_type("1. a\n2. b\n3. c") == BlockType.ORDERED_LIST
# assert block_to_block_type("2. a\n3. b") == BlockType.PARAGRAPH
# assert block_to_block_type("1. a\n3. b") == BlockType.PARAGRAPH