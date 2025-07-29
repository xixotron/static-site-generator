

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        if block in ("", "\n"):
            continue
        blocks.append(block.strip())
    return blocks


