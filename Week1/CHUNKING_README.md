Curriculum (we go one at a time)
#	Strategy	                                   One-line idea
1	Fixed-size chunking	                           Split every N characters/tokens
2	Fixed-size with overlap	                       Same, but chunks share some text so context isn’t cut
3	Sentence-based chunking	                       Split on sentence boundaries, group sentences
4	Paragraph-based chunking	                   Split on blank lines / paragraphs
5	Recursive character chunking	               Try separators in order: paragraph, line, sentence, word
6	Document-structure chunking	                   Split by headings (Markdown, HTML, PDF sections)
7	Code-aware chunking	                           Split by functions/classes using language syntax
8	Semantic chunking	                           Split where the meaning changes, using embeddings
9	Sliding window chunking	                       Overlapping windows moving over the text
10	Parent-child (small-to-big) chunking	       Search small chunks, return the bigger parent
11	Sentence-window retrieval	                   Embed one sentence, return it with its neighbours
12	Hierarchical / RAPTOR-style chunking	       Chunks summarized into higher-level nodes
13	Agentic / LLM-based chunking	               An LLM decides the split points
14	Contextual chunking	                           Add LLM-written context to each chunk before embedding
15	Late chunking	                               Embed the whole document first, then pool per chunk
16	Table / multimodal chunking	                   Handle tables, images and PDFs specially
17	Metadata-enriched chunking	                   Attach source, section, date, etc. to each chunk
18	Final: choosing a strategy	                   Decision guide by project type, plus evaluation



For each lesson we’ll use the same structure so it sticks:

Concept: what it is and why it exists
Visual example: a tiny text example
Code: Python you type yourself, not copy-paste
Drill: a small exercise to repeat
Where to use it: which project sections it fits and which it doesn’t
GitHub note: a short .md file for your repo