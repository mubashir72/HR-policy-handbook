import unittest

import pymupdf

from src.pdf_processing import PdfProcessingError, extract_pdf_pages, validate_pdf_upload


class PdfProcessingTests(unittest.TestCase):
    def test_extracts_text_and_preserves_one_based_page_numbers(self):
        document = pymupdf.open()
        first_page = document.new_page()
        first_page.insert_text((72, 72), "Annual leave is 20 days.")
        second_page = document.new_page()
        second_page.insert_text((72, 72), "Sick leave must be reported.")
        content = document.tobytes()
        document.close()

        pages = extract_pdf_pages(content)

        self.assertEqual([page.page_number for page in pages], [1, 2])
        self.assertIn("Annual leave", pages[0].text)
        self.assertIn("Sick leave", pages[1].text)

    def test_rejects_non_pdf_extension(self):
        with self.assertRaises(PdfProcessingError):
            validate_pdf_upload("policy.txt", b"not a PDF")


if __name__ == "__main__":
    unittest.main()
