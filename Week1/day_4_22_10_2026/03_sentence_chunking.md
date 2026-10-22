# Lesson 3: Sentence-Based Chunking

---

## 1. Concept

Split the text into **sentences first**, then pack whole sentences into a chunk until a size limit (`max_chars` or `max_tokens`) would be exceeded.

- **Why it exists:** Lessons 1 and 2 cut sentences blindly. A sentence is the smallest unit that carries a complete thought, so keeping it whole keeps the meaning whole.
- **Two steps:** (1) split into sentences, (2) group sentences into chunks.
- **Optional:** repeat the last N **sentences** (not characters) in the next chunk. This is sentence overlap.
- **Weakness:** chunk sizes vary, and splitting sentences is harder than it looks (abbreviations, numbered lists, tables).

---

## 2. Visual Example

Text: `Metformin 500mg twice daily. Do not use if eGFR is below 30. Dr. Rao advised checking renal function every 3 months. ...`

Limit: 100 characters.

```
Chunk 0: [Metformin 500mg twice daily.] [Do not use if eGFR is below 30.]          (60 chars)
Chunk 1: [Dr. Rao advised checking renal function every 3 months.] [Stop the drug before contrast imaging.]   (94 chars)
Chunk 2: [Restart after 48 hours if kidney function is stable.]                      (52 chars)
```

Compare with Lesson 1: the warning "Do not use if eGFR is below 30." is now in **one piece**, together with the dose it belongs to.

**The trap (naive splitting):** splitting on "period followed by space" breaks `Dr. Rao` into `Dr.` and `Rao advised...`. You must handle abbreviations.

---

## 3. Code (type this yourself, do not copy-paste)

```python
import re

ABBREVIATIONS = {"dr", "mr", "mrs", "ms", "prof", "e.g", "i.e", "vs", "approx", "fig", "no"}


def split_sentences_naive(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def split_sentences(text: str) -> list[str]:
    sentences = []
    for part in split_sentences_naive(text):
        if sentences:
            last_word = sentences[-1].split()[-1].rstrip(".").lower()
            if sentences[-1].endswith(".") and last_word in ABBREVIATIONS:
                sentences[-1] = f"{sentences[-1]} {part}"   # glue back
                continue
        sentences.append(part)
    return sentences


def sentence_chunks(text: str, max_chars: int = 200, overlap_sentences: int = 0) -> list[str]:
    chunks = []
    current: list[str] = []

    for sentence in split_sentences(text):
        candidate = " ".join(current + [sentence])

        if current and len(candidate) > max_chars:
            chunks.append(" ".join(current))
            current = current[-overlap_sentences:] if overlap_sentences else []
            if len(" ".join(current + [sentence])) > max_chars:
                current = []          # overlap too big, drop it

        current.append(sentence)

    if current:
        chunks.append(" ".join(current))
    return chunks
```

How to read it:

1. `(?<=[.!?])\s+` means "split at whitespace that comes right after `.`, `!` or `?`". The `(?<=...)` part is a lookbehind: it checks the character before without consuming it, so the punctuation stays on the sentence.
2. `split_sentences` repairs the naive result by gluing a piece back when the previous one ended with a known abbreviation.
3. `sentence_chunks` keeps adding sentences while they fit. When the next one would overflow, it saves the chunk and starts a new one, optionally carrying over the last N sentences.
4. A sentence longer than `max_chars` becomes its own oversized chunk. We never cut it.

Full file with demo (standard library only, no installs): `03_sentence_chunker.py`.

**Library options for production** (I could not install these in my environment, so check their docs): `nltk.sent_tokenize`, `spaCy` sentence segmenter, `pysbd`. They handle abbreviations far better than a hand-made list.

---

## 4. Drill (muscle memory)

1. Type `split_sentences_naive` from memory **3 times** (focus on the regex).
2. Type `sentence_chunks` from memory **3 times**.
3. Run the demo and find the wrong split in the naive output.
4. Predict first: with `max_chars=100` and `overlap_sentences=1`, how many chunks does the sample text give? (Answer below.)
5. Add `"inj"` and `"tab"` to the abbreviation set, then test: `Give inj. Insulin 10 units. Tab. Aspirin 75mg daily.`
6. Break it on purpose: run the naive splitter on `1. Take with food. 2. Avoid alcohol. Dose is 0.5 mg daily.` What happens to `1.` and `2.`? What about `0.5`?

**Answers:**
- 4: **4 chunks** (sizes 60, 87, 94, 91 characters).
- 6: the result is `['1.', 'Take with food.', '2.', 'Avoid alcohol.', 'Dose is 0.5 mg daily.']`. The list numbers become separate "sentences", because "1." is followed by a space. The decimal `0.5` is safe, because there is no whitespace after its period.

---

## 5. Where to Use It

|          Your content           |             Verdict              |                Why               |
|             ---                 |               ---                |                ---               |

| **Clinical protocols / health PDFs** |  Better, not enough         | Keeps each rule whole. But protocols have numbered lists, tables, abbreviations and headings that break sentence splitters. Needs structure-aware chunking (Lesson 6). |   

|          **Web pages**          |       Good for article text      | Works on paragraphs of prose. Navigation, menus and lists need cleaning first. |

|           **Code**              |             Avoid                | Code has no sentences. |

|           **Chat logs**         |              Weak                | Messages are short, informal and often have no punctuation. Chunk by message or turn instead. |

|       **PDFs (plain prose)**    |              Good                | Reports, papers and articles with normal sentences. |

**Best use:** prose where every sentence is a self-contained fact (FAQs, articles, guidelines written as sentences), and question-answering where the answer is one or two sentences.

**Watch out for:**
- Variable chunk sizes (use a `max` and sometimes a `min`).
- PDF text extraction often inserts line breaks in the middle of sentences. Clean the text first.
- Numbered lists and bullets are not sentences.
- Language matters: English rules do not work for all languages.

---

## 6. GitHub Note

Save as `03_sentence/notes.md` (and the code as `03_sentence/chunker.py`):

# 03 Sentence-Based Chunking

**Idea:** split into sentences, then pack whole sentences into chunks up to a size limit.

**Pros:** never cuts a sentence; each chunk is a complete thought; sentence overlap is natural.
**Cons:** chunk sizes vary; sentence splitting is tricky (Dr., e.g., 1., decimals, PDFs with broken lines).

**Key regex:** `(?<=[.!?])\s+` (split after punctuation + whitespace).
**Gotchas:** abbreviations break the naive splitter; numbered lists become fake sentences; one long sentence can exceed max size.

**Use for:** prose, FAQs, articles, guidelines written as sentences.
**Avoid for:** code, chat logs, tables, heavily structured clinical documents.

**Production:** use nltk / spaCy / pysbd instead of a hand-made abbreviation list.

---

**Next:** Lesson 4, Paragraph-based chunking.