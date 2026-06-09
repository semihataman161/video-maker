import re


def parse_chunks(text: str):
    lines = text.strip().split("\n")
    chunks = []

    for line in lines:
        match = re.match(r"^\[(\d+)\]\s*(.*)", line)
        if match:
            chunk = match.group(2).strip()
            if chunk:
                chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No chunks parsed!")

    return chunks


def split_sentences(text: str) -> list[str]:
    sentences = re.findall(r'(?:.*?[.?!]"?\s)|(?:.+$)', text)
    return [s.strip() for s in sentences if s.strip()]
