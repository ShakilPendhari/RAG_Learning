"""
Lesson 2: Fixed-size chunking WITH OVERLAP.

Same as Lesson 1, but each chunk repeats the tail of the previous one,
so text near a boundary appears in two chunks and is less likely to be lost.

    step = chunk_size - overlap      (how far the window moves each time)

Setup:  pip install tiktoken
Run:    python chunker.py
"""

import tiktoken

ENCODING_NAME = "cl100k_base"
SAMPLE_TEXT = "Metformin 500mg twice daily. Do not use if eGFR is below 30."


def overlap_chunks(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Split text into `chunk_size`-character pieces; each repeats `overlap` chars of the previous."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    step = chunk_size - overlap
    chunks = []
    for start in range(0, len(text), step):
        chunks.append(text[start : start + chunk_size])
        if start + chunk_size >= len(text):  # this chunk already reached the end
            break
    return chunks


def overlap_token_chunks(text: str, chunk_tokens: int = 200, overlap: int = 40) -> list[str]:
    """Same idea, but measured in tokens instead of characters."""
    if overlap >= chunk_tokens:
        raise ValueError("overlap must be smaller than chunk_tokens")

    enc = tiktoken.get_encoding(ENCODING_NAME)
    tokens = enc.encode(text)

    step = chunk_tokens - overlap
    chunks = []
    for start in range(0, len(tokens), step):
        chunks.append(enc.decode(tokens[start : start + chunk_tokens]))
        if start + chunk_tokens >= len(tokens):
            break
    return chunks


def overlap_token_chunks(text: str, chunk_tokens: int = 200, overlap: int = 40) -> list[str]:
    if overlap >= chunk_tokens:
        raise ValueError("Overlap must be smaller than chunk_tokens")

    enc = tiktoken.get_encoding(ENCODING_NAME)
    tokens = enc.encode(text)

    step - chunk_tokens - overlap
    chunks = []
    for start in range(0, len(tokens), step):
        chunks.append(enc.decode(tokens[start : start + chunk_tokens]))
        if start + chunk_tokens >= len(tokens):
            break
    return chunks


def print_header(title: str) -> None:
    print(f"\n{'=' * 8} {title} {'=' * 8}")


def print_chunks(chunks: list[str]) -> None:
    for number, chunk in enumerate(chunks):
        print(f"{number}  ({len(chunk):>2} chars)  {chunk!r}")


if __name__ == "__main__":
    print(f"Text: {SAMPLE_TEXT!r}")

    print_header("Characters: size 20, overlap 0 (Lesson 1)")
    print_chunks(overlap_chunks(SAMPLE_TEXT, chunk_size=20, overlap=0))

    print_header("Characters: size 20, overlap 8")
    print_chunks(overlap_chunks(SAMPLE_TEXT, chunk_size=20, overlap=8))

    print_header("Tokens: size 8, overlap 3")
    print_chunks(overlap_token_chunks(SAMPLE_TEXT, chunk_tokens=8, overlap=3))