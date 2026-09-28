# Tasks and progress

## Documentation

- [x] Define product requirements in `prd.md`.
- [x] Define the planned system architecture in `architecture.md`.
- [x] Define coding and privacy rules in `rules.md`.
- [x] Define the UI direction in `design.md`.
- [x] Record project context in `memory.md`.

## Implementation backlog

- [x] Create `requirements.txt`, `.gitignore`, and a setup guide. Python 3.11 or 3.12 is recommended for a fresh environment.
- [x] Build PDF validation and per-page extraction with PyMuPDF.
- [x] Implement page preserving chunking and metadata.
- [x] Load the Sentence Transformers model and build/query an in memory FAISS index.
- [x] Implement Groq configuration, grounded prompting, abstention, and source references.
- [x] Build the Streamlit upload, indexing, chat, source excerpt, and error states.
- [x] Verify reset behavior in the session state implementation when a new PDF is uploaded.
- [x] Run automated checks for chunk provenance, bounded evidence, PDF extraction, module imports, and Streamlit startup.
- [ ] Run manual checks with a representative PDF: present answer, absent answer, image only PDF, missing key, and Groq failure.
- [ ] Visually review desktop and narrow layouts with a browser.

## Current status

Application code, setup files, and focused unit tests are complete. Manual browser validation requires a representative text-based HR policy PDF.
