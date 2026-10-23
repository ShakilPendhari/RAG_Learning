# Lesson 4: Paragraph-Based Chunking

---

## 1. Concept

Split the text on **blank lines** (paragraphs), then pack whole paragraphs into a chunk until a size limit would be exceeded.

- **Why it exists:** a paragraph is how the author grouped one idea. Keeping a paragraph whole keeps the idea whole, and the paragraph boundary is a natural place to cut.
- **Compared with sentences (Lesson 3):** bigger units, so each chunk carries more context, and no sentence-splitting tricks are needed (no `Dr.` problem).
- **Three practical add-ons** (all in the code below):
  1. **Un-wrap hard line breaks.** PDFs often break a line in the middle of a sentence.
  2. **Fallback for long paragraphs.** If one paragraph is bigger than `max_chars`, split it by sentences.
  3. **Keep headings with their text.** A tiny paragraph (like "Contraindications") must not be left alone at the end of a chunk.
- **Weakness:** it depends on the text really having blank lines between paragraphs, and paragraph sizes vary a lot.

---

## 2. Visual Example

Input (a PDF-style text with hard-wrapped lines):

```
Metformin Protocol

Dosage

Start with 500mg twice daily with meals. Increase by 500mg every
week if tolerated. Maximum dose is 2000mg daily.

Contraindications

Do not use if eGFR is below 30. Stop before contrast imaging and
restart after 48 hours if kidney function is stable.

Monitoring

Check renal function every 3 months. Check vitamin B12 yearly.
```

**Without heading protection** (`max_chars=160, min_chars=0`):

```
chunk 0 (160 chars):  Metformin Protocol / Dosage / Start with 500mg ... / Contraindications   <-- heading orphaned
chunk 1 (129 chars):  Do not use if eGFR is below 30. ... / Monitoring                         <-- heading orphaned
chunk 2 ( 62 chars):  Check renal function every 3 months. ...
```

The heading "Contraindications" sits in the wrong chunk, away from its text. A search for "contraindications" would find chunk 0, which does not contain the rule.

**With heading protection** (`max_chars=160, min_chars=20`):

```
chunk 0 (141 chars):  Metformin Protocol / Dosage / Start with 500mg ...
chunk 1 (136 chars):  Contraindications / Do not use if eGFR is below 30. ...
chunk 2 ( 74 chars):  Monitoring / Check renal function every 3 months. ...
```

Each heading now travels with its content.

---

## 3. Code (type this yourself, do not copy-paste)

```python
import re


def split_paragraphs(text: str) -> list[str]:
    paragraphs = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = re.sub(r"\s*\n\s*", " ", block).strip()   # un-wrap hard line breaks
        if block:
            paragraphs.append(block)
    return paragraphs


def split_long_paragraph(paragraph: str, max_chars: int) -> list[str]:
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", paragraph) if s]
    pieces, current = [], []
    for sentence in sentences:
        if current and len(" ".join(current + [sentence])) > max_chars:
            pieces.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        pieces.append(" ".join(current))
    return pieces


def paragraph_chunks(text: str, max_chars: int = 300, min_chars: int = 0) -> list[str]:
    units = []
    for paragraph in split_paragraphs(text):
        if len(paragraph) > max_chars:
            units.extend(split_long_paragraph(paragraph, max_chars))
        else:
            units.append(paragraph)

    chunks, current = [], []
    for unit in units:
        if current and len("\n\n".join(current + [unit])) > max_chars:
            carry = []
            if len(current) > 1 and len(current[-1]) < min_chars:
                carry = [current.pop()]          # heading moves to the next chunk
            chunks.append("\n\n".join(current))
            current = carry
        current.append(unit)

    if current:
        chunks.append("\n\n".join(current))
    return chunks
```

How to read it:

1. `re.split(r"\n\s*\n", ...)`: a newline, optional spaces, another newline = a blank line = a paragraph break.
2. `re.sub(r"\s*\n\s*", " ", ...)`: any remaining single line break inside a paragraph becomes a space. This repairs sentences that a PDF broke across lines.
3. A paragraph longer than `max_chars` is replaced by sentence-packed pieces, so no unit is ever too big.
4. The packing loop is Lesson 3's idea, with `"\n\n"` as the glue so paragraph boundaries stay visible.
5. `carry`: when a chunk is about to be saved and its last unit is tiny, that unit is removed and starts the next chunk.

