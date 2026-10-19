# RAG (Retrieval-Augmented Generation): A Complete Guide

## 1. What is RAG?

**RAG stands for Retrieval-Augmented Generation.**

-   **Retrieval:** Find relevant information from a data source.
-   **Augmented:** Give that information to the AI model as additional
    context.
-   **Generation:** Let the AI model generate an answer using that
    context.

In simple terms:

> RAG is a technique in which an AI application searches for relevant
> information from an external knowledge source and provides that
> information to an LLM so it can generate a more relevant, grounded
> answer.

### Example

Imagine building an AI assistant for a company that has hundreds of PDF
documents containing product details, policies, pricing, and technical
documentation.

A user asks:

> What is our company's refund policy for annual subscriptions?

A general-purpose LLM does not automatically know the company's private
policy. With RAG, the application retrieves the relevant section from
company documents and provides it to the LLM. The model generates an
answer based on that evidence.

**Important:** RAG is not a special type of LLM. It is a system
architecture that combines information retrieval with LLM generation.

------------------------------------------------------------------------

## 2. Why do we need RAG?

### Problem 1: Private knowledge

A model is not automatically trained on your private company documents,
internal codebase, customer records, or proprietary policies.

### Problem 2: Changing information

Pricing, product features, technical documentation, and policies can
change after a model's training.

### Problem 3: Hallucinations

An LLM can generate a convincing answer that is factually wrong,
especially when the required information is missing or ambiguous.

### With RAG

1.  The application searches relevant documents.
2.  It finds information related to the question.
3.  It provides that information to the LLM.
4.  The LLM generates an answer grounded in the retrieved context.

  -----------------------------------------------------------------------
  Without RAG                         With RAG
  ----------------------------------- -----------------------------------
  Relies on information available to  Can use external information
  the model in its training and       retrieved at query time
  supplied context                    

  May not know private data           Can access authorized private
                                      documents

  May give outdated answers           Can use updated sources if the
                                      source or index is current

  Harder to trace an answer's source  Can return citations or source
                                      references

  Can invent missing details          Can be instructed to acknowledge
                                      missing evidence
  -----------------------------------------------------------------------

RAG can reduce hallucinations, but it does not eliminate them. Retrieval
can return irrelevant information, documents can be outdated, and the
LLM can still misinterpret evidence.

------------------------------------------------------------------------

## 3. How does RAG work internally?

A typical RAG application has two workflows:

1.  **Indexing workflow:** Prepare documents so they can be searched
    efficiently.
2.  **Query workflow:** Find relevant information when a user asks a
    question.

Indexing usually happens before the question arrives. Retrieval and
generation happen at query time.

------------------------------------------------------------------------

## 4. Workflow A --- Preparing the knowledge base

Suppose an e-commerce company has:

-   PDF documents
-   Product manuals
-   Refund policies
-   Shipping policies
-   Frequently asked questions
-   Technical documentation

Passing every document to the LLM for every question is inefficient. The
application needs a way to organize and search the information.

### Step 1: Collect documents

Sources can include PDFs, websites, databases, text files, Notion pages,
and internal documentation.

### Step 2: Extract and clean text

Convert files into usable text. Remove irrelevant content and preserve
headings, tables, and useful metadata where possible.

### Step 3: Split text into chunks

Break large documents into smaller, meaningful pieces that can be
retrieved independently.

### Example of chunking

Original policy:

> Customers may request a refund within 14 days of purchase. Digital
> products that have already been downloaded are not eligible for
> refunds. Enterprise subscriptions follow a separate contract.

Possible chunks:

**Chunk 1 --- Refund window**

> Customers may request a refund within 14 days of purchase.

**Chunk 2 --- Exceptions**

> Digital products that have already been downloaded are not eligible
> for refunds.

**Chunk 3 --- Enterprise subscriptions**

> Enterprise subscriptions follow a separate contract.

Now the system can retrieve a relevant passage without retrieving the
entire policy.

### How large should a chunk be?

There is no universal answer.

-   Very small chunks may lose context.
-   Very large chunks may contain irrelevant information.
-   Overlapping chunks can preserve context across boundaries.
-   Headings, paragraphs, tables, and semantic boundaries often matter
    more than blindly splitting at a fixed character count.

