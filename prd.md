# Product requirements: HR Policy Assistant

## Goal

Build a Python Streamlit app that lets a user upload one HR policy PDF and ask questions about its contents. The app uses retrieval augmented generation (RAG): PyMuPDF extracts text, Sentence Transformers creates embeddings, FAISS finds relevant passages, and the Groq API drafts answers grounded in those passages.

## Users and primary flow

The primary user is an employee or HR staff member looking for a policy answer. They open the app, upload a text based HR policy PDF, wait for indexing, ask a question, and receive a concise answer with references to the PDF's page numbers. They can ask follow up questions about the same uploaded document or replace it with a different PDF.

## MVP requirements

1. Accept one PDF at a time. Show the filename, page count, and indexing status. Reject unsupported, empty, corrupt, or textless PDFs with actionable messages. Scanned PDFs that require OCR are outside the MVP.
2. Extract page text with PyMuPDF while preserving source page numbers. Split usable text into overlapping chunks and attach document name, page number, and chunk ID as metadata.
3. Embed chunks locally with a Sentence Transformers model. Store normalized vectors in an in memory FAISS index scoped to the user's Streamlit session. Replacing the PDF replaces its index and clears prior conversation.
4. Retrieve the most relevant chunks for each question. Send only the question, bounded conversation context if used, and retrieved passages to Groq. Configure the model through `GROQ_MODEL` and the credential through `GROQ_API_KEY` or Streamlit secrets; never hardcode either credential.
5. Display an answer with page references that map to retrieved passages. If the document does not support an answer, say so plainly and do not invent policy details. Offer the retrieved source excerpts in an expandable area so users can check the evidence.
6. Give clear feedback for upload, extraction, embedding, retrieval, and Groq errors. Keep the app usable for another upload after an error.
7. Do not persist uploaded PDFs, extracted text, embeddings, questions, or answers to disk by default. Avoid logging sensitive document content or secrets.

## Quality and boundaries

- Answers must be grounded in the uploaded PDF. The assistant should distinguish a direct policy statement from an inference and recommend checking with HR when a policy is unclear or absent.
- Source page numbers must be 1 based and match the PDF viewer's page order. Citations are references to evidence, not a guarantee that the model's interpretation is correct.
- A missing Groq key may allow upload and indexing, but asking a question must show a clear setup message rather than crash.
- Initial limits: one PDF, up to 20 MB, and one session local index. These are implementation targets that can be adjusted after performance testing.
- The MVP does not support OCR, multiple document comparison, external policy lookup, user accounts, permanent chat history, or policy administration.
- This is an information aid, not an official HR decision maker. The interface should make verification against the policy easy.

## Acceptance criteria

- A user can upload a valid text based PDF, ask a question, and see an answer with the relevant page reference and source excerpt.
- A question whose answer is absent from the PDF gets an explicit insufficient evidence response.
- Uploading a second PDF removes the first PDF's searchable content and previous chat.
- A scanned or image only PDF, invalid PDF, missing key, and upstream API failure each produce a useful message without a broken session.
- No API key or document text is committed to the repository or included in error output.