Full file with demo (standard library only): `04_paragraph_chunker.py`.

---

## 4. Drill (muscle memory)

1. Type `split_paragraphs` from memory **3 times**, then `paragraph_chunks` **3 times**.
2. Predict first: `max_chars=160, min_chars=0` on the sample text. How many chunks, and which heading is orphaned?
3. Run `split_paragraphs` on this and read the output:
   `"Dosage\nStart with 500mg twice daily.\n\nNotes\n- take with food\n- avoid alcohol"`
   What went wrong with the heading, and with the bullet list?
4. Run the sample with `min_chars=10`. Does "Contraindications" (17 characters) still get orphaned? Why?
5. Run the sample with `max_chars=100, min_chars=20`. Chunk 0 is only `Metformin Protocol`. Why does the title end up alone, and how would you fix it?

**Answers:**
- 2: **3 chunks** (160, 129 and 62 characters). "Contraindications" is orphaned at the end of chunk 0, and "Monitoring" at the end of chunk 1.
- 3: `['Dosage Start with 500mg twice daily.', 'Notes - take with food - avoid alcohol']`. A heading with only a single newline after it gets glued into the paragraph, and bullet lists collapse into one line. Un-wrapping is dangerous for lists and for headings that have no blank line after them.
- 4: Yes. 17 is not below 10, so the heading is not seen as "tiny". `min_chars` is a crude heading detector: it only works if headings are shorter than the value.
- 5: Only the **last** tiny unit is carried over, so "Metformin Protocol" is left behind while "Dosage" moves on. Fix: replace the single `if` with a `while` loop that carries **all** consecutive tiny units from the end of the chunk.

---

## 5. Where to Use It

| Your content | Verdict | Why |
|---|---|---|
| **Clinical protocols / health PDFs** | Good start, not final | Keeps rules and their explanation together. But `min_chars` is a guess at headings, and tables and numbered lists need real structure handling (Lesson 6). Check that your PDF extractor keeps blank lines between paragraphs. |
| **Web pages** | Good | After converting HTML to text, `<p>` blocks become paragraphs. Remove menus and footers first. |
| **Code** | Avoid | Blank lines in code do not mark logical units reliably. Use code-aware chunking (Lesson 7). |
| **Chat logs** | Avoid | There are no paragraphs. Chunk by message, turn or time window. |
| **PDFs (plain prose)** | Good | Reports, papers and articles, as long as the extraction keeps paragraph breaks. |

**Best use:** well-written prose where each paragraph is one idea (articles, guidelines, documentation, blog posts).

**Watch out for:**
- Some PDF extractors return text with no blank lines at all. Then the whole document is one giant paragraph and your code falls back to sentences everywhere. Print the extracted text and look at it before choosing a strategy.
- Un-wrapping line breaks damages bullet lists and tables.
- Chunk sizes vary a lot: one-line paragraphs and 2000-character paragraphs both exist.
- Two headings in a row are not fully handled by the simple version (drill 5).

---

## 6. GitHub Note

Save as `04_paragraph/notes.md` (and the code as `04_paragraph/chunker.py`):

# 04 Paragraph-Based Chunking

**Idea:** split on blank lines, un-wrap hard line breaks, pack whole paragraphs into chunks up to a size limit.

**Key regexes:** `\n\s*\n` (paragraph break), `\s*\n\s*` -> space (un-wrap).
**Add-ons:** sentence fallback for paragraphs over max size; carry tiny paragraphs (headings) to the next chunk.

**Pros:** keeps one idea per chunk; no sentence-splitting tricks; more context than sentence chunks.
**Cons:** needs real paragraph breaks in the text; sizes vary; un-wrapping breaks lists/tables; `min_chars` is only a crude heading guess.

**Gotchas:** check the extractor output first (PDFs may have no blank lines); a heading with one newline gets glued to its paragraph; consecutive headings need a loop, not an `if`.

**Use for:** articles, guidelines, documentation, web text.
**Avoid for:** code, chat logs, tables, heavily structured clinical documents.

---

**Next:** Lesson 5, Recursive character chunking.