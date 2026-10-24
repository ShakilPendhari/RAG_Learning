import re

# =============================================================================
# REGEX PATTERNS (read these first)
# =============================================================================

# -----------------------------------------------------------------------------
# 1) INITIAL_PATTERN  -> finds a single capital letter + dot, like "J." or "K."
#
#       \b([A-Z])\.
#
#   \b       word boundary: the letter must START a word.
#            "J. K." matches, but the "U." in "ICU." does not (U is inside a word).
#   [A-Z]    one capital letter (A to Z)
#   (...)    brackets = remember this part, so we can use it again as \1
#   \.       a real dot. A plain "." in regex means "any character",
#            so we write \. to say "the dot character itself".
#
#   Used with re.sub(..., r"\1<DOT>", text):  "J." -> "J<DOT>"   (\1 = the letter)
# -----------------------------------------------------------------------------
INITIAL_PATTERN = r"\b([A-Z])\."

# -----------------------------------------------------------------------------
# 2) SENTENCE_BREAK_PATTERN  -> finds the SPACE between two sentences
#
#       (?<=[.!?])\s+(?=[A-Z0-9])
#
#   (?<=[.!?])   LOOK BEHIND: the text just before must be  .  !  or  ?
#                It only checks. It does not become part of the match,
#                so the dot stays attached to its sentence when we split.
#   [.!?]        any ONE of these three characters
#   \s+          one or more whitespace characters (space, tab, newline).
#                THIS is the part that is matched, so THIS is what gets cut out.
#   (?=[A-Z0-9]) LOOK AHEAD: the text just after must start with a capital
#                letter or a digit. Again it only checks, it is not removed.
#
#   Why this helps:
#     "daily. Do not"     -> dot, space, capital D   -> split
#     "0.5 mg"            -> dot but NO whitespace   -> no split
#     "1. a, 2. b"        -> next letter is lowercase -> no split
# -----------------------------------------------------------------------------
SENTENCE_BREAK_PATTERN = r"(?<=[.!?])\s+(?=[A-Z0-9])"

# -----------------------------------------------------------------------------
# 3) NUMBER_ONLY_PATTERN  -> a piece that is ONLY a list number, like "1." or "12."
#
#       \d+\.
#
#   \d       one digit (0 to 9)
#   +        one or more of them  ("1", "12", "305" ...)
#   \.       a real dot
#
#   Used with re.fullmatch, which means the WHOLE piece must look like this.
#   So "1." matches, but "Do not use if eGFR is below 30." does not
#   (it only ENDS with a number, it is not only a number).
# -----------------------------------------------------------------------------
NUMBER_ONLY_PATTERN = r"\d+\."

# Words whose dot is NOT the end of a sentence (we hide their dot, see Step 1)
ABBREVIATIONS = ["Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "vs.", "e.g.", "i.e."]


# =============================================================================
# CODE
# =============================================================================

def split_sentences(text):
    if not text.strip():          # empty text -> no sentences
        return []

    # Step 1: hide the dots that are NOT sentence ends
    for word in ABBREVIATIONS:
        text = text.replace(word, word.replace(".", "<DOT>"))   # Dr. -> Dr<DOT>
    text = re.sub(INITIAL_PATTERN, r"\1<DOT>", text)             # J. -> J<DOT>

    # Step 2: cut the text at the spaces between sentences
    pieces = re.split(SENTENCE_BREAK_PATTERN, text)

    # Step 3: a piece that is only "1." or "2." belongs to the sentence after it
    sentences = []
    for piece in pieces:
        if sentences and re.fullmatch(NUMBER_ONLY_PATTERN, sentences[-1]):
            sentences[-1] = sentences[-1] + " " + piece
        else:
            sentences.append(piece)

    # Step 4: put the hidden dots back
    return [s.replace("<DOT>", ".") for s in sentences]


if __name__ == "__main__":
    text = (
        "Metformin 500mg twice daily. Do not use if eGFR is below 30. "
        "Dr. Rao advised checking renal function every 3 months. "
        "Stop the drug before contrast imaging. "
        "Restart after 48 hours if kidney function is stable. "
        "Options are 1. a, 2. b, 3. c. Author is J. K. Rowling."
    )
    for sentence in split_sentences(text):
        print("-", sentence)