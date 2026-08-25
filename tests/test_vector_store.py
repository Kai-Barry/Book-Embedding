import unittest
import numpy as np
import pandas as pd
from src.vector_store import BookVectorStore

class TestVectorStore(unittest.TestCase):
    def setUp(self):
        self.store = BookVectorStore()

    def test_store_initialization(self):
        self.assertTrue(self.store.is_persisted(), "Vector store should be persisted on disk")
        self.assertIsNotNone(self.store.df, "Metadata dataframe should be loaded")
        self.assertIsNotNone(self.store.embeddings, "Embedding matrix should be loaded")
        self.assertGreater(len(self.store.df), 0, "Corpus should have books")
        self.assertEqual(len(self.store.df), len(self.store.embeddings), "Row counts must match embeddings count")

    def test_vector_dimensions_and_normalization(self):
        dim = self.store.embeddings.shape[1]
        self.assertIn(dim, [768, 1024], f"Unexpected embedding dimension: {dim}")
        
        # Verify unit normalization on sample vectors
        sample_norms = np.linalg.norm(self.store.embeddings[:10], axis=1)
        for norm in sample_norms:
            self.assertAlmostEqual(norm, 1.0, places=3, msg="Embedding vector must be L2 unit normalized")

    def test_vector_search_cosine_similarity(self):
        if len(self.store.embeddings) > 0:
            query_vec = self.store.embeddings[0]
            results = self.store.search_by_vector(query_vec, top_k=5)
            self.assertEqual(len(results), 5)
            # The top result must be the book itself with ~1.0 similarity
            self.assertAlmostEqual(results[0]["similarity_score"], 1.0, places=2)

if __name__ == "__main__":
    unittest.main()
