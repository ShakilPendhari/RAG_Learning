# Lesson 1: Fixed-Size Chunking

---

## 1. Concept

Cut the text into equal pieces of N characters (or N tokens), ignoring the content.

- **Why it exists:** embedding models and LLMs have input limits, and a whole document in one vector gives blurry search results.
- **Why it's simple:** no parsing, no models, fast and predictable.
- **Weakness:** it cuts blindly, even in the middle of a word, sentence or table row.

---

## 2. Visual Example

Text (60 characters), chunk size 20:

```
Metformin 500mg twice daily. Do not use if eGFR is below 30.
|--------------------|--------------------|--------------------|
 Metformin 500mg twi  ce daily. Do not us  e if eGFR is below 30.
```

The sentence "Do not use if eGFR is below 30" is split across two chunks. A search could retrieve one half and miss the warning. In clinical text, that is a real safety problem.

---

## 3. Code (type this yourself, do not copy-paste)

### Version A: by characters

```python
def fixed_size_chunks(text: str, chunk_size: int = 500) -> list[str]:
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i : i + chunk_size])
    return chunks


if __name__ == "__main__":
    text = "Metformin 500mg twice daily. Do not use if eGFR is below 30."
    for n, c in enumerate(fixed_size_chunks(text, 20)):
        print(n, repr(c))
```

### Version B: by tokens (what models actually count)

```python
import tiktoken

def fixed_token_chunks(text: str, chunk_tokens: int = 200) -> list[str]:
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), chunk_tokens):
        chunks.append(enc.decode(tokens[i : i + chunk_tokens]))
    return chunks
```

Install with `pip install tiktoken`.
Characters are easier to reason about. Tokens match the model limit exactly, so prefer them in real projects.

---

## 4. Drill (muscle memory)

Do these in order, without looking at the code while typing:

1. Type `fixed_size_chunks` from memory **3 times**.
2. Predict first: a 1000-character text with `chunk_size=300` gives how many chunks, and how long is the last one?
3. Run it on any paragraph and find a chunk that cuts a word in half.
4. Change `chunk_size` to 50, 200 and 1000. Notice how retrieval quality would change: tiny chunks lose context, huge chunks blur meaning.

**Answer to 2:** 4 chunks, and the last one has 100 characters.

---

## 5. Where to Use It

| Your content | Verdict | Why |
|---|---|---|
| **Clinical protocols / health PDFs** | Avoid | Splits doses, contraindications and tables. Dangerous for accuracy. |
| **Web pages** | Baseline only | Ignores headings and layout, so chunks are noisy. |
| **Code** | Avoid | Cuts functions in half. |
| **Chat logs** | Weak | Splits a message, or a question from its answer. |
| **PDFs (plain prose)** | OK for a baseline | Fine for a first prototype. |

**Best use:** a quick baseline to compare other strategies against, uniform text, and fast prototypes. Every later strategy in this course exists to fix a weakness of this one.

---

## 6. GitHub Note

Save as `01_fixed_size/notes.md` (and the code above as `01_fixed_size/chunker.py`):

# 01 Fixed-Size Chunking

**Idea:** split text every N characters/tokens, ignoring content.

**Pros:** simple, fast, predictable chunk size.
**Cons:** cuts mid-word/sentence/table; no semantic awareness.

**Code:** see `chunker.py` (char version + tiktoken version)

**Use for:** baseline, prototypes, uniform text.
**Avoid for:** clinical protocols, code, tables, chat logs.

**Key lesson:** small chunks lose context, big chunks blur meaning. Always compare other strategies against this baseline.

---

**Next:** Lesson 2, Fixed-size with overlap.