As an initial experiment, try chunks of roughly 300--800 tokens with
some overlap, then measure retrieval quality. This is a starting point,
not a universal rule.

### Step 4: Generate embeddings

An **embedding** is a numerical representation of data, usually produced
by an embedding model.

Consider these sentences:

-   "How can I get my money back?"
-   "What is the procedure for requesting a refund?"

The wording differs, but the meanings are similar. A good semantic
embedding model can map them to vectors that are relatively close in its
vector space.

Illustrative vectors:

``` text
Sentence A -> [0.82, 0.14, -0.31, 0.67, ...]
Sentence B -> [0.79, 0.17, -0.28, 0.63, ...]
```

These numbers are made up for illustration. Real embeddings often
contain hundreds or thousands of dimensions.

The vectors are outputs of a trained embedding model, not manually
assigned word scores.

During indexing, the application generates an embedding for each chunk
and stores it. During a query, it embeds the user's question and
searches for similar stored vectors.

**An embedding model does not answer the question. It helps the system
find potentially relevant information.** The LLM generally performs the
final natural-language generation.

### Step 5: Store searchable records

A vector database stores and searches vector representations. It can
find vectors similar to a query vector, often using approximate
nearest-neighbor algorithms for scale.

Common options include:

-   Pinecone
-   Weaviate
-   Qdrant
-   Chroma
-   PostgreSQL with pgvector

You do not always need a dedicated vector database. For a small
application, PostgreSQL with pgvector or another suitable search index
may be enough.

Example record:

``` js
{
  id: "chunk_102",
  text: "Customers may request a refund within 14 days...",
  embedding: [0.82, 0.14, -0.31, 0.67],
  metadata: {
    document: "refund-policy.pdf",
    section: "Refund Window",
    tenantId: "company_123"
  }
}
```

The vector is abbreviated and illustrative.

Notice that the record stores more than the vector:

-   `text`: the source content to provide to the LLM.
-   `embedding`: the numerical representation used for vector search.
-   `metadata`: information used for filtering, access control, and
    citations.

------------------------------------------------------------------------

## 5. Workflow B --- Answering a user's question

Suppose a user asks:

> Can I get a refund if I request it 10 days after purchasing?

The query workflow is:

1.  **Receive the query.**
2.  **Retrieve relevant chunks** by searching the knowledge base.
3.  **Filter or rerank results** to select useful evidence.
4.  **Construct the LLM prompt** with the question and retrieved
    context.
5.  **Generate the response** using the evidence.

Example retrieved context:

> Customers may request a refund within 14 days of purchase. Digital
> products that have already been downloaded are not eligible for
> refunds.

Possible answer:

> The policy allows refund requests within 14 days of purchase, so a
> request after 10 days falls within that window. However, downloaded
> digital products are excluded.

The answer accounts for both the refund window and an important
exception. If the system retrieves only the 14-day window but misses the
exception, the answer may be incomplete.

### Example LLM prompt

``` text
SYSTEM:
You are a customer-support assistant.

Answer using the supplied context.
Do not invent policy details.
If the context does not contain the answer, say so.
Mention relevant exceptions.

CONTEXT:
Customers may request a refund within 14 days of purchase.
Digital products that have already been downloaded are not
eligible for refunds.

USER QUESTION:
Can I get a refund if I request it 10 days after purchasing?
```

The LLM receives the context as part of its input. It does not
necessarily connect to the vector database itself. The application
typically performs retrieval and passes the results to the model.

**Core RAG mechanism: retrieve first, generate second.**

------------------------------------------------------------------------

## 6. Keyword search vs. semantic search

Suppose a document says:

> Customers can request a refund within 14 days.

The user asks:

> How long do I have to get my money back?

A traditional keyword search might look for words such as `money`,
`back`, or `refund`. If the document does not contain the user's exact
terms, a simple keyword search may miss it.

