"""
Lesson 3: Sentence-based chunking.

Step 1: split the text into sentences.
Step 2: pack whole sentences into a chunk until max_chars would be exceeded.
Optional: repeat the last N sentences in the next chunk (sentence overlap).

A sentence is never cut in half, so "Do not use if eGFR is below 30." stays whole.

Run:  python 03_sentence_chunker.py      (standard library only, no installs)
"""

import re

# Abbreviations that end with a period but do NOT end a sentence.
ABBREVIATIONS = {"dr", "mr", "mrs", "ms", "prof", "e.g", "i.e", "vs", "approx", "fig", "no"}

SAMPLE_TEXT = (
    "Metformin 500mg twice daily. Do not use if eGFR is below 30. "
    "Dr. Rao advised checking renal function every 3 months. "
    "Stop the drug before contrast imaging. "
    "Restart after 48 hours if kidney function is stable."
)


# ---------------------------------------------------------------------------
# Step 1: sentence splitting
# ---------------------------------------------------------------------------

def split_sentences_naive(text: str) -> list[str]:
    """Split after . ! ? followed by whitespace. Simple, but breaks on 'Dr. Rao'."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def split_sentences(text: str) -> list[str]:
    """Naive split, then glue back pieces that ended on a known abbreviation."""
    sentences = []
    for part in split_sentences_naive(text):
        if sentences:
            last_word = sentences[-1].split()[-1].rstrip(".").lower()
            if sentences[-1].endswith(".") and last_word in ABBREVIATIONS:
                sentences[-1] = f"{sentences[-1]} {part}"
                continue
        sentences.append(part)
    return sentences


# ---------------------------------------------------------------------------
# Step 2: pack sentences into chunks
# ---------------------------------------------------------------------------

def sentence_chunks(text: str, max_chars: int = 200, overlap_sentences: int = 0) -> list[str]:
    """Group whole sentences into chunks of at most ~max_chars characters.

    A single sentence longer than max_chars becomes its own (oversized) chunk.
    """
    chunks = []
    current: list[str] = []

    for sentence in split_sentences(text):
        candidate = " ".join(current + [sentence])

        if current and len(candidate) > max_chars:
            chunks.append(" ".join(current))
            # start the next chunk with the last N sentences (overlap)
            current = current[-overlap_sentences:] if overlap_sentences else []
            # drop the overlap if it would make the new chunk too big already
            if len(" ".join(current + [sentence])) > max_chars:
                current = []

        current.append(sentence)

    if current:
        chunks.append(" ".join(current))
    return chunks


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    print(f"\n{'=' * 8} {title} {'=' * 8}")


def print_chunks(chunks: list[str]) -> None:
    for number, chunk in enumerate(chunks):
        print(f"{number}  ({len(chunk):>3} chars)  {chunk!r}")


if __name__ == "__main__":
    print_header("Naive split (note the wrong split at 'Dr.')")
    for s in split_sentences_naive(SAMPLE_TEXT):
        print(" -", s)

    print_header("Split with abbreviation handling")
    for s in split_sentences(SAMPLE_TEXT):
        print(" -", s)

    print_header("Chunks: max 100 chars, no overlap")
    print_chunks(sentence_chunks(SAMPLE_TEXT, max_chars=100))

    print_header("Chunks: max 100 chars, 1 sentence overlap")
    print_chunks(sentence_chunks(SAMPLE_TEXT, max_chars=100, overlap_sentences=1))