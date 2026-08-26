import unittest
from fastapi.testclient import TestClient
from src.api import app

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_status_endpoint(self):
        res = self.client.get("/api/status")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ready")
        self.assertIn("gpu", data)
        self.assertIn("index", data)
        self.assertGreater(data["index"]["books_count"], 0)

    def test_catalog_autocomplete(self):
        res = self.client.get("/api/catalog?q=Dune&limit=5")
        self.assertEqual(res.status_code, 200)
        books = res.json()
        self.assertIsInstance(books, list)
        self.assertGreater(len(books), 0)

    def test_similar_endpoint(self):
        # Search a book first
        cat_res = self.client.get("/api/catalog?q=Dune&limit=1")
        self.assertEqual(cat_res.status_code, 200)
        book_id = cat_res.json()[0]["id"]

        sim_res = self.client.get(f"/api/similar/{book_id}?top_k=4")
        self.assertEqual(sim_res.status_code, 200)
        data = sim_res.json()
        self.assertIn("results", data)
        self.assertEqual(len(data["results"]), 4)

    def test_profile_recommend_endpoint(self):
        payload = {
            "history": [
                {"id": "cmu_6628", "rating": 5.0, "liked_aspects": ["world_building", "philosophical"]},
                {"title": "Frankenstein", "rating": 4.0, "liked_aspects": ["dark_atmosphere"]}
            ],
            "top_k": 4
        }
        res = self.client.post("/api/recommend/profile", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("results", data)
        self.assertIn("taste_dna", data)
        self.assertEqual(len(data["results"]), 4)

    def test_genres_endpoint(self):
        res = self.client.get("/api/genres")
        self.assertEqual(res.status_code, 200)
        genres = res.json()
        self.assertIsInstance(genres, list)

    def test_single_cover_endpoint(self):
        cat_res = self.client.get("/api/catalog?q=Dune&limit=1")
        self.assertEqual(cat_res.status_code, 200)
        book_id = cat_res.json()[0]["id"]

        cover_res = self.client.get(f"/api/cover/{book_id}")
        self.assertEqual(cover_res.status_code, 200)
        data = cover_res.json()
        self.assertEqual(data["book_id"], book_id)
        self.assertIn("has_cover", data)

    def test_batch_covers_endpoint(self):
        payload = {
            "books": [
                {"id": "cmu_6628", "title": "Dune", "author": "Frank Herbert"},
                {"id": "cmu_71416", "title": "Paul of Dune", "author": "Kevin J. Anderson"}
            ]
        }
        res = self.client.post("/api/covers/batch", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("covers", data)
        self.assertIsInstance(data["covers"], dict)

if __name__ == "__main__":
    unittest.main()
