import unittest
from src.data_enricher import DataEnricher, data_enricher

class TestDataEnricher(unittest.TestCase):
    def setUp(self):
        self.enricher = data_enricher

    def test_series_detection(self):
        tests = [
            ("Dune (Dune Chronicles #1)", "Dune Chronicles", "#1"),
            ("Foundation and Empire (Foundation, Book 2)", "Foundation", "#2"),
            ("Harry Potter and the Goblet of Fire (Harry Potter #4)", "Harry Potter", "#4")
        ]
        for title, expected_series, expected_vol in tests:
            res = DataEnricher.detect_series(title)
            self.assertIsNotNone(res, f"Failed detecting series for '{title}'")
            self.assertIn(expected_series.lower(), res["series"].lower())
            self.assertEqual(res["volume"], expected_vol)

    def test_popularity_profile(self):
        # Known global phenomenon
        res_global = DataEnricher.compute_popularity_profile("Dune", 150000, 4.3)
        self.assertEqual(res_global["tier"], "Global Phenomenon")
        self.assertGreaterEqual(res_global["score"], 90)

        # Deterministic fallback
        res_fallback = DataEnricher.compute_popularity_profile("Unknown Book 123", None, None)
        self.assertIn(res_fallback["tier"], ["Bestseller Classic", "Popular Favorite", "Hidden Gem", "Cult Gem"])
        self.assertGreater(res_fallback["score"], 0)

    def test_bolster_book_in_memory(self):
        raw_book = {
            "id": "test_1",
            "title": "Foundation (Foundation #1)",
            "author": "Isaac Asimov",
            "summary": "Hari Seldon creates psychohistory.",
            "genres": "Science Fiction"
        }
        enriched = self.enricher.bolster_book(raw_book, fetch_online=False)
        self.assertIn("series_info", enriched)
        self.assertIn("popularity", enriched)
        self.assertIn("readability", enriched)

if __name__ == "__main__":
    unittest.main()
