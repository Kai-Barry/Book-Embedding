import unittest
from src.vector_store import BookVectorStore
from src.recommender import BookRecommender

class TestRecommender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.store = BookVectorStore()
        cls.recommender = BookRecommender(cls.store, None)

    def test_search_catalog_titles(self):
        results = self.recommender.search_catalog_titles("Dune", limit=5)
        self.assertGreater(len(results), 0)
        self.assertTrue(any("dune" in r["title"].lower() for r in results))

    def test_recommend_similar_to_book(self):
        dune_matches = self.recommender.search_catalog_titles("Dune", limit=1)
        self.assertTrue(len(dune_matches) > 0)
        book_id = dune_matches[0]["id"]

        rec_data = self.recommender.recommend_similar_to_book(
            book_id_or_title=book_id,
            top_k=6,
            weight_plot=1.0,
            weight_tone=0.8,
            weight_style=0.5,
            weight_pacing=0.5,
            weight_community=1.0,
            boost_keywords=["Space & Cosmic Domain:2.0"],
            exclude_keywords=[]
        )

        results = rec_data.get("results", [])
        self.assertEqual(len(results), 6)
        self.assertIn("target_book", rec_data)
        self.assertIn("subclustered_motifs", rec_data)
        
        # Verify explainability decomposition
        first = results[0]
        self.assertIn("match_breakdown", first)
        self.assertIn("similarity_reasons", first)
        self.assertIn("plot_pct", first["match_breakdown"])

    def test_recommend_from_profile_multi_book(self):
        history = [
            {"title": "Dune", "rating": 5.0, "liked_aspects": ["world_building", "philosophical"]},
            {"title": "Frankenstein", "rating": 5.0, "liked_aspects": ["philosophical", "dark_atmosphere"]},
            {"title": "Dracula", "rating": 4.0, "liked_aspects": ["dark_atmosphere"]}
        ]

        res = self.recommender.recommend_from_profile(history, top_k=6)
        results = res.get("results", [])
        self.assertEqual(len(results), 6)
        self.assertIn("taste_dna", res)
        self.assertIn("taste_archetype", res["taste_dna"])
        self.assertIn("top_genres", res["taste_dna"])

        # Check attribution influences
        first = results[0]
        self.assertIn("top_influences", first)
        self.assertGreater(len(first["top_influences"]), 0)

if __name__ == "__main__":
    unittest.main()
