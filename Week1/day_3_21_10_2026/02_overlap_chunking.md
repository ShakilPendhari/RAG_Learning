# Lesson 2: Fixed-Size Chunking with Overlap

---

## 1. Concept

Same as Lesson 1 (cut every N characters/tokens), but each chunk **repeats the last part of the previous chunk**. That repeated part is the **overlap**.

- **Why it exists:** Lesson 1 cut "eGFR" and "Do not use if..." in half. With overlap, text near a boundary appears in two chunks, so at least one chunk usually holds it whole.
- **Formula:** `step = chunk_size - overlap` (how far the window moves each time)
- **Typical overlap:** 10 to 20% of chunk size (for example size 500, overlap 50 to 100)
- **Weakness:** still blind to meaning. Overlap only helps if it is **bigger than the unit you want to keep intact**.

---

## 2. Visual Example

Text (60 characters), chunk size 20, overlap 8 (so step = 12):

```
Metformin 500mg twice daily. Do not use if eGFR is below 30.

chunk 0: Metformin 500mg twic
chunk 1:          0mg twice daily. Do 
chunk 2:                    ily. Do not use if e
chunk 3:                             use if eGFR is below
chunk 4:                                        is below 30.
```

What improved: chunk 2 cuts "eGFR" (`e`), but chunk 3 holds `eGFR` whole.

What did NOT improve: no single chunk holds the full sentence "Do not use if eGFR is below 30". The overlap (8) is smaller than the sentence (about 31), so the warning is still split. To keep a unit whole, overlap must be at least as long as that unit.

---

## 3. Code (type this yourself, do not copy-paste)

```python
def overlap_chunks(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    step = chunk_size - overlap
    chunks = []
    for start in range(0, len(text), step):
        chunks.append(text[start : start + chunk_size])
        if start + chunk_size >= len(text):  # reached the end, stop
            break
    return chunks
```

Three things to understand, not memorize:

1. `range(0, len(text), step)`: the window jumps by `step`, not by `chunk_size`.
2. The `if overlap >= chunk_size` guard: if the overlap equals the size, the step is 0 and the loop never moves (infinite loop).
3. The `break`: without it you get extra tail chunks that are already fully contained in the previous chunk.

Full file with the token version and demo: `02_overlap_chunker.py`.

**Token version** (same idea, step counted in tokens):

```python
def overlap_token_chunks(text, chunk_tokens=200, overlap=40):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    step = chunk_tokens - overlap
    chunks = []
    for start in range(0, len(tokens), step):
        chunks.append(enc.decode(tokens[start : start + chunk_tokens]))
        if start + chunk_tokens >= len(tokens):
            break
    return chunks
```

Using your 21-token output from Lesson 1 with size 8 and overlap 3 (step 5), the chunks start at token 0, 5, 10, 15:

```
0: 'Metformin 500mg twice daily'
1: 'mg twice daily. Do not use if'
2: ' not use if eGFR is below'
3: 'FR is below 30.'
```

Chunk 2 now contains "eGFR" whole, which Lesson 1's token chunks never did.

---

## 4. Drill (muscle memory)

1. Type `overlap_chunks` from memory **3 times**.
2. Predict first: a 1000-character text, `chunk_size=300`, `overlap=100`. How many chunks, and how long is the last one?
3. Run it with `overlap=0`, then `8`, then `15` on the Metformin sentence. At which overlap does a chunk first contain the full word "eGFR"?
4. Set `overlap=300` with `chunk_size=300`. Read the error and explain why the guard exists.
5. Compute the storage cost: size 500, overlap 100. How much more text do you store than with no overlap?

**Answers:**
- 2: step = 200, so chunks start at 0, 200, 400, 600, 800. That is **5 chunks**, and the last has **200 characters**.
- 3: overlap 8 already works for "eGFR" (see the example above). For the whole sentence you would need an overlap of about 31.
- 4: step would be 0, so the window never moves.
- 5: step = 400, so you store 500/400 = **1.25x**, which is 25% more text and 25% more embeddings.

---

## 5. Where to Use It

| Your content | Verdict | Why |
|---|---|---|
| **Clinical protocols / health PDFs** | Weak | Better than Lesson 1, but a dose and its contraindication can still be split. Use structure-aware strategies later. |
| **Web pages** | Baseline | Fine as a quick comparison point. Ignores headings. |
| **Code** | Avoid | Overlap cannot fix a function cut in half. |
| **Chat logs** | Okay | Overlap carries the previous message into the next chunk, so a reply keeps some context. |
| **PDFs (plain prose)** | Good for a first prototype | Articles and essays tolerate this well. |

**Costs to remember:**
- More chunks means more storage and more embedding cost.
- The same text can be retrieved twice, so you may get near-duplicate results.

**Best use:** prototypes and plain prose where you want a cheap safety margin at chunk boundaries.

---

## 6. GitHub Note

Save as `02_overlap/notes.md` (and the code as `02_overlap/chunker.py`):

# 02 Fixed-Size Chunking with Overlap

**Idea:** fixed-size chunks, but each repeats the tail of the previous one.

**Formula:** `step = chunk_size - overlap`. Typical overlap 10-20%.

**Pros:** boundary text appears in two chunks; still simple and fast.
**Cons:** still ignores meaning; duplicates data (+25% at 500/100); near-duplicate retrieval results.

**Key lesson:** overlap must be longer than the unit you want to keep whole (a sentence, a dose rule). A small overlap only rescues short pieces like a single term.

**Gotchas:** guard `overlap >= chunk_size` (infinite loop); `break` when the window reaches the end.

**Use for:** prototypes, plain prose, chat logs.
**Avoid for:** code, clinical tables, structured documents.

---

**Next:** Lesson 3, Sentence-based chunking.