Semantic search uses embeddings to identify related meanings, so it may
retrieve the refund policy even when the wording differs.

  -----------------------------------------------------------------------
  Keyword search                      Semantic search
  ----------------------------------- -----------------------------------
  Primarily matches terms and tokens  Matches similarity in learned
                                      meaning

  Strong for exact product codes,     Strong for paraphrases and
  names, and phrases                  natural-language questions

  Can miss differently worded queries Can miss exact matches or confuse
                                      related concepts

  Commonly uses inverted indexes,     Commonly uses vector similarity
  such as BM25                        
  -----------------------------------------------------------------------

Neither approach is universally better. Production RAG systems often use
**hybrid search**, combining keyword retrieval with vector retrieval.
This is useful when users ask about both concepts and exact identifiers,
such as "refund policy for product SKU AB-104."

### How is similarity calculated?

A common method is cosine similarity:

\[ \\operatorname{cosine}(A,B)= \\frac{A\\cdot B}{\\\|A\\\|\\\|B\\\|} \]

Here, (A) is the query embedding and (B) is a document embedding. The
score measures angle-based similarity between two nonzero vectors.

A higher score often indicates greater semantic similarity, but it is
not a universal probability that the document is relevant. The exact
behavior depends on the embedding model and retrieval configuration.

------------------------------------------------------------------------

## 7. What is reranking?

Imagine a user asks:

> Can I cancel my annual subscription and get a refund?

Initial retrieval returns:

    Rank Retrieved chunk               Relevance
  ------ ----------------------------- -----------
       1 Annual subscription pricing   Medium
       2 Cancellation process          High
       3 Refund eligibility            Very high
       4 Monthly billing FAQ           Low
       5 Enterprise contract terms     Medium

Vector search may rank the most useful passage below another passage
because semantic similarity does not guarantee answer relevance.

A **reranker** evaluates query-document pairs more precisely and
reorders them. The application can then select the best passages for the
LLM.

A possible pipeline:

1.  Retrieve 20 candidate chunks.
2.  Rerank the candidates.
3.  Select the top 3--5 relevant chunks.
4.  Send those chunks to the LLM.

These numbers are illustrative. The right values depend on the data,
latency requirements, and evaluation results.

Reranking is optional, not mandatory. Better retrieval can improve
answer quality, but reranking adds computation, latency, and cost.
Measure whether the improvement justifies the expense.

------------------------------------------------------------------------

## 8. Real-world example: RAG for a SaaS product

Imagine building an AI assistant for a multi-tenant SaaS application
such as CricVision.

Users ask:

-   "How do I create a new academy?"
-   "How do I invite a coach?"
-   "Why can't I access the analytics page?"
-   "What is included in my subscription?"

The knowledge sources might include:

-   Getting-started guides
-   Academy management documentation
-   User permissions
-   Billing information
-   Troubleshooting instructions

A RAG assistant could use this architecture:

1.  Collect and index product documentation.
2.  Authenticate the user.
3.  Identify the tenant and permissions.
4.  Retrieve authorized content relevant to the question.
5.  Supply the retrieved content to the LLM.
6.  Return an answer with source references.

### Multi-tenant data isolation

Suppose Academy A and Academy B use the same SaaS product. Academy A has
private documents containing its subscription details. Academy B must
not be able to retrieve those documents.

An indexed chunk might contain:

``` js
{
  documentId: "doc_101",
  tenantId: "academy_A",
  visibility: "private",
  text: "Academy A's subscription details..."
}
```

The backend must enforce access control when retrieving information.

-   Shared documentation can be available to all authorized tenants.
-   Academy-specific documents require matching tenant authorization.
-   User-specific records require appropriate user-level permission.
-   Private information must never be placed into the prompt just
    because vector search returned it.

**Security rule:** Access control belongs in the application and
retrieval layer, not solely in the prompt.

------------------------------------------------------------------------

## 9. RAG vs. fine-tuning vs. a normal LLM

These concepts solve different problems.

  -----------------------------------------------------------------------
  Approach                What it changes         Best suited for
  ----------------------- ----------------------- -----------------------
  Normal LLM              Uses the model and      General reasoning,
                          supplied context        writing, and coding

  RAG                     Supplies relevant       Private documents,
                          external knowledge at   current policies,
                          query time              documentation

  Fine-tuning             Updates model           Adapting behavior,
                          parameters using        format, style, or task
                          training examples       patterns
  -----------------------------------------------------------------------

