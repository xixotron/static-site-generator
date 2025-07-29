import re

from enum import Enum


class BlockType(Enum):
    PARAGRAPH       = "paragraph"
    HEADING         = "heading"
    CODE            = "code"
    QUOTE           = "quote"
    UNORDERED_LIST  = "unordered_list"
    ORDERED_LIST    = "ordered_list"


def block_to_block_type(block: str) ->BlockType:
    matches = re.fullmatch(r"^#{1,6} [^\n]*$", block)
    if matches:
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    is_quote_block = True
    is_unordered_block = True
    is_ordered_block = True
    for i, line in enumerate(block.split("\n")):
        numeral = f"{i + 1}."

        is_quote_block =  is_quote_block and line.startswith("> ")
        is_unordered_block = is_unordered_block and line.startswith("- ")
        is_ordered_block = is_ordered_block and line.startswith(numeral)

        if not (is_quote_block or is_unordered_block or is_ordered_block):
            return BlockType.PARAGRAPH

    if is_quote_block:
        return BlockType.QUOTE
    if is_unordered_block:
        return BlockType.UNORDERED_LIST
    if is_ordered_block:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH



def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        if block in ("", "\n"):
            continue
        blocks.append(block.strip())
    return blocks


