import unittest

from src.chunking import chunk_pages
from src.pdf_processing import ExtractedPage


class ChunkingTests(unittest.TestCase):
    def test_preserves_pages_and_creates_overlapping_chunks(self):
        pages = [
            ExtractedPage(page_number=1, text="A" * 50),
            ExtractedPage(page_number=2, text="B" * 20),
        ]

        chunks = chunk_pages(pages, "policy.pdf", chunk_size=30, overlap=10)

        self.assertEqual([chunk.page_number for chunk in chunks], [1, 1, 2])
        self.assertEqual(chunks[0].chunk_id, "p1-c1")
        self.assertEqual(chunks[1].chunk_id, "p1-c2")
        self.assertEqual(chunks[2].document_name, "policy.pdf")
        self.assertTrue(chunks[0].text[-10:] in chunks[1].text)

    def test_rejects_invalid_overlap(self):
        pages = [ExtractedPage(page_number=1, text="Policy text")]
        with self.assertRaises(ValueError):
            chunk_pages(pages, "policy.pdf", chunk_size=10, overlap=10)


if __name__ == "__main__":
    unittest.main()
