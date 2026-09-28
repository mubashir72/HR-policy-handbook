"""Safe, page-preserving PDF text extraction."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import pymupdf

from src.config import MAX_EXTRACTED_CHARACTERS, MAX_UPLOAD_BYTES


class PdfProcessingError(ValueError):
    """Raised when an uploaded PDF cannot be used for retrieval."""


@dataclass(frozen=True)
class ExtractedPage:
    page_number: int
    text: str


def validate_pdf_upload(filename: str, content: bytes) -> None:
    if not filename.lower().endswith(".pdf"):
        raise PdfProcessingError("Please upload a PDF file.")
    if not content:
        raise PdfProcessingError("The uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise PdfProcessingError("This PDF is larger than the 20 MB upload limit.")


def extract_pdf_pages(content: bytes) -> list[ExtractedPage]:
    """Extract readable text from every PDF page without saving user data to disk."""
    try:
        document = pymupdf.open(stream=content, filetype="pdf")
    except (pymupdf.FileDataError, RuntimeError, ValueError) as error:
        raise PdfProcessingError("The uploaded file is not a readable PDF.") from error

    pages: list[ExtractedPage] = []
    character_count = 0
    try:
        for page_number, page in enumerate(document, start=1):
            text = " ".join(page.get_text("text").split())
            character_count += len(text)
            if character_count > MAX_EXTRACTED_CHARACTERS:
                raise PdfProcessingError(
                    "This PDF contains too much extractable text for the current limit."
                )
            if text:
                pages.append(ExtractedPage(page_number=page_number, text=text))
    finally:
        document.close()

    if not pages:
        raise PdfProcessingError(
            "This PDF has no readable text. Please upload a text-based PDF; scanned PDFs need OCR."
        )
    return pages
