# Project architecture

## Data flow

```text
PDF upload (Streamlit)
  -> validate type and size
  -> PyMuPDF page text extraction
  -> normalize and chunk text with page metadata
  -> Sentence Transformers embeddings
  -> normalized FAISS index in session state

Question (Streamlit)
  -> embed question with the same model
  -> FAISS top-k search
  -> build evidence bounded Groq prompt
  -> answer with page citations and inspectable excerpts
```

## Planned modules

| Module | Responsibility |
| --- | --- |
| `app.py` | Streamlit page, uploader, chat UI, status, and session lifecycle. |
| `src/pdf_processing.py` | Validate PDF bytes; extract page text and page metadata with PyMuPDF. |
| `src/chunking.py` | Normalize text and split it into overlapping, traceable chunks. |
| `src/retrieval.py` | Load the embedding model, create normalized embeddings, build/query the FAISS index, return chunks with scores. |
| `src/answering.py` | Assemble grounded prompts, call Groq, validate or attach source references, handle insufficient evidence. |
| `src/config.py` | Read validated configuration and secrets. |
| `tests/` | Focused tests for extraction, chunk metadata, retrieval mapping, and answer formatting. |
| `requirements.txt` | Pinned or bounded Python dependencies. |
| `.streamlit/config.toml` | Optional theme and nonsecret UI settings. |

These are planned files; this documentation pass creates none of the application modules.

## Retrieval design

- Start with `sentence-transformers/all-MiniLM-L6-v2`, subject to compatibility with the chosen Python environment. Load it once with Streamlit resource caching.
- Start with approximately 800 characters per chunk and 120 characters of overlap. Prefer paragraph boundaries where practical; never combine text from different PDF pages in one chunk.
- L2 normalize document and query embeddings and use FAISS `IndexFlatIP` for cosine equivalent ranking. Maintain a parallel metadata list whose position matches each FAISS vector ID.
- Retrieve up to four chunks per question. Bound both chunk count and total prompt length so long PDFs cannot create unbounded Groq requests.
- Record source identifiers such as `document filename, page, chunk ID`. Show page citations only for passages actually supplied to the answer call. Treat similarity as ranking, not proof of relevance; instruct the model to abstain when evidence is inadequate.

## State and configuration

- Keep uploaded bytes only as long as needed to extract and index. Keep the index, chunk metadata, PDF identity, and chat messages in `st.session_state` so users' documents stay separated.
- Cache the shared embedding model, but do not put user PDF content or its index into a global cache. Reindex only when the uploaded file identity changes, using a content hash to detect replacement.
- Read `GROQ_API_KEY` from the process environment or Streamlit secrets. Read the target model from `GROQ_MODEL`; document a currently available value during implementation instead of embedding an assumed permanent model ID here.
- Never write PDF text, embeddings, key, or chat content to application logs or persistent files by default.

## Failure handling

- Validate extension, MIME where available, byte size, and whether PyMuPDF can open the file. Detect zero extractable text and explain the OCR limitation.
- Catch embedding and Groq errors at their boundaries. Present a short user facing error and keep technical details out of the page and logs when they may contain sensitive text.
- Keep each response tied to the active document identity so a changed upload cannot display an answer based on a previous document.