### Example: A customer-support AI

Suppose you want a chatbot to answer in a consistent support style and
use the latest refund policy.

A sensible approach might be:

-   Use a capable LLM for language understanding and generation.
-   Use RAG to supply the latest refund policy.
-   Consider fine-tuning only if you have evidence that prompting alone
    cannot reliably achieve the desired behavior.

Fine-tuning is not a reliable substitute for a searchable, updatable
knowledge base. It does not guarantee that a model will accurately
recall every fact.

RAG does not automatically teach the model a new skill or guarantee a
specific output format. RAG and fine-tuning can be combined when
justified.

### Check your understanding

**Scenario:** Your company changes its product pricing every month. You
want the chatbot to answer using the latest prices without retraining
the model every month.

The most direct fit is to retrieve current pricing information and
provide it to the LLM. The source and index must still be kept current.

------------------------------------------------------------------------

## 10. When should you use RAG, and when should you avoid it?

RAG is useful, but it is not the answer to every AI problem.

  -----------------------------------------------------------------------
  Use case                            Recommended approach
  ----------------------------------- -----------------------------------
  Ask questions about company PDFs    RAG

  Search a large technical            RAG
  documentation library               

  Chat with a private codebase        RAG, potentially combined with code
                                      search

  Answer questions about changing     RAG or direct retrieval from the
  product policies                    source

  Calculate a customer's current      Query the authorized database and
  invoice                             calculate

  Retrieve exact order status         Query the transactional database or
                                      API

  Generate code                       Usually an LLM; add retrieval for
                                      repository context when useful

  Consistently follow a specialized   Prompting first; fine-tuning if
  output style                        justified
  -----------------------------------------------------------------------

**RAG is not a replacement for a database or backend business logic.**

For example, if a user asks how much revenue their academy generated
yesterday, query the relevant transaction records, enforce
authorization, and calculate the result. Embeddings are not the right
mechanism for retrieving exact financial figures.

An AI application can combine RAG with SQL queries, APIs, and tools.
Each component should handle the work it is suited for.

------------------------------------------------------------------------

## 11. Limitations of RAG

### 1. Retrieval failure

The relevant document exists, but the system fails to retrieve it.
Causes can include poor chunking, weak embeddings, missing metadata, or
an unsuitable search strategy.

**Improvement:** Evaluate retrieval, experiment with chunking, and
consider hybrid search or reranking.

### 2. Outdated information

The original document changes, but the index still contains the old
version.

**Improvement:** Build an ingestion and re-indexing process, handle
document updates and deletions, and track source versions.

### 3. Incorrect generation

The retrieved evidence is correct, but the LLM misinterprets it or
introduces unsupported claims.

**Improvement:** Use clear grounding instructions, citations,
answerability checks, and evaluation tests. High-risk decisions need
appropriate verification.

### 4. Security and prompt injection

A retrieved document may contain malicious instructions, or the
retrieval system may expose unauthorized information.

**Improvement:** Enforce access control before content reaches the
model, treat retrieved text as untrusted data, and test for prompt
injection and cross-tenant data leakage.

### 5. Cost and latency

Parsing, embedding, retrieval, reranking, and generation all consume
resources.

**Improvement:** Cache appropriate results, batch document embeddings,
limit retrieved context, and measure end-to-end latency and cost.

------------------------------------------------------------------------

## 12. Building a RAG application as a full-stack developer

Start with a small document Q&A application rather than a large
enterprise knowledge platform.

### Project: Knowledge Assistant

Features:

-   Upload documents.
-   Ask questions about those documents.
-   Receive answers with source references.

### Suggested stack

  -----------------------------------------------------------------------
  Component                           Options
  ----------------------------------- -----------------------------------
  Frontend                            React or Next.js

  Backend                             Node.js or Python with FastAPI

  LLM                                 Hosted or local model

  Storage                             PostgreSQL with pgvector

  Document storage                    Local storage for a prototype;
                                      object storage for production
  -----------------------------------------------------------------------

