"""
Lesson 1: Fixed-size chunking.

Two ways to cut text into equal pieces:
  A) by characters  - simple, easy to reason about
  B) by tokens      - matches what embedding models / LLMs actually count

Both ignore meaning, so they can cut words, sentences and tables in half.
Use them as a baseline to compare better strategies against.

Setup:  pip install tiktoken
Run:    python chunker.py
"""

import tiktoken

# cl100k_base is the tokenizer used by OpenAI's GPT-4 / text-embedding-3 models.
ENCODING_NAME = "cl100k_base"
SAMPLE_TEXT = "Metformin 500mg twice daily. Do not use if eGFR is below 30."


# ---------------------------------------------------------------------------
# Chunkers
# ---------------------------------------------------------------------------

def fixed_size_chunks(text: str, chunk_size: int = 500) -> list[str]:
    """Split text into pieces of `chunk_size` characters (last piece may be shorter)."""
    chunks = []
    for start in range(0, len(text), chunk_size):
        chunks.append(text[start : start + chunk_size])
    return chunks


def fixed_token_chunks(text: str, chunk_tokens: int = 200) -> list[str]:
    """Split text into pieces of `chunk_tokens` tokens (last piece may be shorter)."""
    enc = tiktoken.get_encoding(ENCODING_NAME)
    tokens = enc.encode(text)

    chunks = []
    for start in range(0, len(tokens), chunk_tokens):
        chunks.append(enc.decode(tokens[start : start + chunk_tokens]))
    return chunks


# ---------------------------------------------------------------------------
# Helpers for printing (so the demo below stays easy to read)
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    print(f"\n{'=' * 8} {title} {'=' * 8}")


def print_chunks(chunks: list[str]) -> None:
    for number, chunk in enumerate(chunks):
        print(f"{number}  ({len(chunk):>2} chars)  {chunk!r}")


def print_token_breakdown(text: str) -> None:
    """Show every token on its own line: position, token id, and the text it covers."""
    enc = tiktoken.get_encoding(ENCODING_NAME)
    token_ids = enc.encode(text)

    print(f"total tokens: {len(token_ids)}")
    for position, token_id in enumerate(token_ids):
        print(f"{position:>2}  id={token_id:<6}  {enc.decode([token_id])!r}")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Text: {SAMPLE_TEXT!r}")

    print_header("Version A: characters (size 20)")
    print_chunks(fixed_size_chunks(SAMPLE_TEXT, chunk_size=20))

    print_header("Version B: tokens (size 5)")
    print_chunks(fixed_token_chunks(SAMPLE_TEXT, chunk_tokens=5))

    print_header("Token breakdown (why 5 tokens != 5 characters)")
    print_token_breakdown(SAMPLE_TEXT)