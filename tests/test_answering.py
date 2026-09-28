import unittest

from src.answering import build_evidence
from src.chunking import TextChunk
from src.retrieval import RetrievalResult


class AnsweringTests(unittest.TestCase):
    def test_evidence_has_page_labels_and_is_bounded(self):
        results = [
            RetrievalResult(
                chunk=TextChunk("p3-c1", "policy.pdf", 3, "Leave policy details"),
                score=0.9,
            ),
            RetrievalResult(
                chunk=TextChunk("p4-c1", "policy.pdf", 4, "More policy details"),
                score=0.8,
            ),
        ]

        evidence = build_evidence(results, max_characters=40)

        self.assertIn("[Page 3 | p3-c1]", evidence)
        self.assertLessEqual(len(evidence), 42)


if __name__ == "__main__":
    unittest.main()
