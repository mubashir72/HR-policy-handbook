# Project context

## Request and scope

The user wants an HR policy assistant built with Python, Streamlit, a Groq API key, FAISS, Sentence Transformers, and PyMuPDF. The intended interaction is to upload an HR policy PDF and ask questions about it. The current request is limited to creating six documentation files: `prd.md`, `architecture.md`, `rules.md`, `design.md`, `tasks.md`, and `memory.md`.

## Decisions recorded for implementation

- MVP handles one text based PDF per session; OCR and multiple document search are later possibilities.
- Uploading a new PDF resets the index and conversation.
- Retrieval is local with Sentence Transformers embeddings and an in memory FAISS index. Groq generates the final answer from retrieved passages.
- Answers show 1 based PDF page references and inspectable source excerpts, and explicitly abstain when evidence is insufficient.
- Prefer session scoped document data and no persistence of uploaded content or chat by default.
- Store the API key in environment or Streamlit secrets; keep the Groq model configurable.
- Initial implementation targets are a 20 MB PDF limit, about 800 character chunks with 120 character overlap, and up to four retrieved chunks. Validate these during implementation.

## Repository state

The workspace was empty when documentation work began. Application code and dependency files are future work tracked in `tasks.md`.

## Open implementation choices

- Verify a mutually supported Python and package version set before installing dependencies.
- Select an available Groq model at implementation time and document the required `GROQ_MODEL` value.
- Tune chunk size, prompt bounds, and retrieval relevance with representative policy PDFs.
