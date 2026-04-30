import re


def parse_chunks(text: str):
    lines = text.strip().split("\n")
    chunks = []

    for line in lines:
        match = re.match(r"^\d+\)\s*(.*)", line)
        if match:
            chunk = match.group(1).strip()
            if chunk:
                chunks.append(chunk)

    if not chunks:
        raise ValueError("No chunks parsed from LLM output")

    return chunks
