Week 1: Naive RAG, end to end
Goal: a command-line tool that answers questions about your documents and names the file each answer came from.
[ ] Sunday (plan): Create a project folder and a journal/ folder. Pick 5 to 10 of your own documents. Write 10 questions you know the answers to, with the expected answers.
[ ] Monday: Ask an LLM your 10 questions with no documents. Record which ones it gets wrong or invents. This is the problem RAG solves.
[ ] Tuesday: Load your documents and split them into chunks of about 500 characters with a small overlap. Print 10 chunks and read them. Note anything that looks broken.
[ ] Wednesday: Turn each chunk into an embedding and store it in a vector store. Search for each of your 10 questions and check by eye whether the right chunk is in the top 3.
[ ] Thursday: Put the top chunks into a prompt and ask the LLM to answer only from them, naming the source file.
[ ] Friday: Run all 10 questions. In a small table, mark each one: retrieval right or wrong, answer right or wrong. Look for patterns in the failures.
[ ] Saturday: Write the README (how to run it) and the weekly summary. Record a 2-minute screen demo if you like.


Week 2: Measure and improve retrieval
Goal: stop guessing. Change one thing at a time and let a score tell you whether it helped.
[ ] Sunday (plan): Grow your question set from 10 to 20. For each question, note which file or chunk contains the answer.
[ ] Monday: Write an evaluation script that reports hit rate at 3 (is the right chunk in the top 3?). Run it on your Week 1 setup and save the number as your baseline.
[ ] Tuesday: Try 3 chunk sizes (for example 200, 500 and 1000 characters). Rerun the script each time and log the scores in an experiments table.
[ ] Wednesday: Try different top-k values and add metadata (file name, section title) to chunks. Log the results.
[ ] Thursday: Add keyword search (BM25) next to vector search and combine the two. Compare against your baseline.
[ ] Friday: Add a reranker on the top 10 results. Log the score and the extra response time.
[ ] Saturday: Pick the best setup, write down why it won, and add one line on what surprised you.


Week 3: Trustworthy answers and a usable app
Goal: an app other people could use, which cites its sources and admits when it does not know.
[ ] Sunday (plan): Write 5 questions your documents cannot answer. These test whether the app refuses instead of inventing.
[ ] Monday: Rewrite the prompt so the model answers only from the retrieved text, quotes the source, and says "I don't know" when the text lacks the answer. Test on your 5 unanswerable questions.
[ ] Tuesday: Add a relevance cutoff: if the best chunk scores too low, skip the LLM and say there is no answer. Tune the cutoff using your questions.
[ ] Wednesday: Add messier documents (tables, PDFs with columns, a scanned page). Note what breaks in loading and chunking, and fix the worst problem.
[ ] Thursday: Add follow-up questions. Rewrite each follow-up into a standalone question using the chat history, then retrieve.
[ ] Friday: Build a simple web interface (Streamlit or FastAPI) that shows the answer and the source chunks next to it.
[ ] Saturday: Rerun your full evaluation, record the refusal score, and write the weekly summary.


Week 4: Ship it and learn from failures
Goal: a RAG app that runs with one command, logs what it does, and has a check you rerun after every change.
[ ] Sunday (plan): List what must work for you to call the project finished. Keep it to 5 items.
[ ] Monday: Add logging: for every question, save the question, the retrieved chunks, the answer, and the time taken.
[ ] Tuesday: Package the app with Docker so it starts with one command on a clean machine.
[ ] Wednesday: Turn your evaluation into one command that prints hit rate, refusal score and average response time. Run it before and after every change from now on.
[ ] Thursday: Read your logs and pick the 5 worst answers. For each, decide whether retrieval, the prompt or the documents caused the failure, and fix one.
[ ] Friday: Deploy it somewhere free if you want to share it, or record a demo instead.
[ ] Saturday: Write the final write-up: what you built, your experiments table, the 3 biggest lessons, and what you would try next.
Stretch ideas once the basics work: query rewriting with several variants, answering from tables, or comparing two embedding models on your evaluation.
Documentation system
Write a 5-minute note at the end of every session. The last line, "Start here next time", is what lets you pick the work up weeks later without re-reading everything.
Folder layout: one journal/ folder with week1/ to week4/, a glossary.md for terms you learn, and an experiments.md table for Weeks 2 to 4.


Daily note template (copy for each session):
# Day note: <date> (Week <n>, Day <n>)

**Goal today:**
**What I built or changed:**
**What broke, and why (in my own words):**
**One thing I learned:**
**Numbers (hit rate, time, score):**
**Start here next time:**
Weekly summary (Saturday): what you shipped, the scores that moved, the 3 mistakes that taught you the most, and next week's first task. Add each new term to glossary.md with a one-line explanation and an example from your own project.
On a busy day (20-minute version): do only the day's first checkbox, write the note, and write the "Start here next time" line. A short day that keeps the thread beats a skipped one.