Choose one stack and keep the first version small.

### Build it in five stages

#### Stage 1 --- Basic LLM application

Create an API endpoint that accepts a question, calls an LLM, and
returns its answer. This establishes the generation part.

#### Stage 2 --- Document ingestion

Accept a PDF or text file, extract its contents, split the text into
chunks, generate embeddings, and store the chunks.

#### Stage 3 --- Retrieval

Embed a user's question, search for relevant chunks, and return the top
results. Initially, inspect the retrieved chunks before involving the
LLM.

#### Stage 4 --- Grounded generation

Pass the question and retrieved chunks to the LLM. Ask it to answer
using the evidence and return source references.

#### Stage 5 --- Evaluation and production readiness

Test relevant and irrelevant questions, missing answers, outdated
documents, access control, latency, and cost. Add reranking or hybrid
search only where testing demonstrates a need.

### Conceptual backend pseudocode

``` js
async function answerQuestion(question, user) {
  // 1. Embed the user's question
  const queryVector = await embed(question);

  // 2. Retrieve only authorized chunks
  const chunks = await searchDocuments({
    queryVector,
    tenantId: user.tenantId,
    limit: 5
  });

  // 3. Check whether useful evidence was found
  if (!hasSufficientEvidence(chunks)) {
    return {
      answer: "I couldn't find sufficient information.",
      sources: []
    };
  }

  // 4. Generate an answer from the evidence
  const result = await generateAnswer({
    question,
    context: chunks
  });

  // 5. Return the answer and source references
  return {
    answer: result.answer,
    sources: chunks.map(chunk => chunk.documentId)
  };
}
```

This is conceptual pseudocode, not a complete implementation. The
functions are placeholders. In a real implementation,
`hasSufficientEvidence` needs a meaningful retrieval-quality or
answerability check, and access control must be enforced by the database
or trusted backend---not just by passing a `tenantId` into an arbitrary
function.

Retrieving five chunks does not guarantee that those chunks answer the
question. Measure retrieval quality.

------------------------------------------------------------------------

## 13. How do you know whether your RAG system is good?

Do not judge it only by whether the chatbot produces fluent answers.

  -----------------------------------------------------------------------
  Metric                              What it tells you
  ----------------------------------- -----------------------------------
  Retrieval Recall@k                  How often relevant evidence appears
                                      among the top `k` retrieved results

  Answer correctness / faithfulness   Whether the generated answer is
                                      correct and supported by the
                                      available evidence

  Latency and cost                    Whether the system is efficient
                                      enough for real users
  -----------------------------------------------------------------------

For example, prepare 50 test questions with known relevant document
chunks. Check whether the correct evidence appears in the top five
retrieval results. Then assess whether the answer uses that evidence
correctly.

Keep retrieval evaluation separate from answer evaluation. If retrieval
fails, changing the generation prompt alone will not fix the underlying
problem.

For production systems, also test citations, refusal behavior when
evidence is missing, permission boundaries, and document freshness.

------------------------------------------------------------------------

## 14. Final mental model

Remember these four components:

### 1. Knowledge base

Where the information comes from: documents, databases, and other
sources.

### 2. Retriever

Finds the most relevant, authorized information for a question.

### 3. LLM

Interprets the question and generates a response using the supplied
context.

### 4. Application layer

Controls permissions, validates inputs, manages sources, and evaluates
the answer.

The complete process is:

**Documents → Chunking → Embeddings → Search index → User query →
Retrieval → Context → LLM → Grounded answer.**

The indexing steps happen ahead of the query, while retrieval and
generation happen at query time.

------------------------------------------------------------------------

## Recommended learning order

1.  Understand embeddings and vector similarity.
2.  Learn chunking strategies.
3.  Implement vector retrieval and inspect the results.
4.  Add LLM generation grounded in retrieved context.
5.  Add citations, evaluation, access control, and document updates.
6.  Explore hybrid search and reranking after measuring the baseline.

Do not jump straight into a complex agent framework. First understand
why the system retrieves a particular passage. That understanding will
make you much better at debugging and improving a RAG application.
