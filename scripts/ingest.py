import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import time
import torch
from src.config import DEFAULT_LOCAL_MODEL, GEMINI_MODEL, BATCH_SIZE
from src.data_loader import BookDataLoader
from src.embedder import get_embedder
from src.vector_store import BookVectorStore

def main():
    parser = argparse.ArgumentParser(description="Ingest book dataset and compute dense vectors on GPU/API")
    parser.add_argument("--provider", type=str, default="local", choices=["local", "gemini"], help="Embedding provider")
    parser.add_argument("--model", type=str, default=None, help="Embedding model name override")
    parser.add_argument("--sample", type=int, default=None, help="Optional sample limit for quick testing (e.g. 1000)")
    parser.add_argument("--custom-csv", type=str, default=None, help="Path to custom Goodreads CSV file")
    parser.add_argument("--min-ratings", type=int, default=100, help="Minimum reader rating count filter for Goodreads books")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size for GPU encoding")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("[Book-Embedding] Data Ingestion & GPU Vector Pipeline")
    print("=" * 60)
    
    if torch.cuda.is_available():
        print(f"[GPU Detected] {torch.cuda.get_device_name(0)}")
        print(f"[VRAM Total] {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
    else:
        print("[Warning] CUDA GPU not detected. Using CPU.")

    # 1. Load Data
    t0 = time.time()
    if args.custom_csv:
        print(f"[1/3] Loading custom CSV dataset from: {args.custom_csv}")
        df = BookDataLoader.load_custom_csv(args.custom_csv)
    else:
        print(f"[1/3] Loading CMU & Goodreads 100k (min_ratings >= {args.min_ratings}) popular books...")
        df = BookDataLoader.load_cmu_books(max_records=args.sample, min_ratings=args.min_ratings)
        
    if args.sample and len(df) > args.sample:
        df = df.iloc[:args.sample].copy()
        
    print(f"Loaded {len(df)} cleaned popular book summaries in {time.time() - t0:.2f}s")
    
    # 2. Instantiate Embedder
    model_name = args.model or (DEFAULT_LOCAL_MODEL if args.provider == "local" else GEMINI_MODEL)
    print(f"[2/3] Initializing Embedder [{args.provider.upper()}] with model: {model_name}...")
    embedder = get_embedder(provider=args.provider, model_name=model_name)
    
    # 3. Compute Embeddings
    print(f"[3/3] Generating dense semantic embeddings for {len(df)} books (Batch size: {args.batch_size})...")
    t_embed_start = time.time()
    
    texts = df["embedding_text"].tolist()
    embeddings = embedder.embed_texts(texts, batch_size=args.batch_size)
    
    embed_duration = time.time() - t_embed_start
    print(f"[Success] Computed {embeddings.shape[0]} vectors of dimension {embeddings.shape[1]} in {embed_duration:.2f}s ({len(df)/embed_duration:.1f} books/sec)")
    
    # 4. Save to Vector Store
    vector_store = BookVectorStore()
    vector_store.save(df, embeddings, model_name=model_name)
    
    # 5. Build 2D UMAP Galaxy Coordinates
    print("[4/4] Generating 2D constellation coordinates (UMAP high-spread projection)...")
    try:
        vector_store.compute_2d_projection()
        print("[VectorStore] 2D Galaxy coordinates computed and saved.")
    except Exception as e:
        print(f"[VectorStore Warning] 2D projection generation skipped: {e}")
        
    # 6. Rebuild Collaborative Item2Vec Embeddings
    print("[CollaborativeEngine] Rebuilding Item2Vec co-reading graph embeddings for expanded catalog...")
    try:
        from src.collaborative import CollaborativeEngine
        collab = CollaborativeEngine()
        collab._build_seed_collaborative_embeddings()
        print("[CollaborativeEngine] Collaborative Item2Vec vectors successfully rebuilt.")
    except Exception as e:
        print(f"[CollaborativeEngine Warning] Collaborative rebuild skipped: {e}")

    print("=" * 60)
    print(f"[Complete] Ingestion & Indexing of {len(df)} popular books complete!")
    print("Run `python -m uvicorn src.api:app --reload` to start the API and Web UI.")

if __name__ == "__main__":
    main()
