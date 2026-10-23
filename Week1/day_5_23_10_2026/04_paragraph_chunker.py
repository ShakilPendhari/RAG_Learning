"""
Lesson 4: Paragraph-based chunking.

Step 1: split the text on blank lines (paragraphs), and un-wrap hard line breaks
        (PDFs often break lines in the middle of a sentence).
Step 2: pack whole paragraphs into a chunk until max_chars would be exceeded.
Extras: a paragraph that is too long falls back to sentence splitting;
        tiny paragraphs (headings) are kept together with the paragraph after them.

Run:  python 04_paragraph_chunker.py      (standard library only, no installs)
"""

import re

SAMPLE_TEXT = """Metformin Protocol

Dosage

Start with 500mg twice daily with meals. Increase by 500mg every
week if tolerated. Maximum dose is 2000mg daily.

Contraindications

Do not use if eGFR is below 30. Stop before contrast imaging and
restart after 48 hours if kidney function is stable.

Monitoring

Check renal function every 3 months. Check vitamin B12 yearly."""

LONG_PARAGRAPH = (
    "Metformin lowers blood glucose mainly by reducing liver glucose output. "
    "It also improves insulin sensitivity in muscle. "
    "Common side effects are nausea and diarrhoea, which usually settle in two weeks. "
    "Take it with meals to reduce stomach upset."
)


# ---------------------------------------------------------------------------
# Step 1: paragraph splitting
# ---------------------------------------------------------------------------

def split_paragraphs(text: str) -> list[str]:
    """Split on blank lines, then turn remaining single line breaks into spaces."""
    paragraphs = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = re.sub(r"\s*\n\s*", " ", block).strip()  # un-wrap hard line breaks
        if block:
            paragraphs.append(block)
    return paragraphs


# ---------------------------------------------------------------------------
# Fallback: split a too-long paragraph by sentences
# ---------------------------------------------------------------------------

def split_long_paragraph(paragraph: str, max_chars: int) -> list[str]:
    """Pack sentences of one long paragraph into pieces of at most max_chars."""
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", paragraph) if s]
    pieces: list[str] = []
    current: list[str] = []
    for sentence in sentences:
        if current and len(" ".join(current + [sentence])) > max_chars:
            pieces.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        pieces.append(" ".join(current))
    return pieces


# ---------------------------------------------------------------------------
# Step 2: pack paragraphs into chunks
# ---------------------------------------------------------------------------

def paragraph_chunks(text: str, max_chars: int = 300, min_chars: int = 0) -> list[str]:
    """Group whole paragraphs into chunks of at most ~max_chars characters.

    min_chars: a paragraph shorter than this (like a heading) is never left at
               the END of a chunk; it moves to the start of the next chunk.
    """
    # 1) make sure no single unit is bigger than max_chars (fallback to sentences)
    units: list[str] = []
    for paragraph in split_paragraphs(text):
        if len(paragraph) > max_chars:
            units.extend(split_long_paragraph(paragraph, max_chars))
        else:
            units.append(paragraph)

    # 2) pack units into chunks
    chunks: list[str] = []
    current: list[str] = []
    for unit in units:
        if current and len("\n\n".join(current + [unit])) > max_chars:
            carry: list[str] = []
            if len(current) > 1 and len(current[-1]) < min_chars:
                carry = [current.pop()]  # heading stays with the text after it
            chunks.append("\n\n".join(current))
            current = carry
        current.append(unit)

    if current:
        chunks.append("\n\n".join(current))
    return chunks


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    print(f"\n{'=' * 8} {title} {'=' * 8}")


def print_chunks(chunks: list[str]) -> None:
    for number, chunk in enumerate(chunks):
        print(f"--- chunk {number} ({len(chunk)} chars) ---")
        print(chunk)


if __name__ == "__main__":
    print_header("Paragraphs (hard line breaks removed)")
    for p in split_paragraphs(SAMPLE_TEXT):
        print(" -", repr(p))

    print_header("Chunks: max 160 chars, min_chars=0 (headings can be left behind)")
    print_chunks(paragraph_chunks(SAMPLE_TEXT, max_chars=160, min_chars=0))

    print_header("Chunks: max 160 chars, min_chars=20 (headings move with their text)")
    print_chunks(paragraph_chunks(SAMPLE_TEXT, max_chars=160, min_chars=20))

    print_header("Long paragraph falls back to sentences (max 120)")
    print_chunks(paragraph_chunks(LONG_PARAGRAPH, max_chars=120))