from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from typing import Any



def extract_title(markdown: str) -> str | Any:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            return block.lstrip("#").strip()

    raise Exception("Missing Header/Title")



