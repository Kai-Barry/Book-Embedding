import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import time
from src.vector_store import BookVectorStore
from src.embedder import get_embedder
from src.recommender import BookRecommender

def test_pipeline():
    print("Testing Book-Embedding Vector & Similarity Pipeline...")
    store = BookVectorStore()
    embedder = get_embedder("local")
    rec = BookRecommender(store, embedder)

    print("\n--- TEST 1: Semantic Natural Language Search ---")
    query = "cyberpunk detectives and artificial intelligence in futuristic mega city"
    t0 = time.perf_counter()
    results = rec.search_books_by_text(query, top_k=5)
    lat = (time.perf_counter() - t0) * 1000.0
    print(f"Query: '{query}' (Latency: {lat:.1f}ms)")
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['title']} by {r['author']} | Match: {r['similarity_score']*100:.1f}% | Genres: {r['genres']}")

    print("\n--- TEST 2: Book-to-Book Similarity (Target: Dune) ---")
    t0 = time.perf_counter()
    data_dune = rec.recommend_similar_to_book("Dune", top_k=5)
    lat = (time.perf_counter() - t0) * 1000.0
    print(f"Target: Dune (Latency: {lat:.1f}ms)")
    for i, r in enumerate(data_dune.get("results", []), 1):
        print(f"  {i}. {r['title']} by {r['author']} | Match: {r['similarity_score']*100:.1f}% | Genres: {r['genres']}")

    print("\n--- TEST 3: Book-to-Book Similarity (Target: Dracula) ---")
    data_drac = rec.recommend_similar_to_book("Dracula", top_k=5)
    for i, r in enumerate(data_drac.get("results", []), 1):
        print(f"  {i}. {r['title']} by {r['author']} | Match: {r['similarity_score']*100:.1f}% | Genres: {r['genres']}")

    print("\nAll verification tests completed successfully!")

if __name__ == "__main__":
    test_pipeline()
