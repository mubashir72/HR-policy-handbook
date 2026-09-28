# HR Policy Assistant

Ask clear questions about an HR policy PDF and receive evidence-based answers with page references. The app uses local retrieval with PyMuPDF, Sentence Transformers, and FAISS; Groq generates the final answer from the passages found in the uploaded document.

> This project is a policy information tool. Check the cited source text and confirm unclear or sensitive matters with your HR team.

## What you can do

- Upload one text-based HR policy PDF up to 20 MB.
- Ask everyday questions such as “How much annual leave do I receive?”
- Read answers with page citations and expandable source excerpts.
- Replace the document at any time; the app clears the prior index and conversation.
- Keep uploaded content and chat history inside the active browser session by default.

## Quick start

Use Python 3.11 or 3.12 for a fresh setup. Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` file in the project folder:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

`GROQ_MODEL` is optional; `openai/gpt-oss-20b` is the default. You may also use environment variables or `.streamlit/secrets.toml`. These credential files are ignored by Git.

Start the app:

```powershell
streamlit run app.py
```

Open the local address shown in the terminal, upload a PDF, wait for the **Policy ready** message, and ask a question.

## Try it with the sample handbook

The project includes a fictional policy document at `output/pdf/sample_hr_policy_handbook.pdf`.

Upload it and try these questions:

| Question | Expected evidence |
| --- | --- |
| How much annual leave do full-time employees receive? | 20 paid working days per year; page 6. |
| When should I tell my manager I will be absent? | As soon as possible and no later than 30 minutes before the scheduled start time; page 5. |
| What is required for remote work? | Manager approval, availability during core hours, approved tools, and secure handling of data; page 8. |
| Can I use my personal email for company files? | No; approved company accounts and storage must be used; page 10. |

## Supported and unsupported PDFs

| Works well | Needs preparation or is unsupported |
| --- | --- |
| Text-based PDFs with selectable text | Scanned or image-only PDFs without OCR |
| One policy document per session | Multiple documents in one search |
| English policy content | Permanent document or chat storage |

## Troubleshooting

| Message or symptom | What to do |
| --- | --- |
| “This PDF has no readable text” | Use a text-based PDF or OCR the scan first. |
| “Groq rejected the API key” | Update `GROQ_API_KEY` in `.env`, environment variables, or Streamlit secrets. |
| “The configured Groq model is unavailable” | Set `GROQ_MODEL=openai/gpt-oss-20b`, then restart Streamlit. |
| The first upload is slow | The embedding model downloads and loads on its first use. Later uploads use the cached model. |

## Run checks

```powershell
python -m unittest discover -s tests -v
```

## Project structure

```text
app.py                    Streamlit interface and session workflow
src/pdf_processing.py     PDF validation and per-page extraction
src/chunking.py           Page-preserving text chunks
src/retrieval.py          Sentence Transformer embeddings and FAISS search
src/answering.py          Grounded Groq prompts and error messages
output/pdf/               Sample policy handbook
tests/                    Focused unit tests
```
