import unittest
import numpy as np
from src.collaborative import collaborative_engine

class TestCollaborativeEngine(unittest.TestCase):
    def setUp(self):
        self.collab = collaborative_engine

    def test_collaborative_initialization(self):
        self.assertTrue(self.collab.has_embeddings(), "Collaborative engine should have loaded vectors")
        self.assertIsNotNone(self.collab.vectors)
        self.assertGreater(len(self.collab.vectors), 0)
        self.assertEqual(self.collab.vectors.shape[1], 128, "Item2Vec vector dim should be 128")

    def test_get_collaborative_vector(self):
        first_id = list(self.collab.id_to_idx.keys())[0]
        vec = self.collab.get_embedding(first_id)
        self.assertIsNotNone(vec)
        self.assertEqual(len(vec), 128)
        self.assertAlmostEqual(float(np.linalg.norm(vec)), 1.0, places=3)

    def test_score_all(self):
        dummy_query = np.random.randn(128).astype(np.float32)
        dummy_query /= np.linalg.norm(dummy_query)
        scores = self.collab.score_all(dummy_query)
        self.assertEqual(len(scores), len(self.collab.vectors))
        self.assertTrue(np.all(scores >= 0.35) and np.all(scores <= 1.0), "Scores should be rescaled appropriately")

    def test_get_collaborative_scores(self):
        ids = list(self.collab.id_to_idx.keys())[:5]
        target_id = ids[0]
        candidate_ids = ids[1:]
        scores = self.collab.get_collaborative_scores(target_id, candidate_ids)
        self.assertEqual(len(scores), 4)

if __name__ == "__main__":
    unittest.main()
