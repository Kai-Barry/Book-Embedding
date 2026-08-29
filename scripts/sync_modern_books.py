import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from src.config import VECTOR_DB_DIR
from src.embedder import get_embedder
from src.modern_loader import CURATED_MODERN_BOOKS
from src.vector_store import BookVectorStore

def sync_rich_modern_books():
    print("=" * 60)
    print("Syncing Rich Modern Bestsellers into Vector Database")
    print("=" * 60)

    store = BookVectorStore()
    embedder = get_embedder("local")

    print(f"Initial store size: {len(store.df)} books")

    df = store.df.copy()
    embeddings = store.embeddings.copy()

    for book in CURATED_MODERN_BOOKS:
        b_id = book["id"]
        b_title = book["title"]
        b_summary = book["summary"]
        b_embed_text = book["embedding_text"]

        print(f"\nProcessing '{b_title}' (ID: {b_id})...")
        print(f"  Summary Length: {len(b_summary)} chars ({len(b_summary.split())} words)")

        # Compute high-density GPU embedding
        new_vec = embedder.embed_texts([b_embed_text])[0]

        # Check if ID or Title exists
        match = df[(df["id"].astype(str) == str(b_id)) | (df["title"].str.lower() == str(b_title).lower())]

        if not match.empty:
            idx = match.index[0]
            print(f"  -> Updating existing record at index {idx}")
            for k, v in book.items():
                if k in df.columns:
                    df.at[idx, k] = v
            embeddings[idx] = new_vec
        else:
            print(f"  -> Appending new record to database")
            new_row = {col: None for col in df.columns}
            for k, v in book.items():
                if k in df.columns:
                    new_row[k] = v
                else:
                    df[k] = None
                    new_row[k] = v
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            embeddings = np.vstack([embeddings, new_vec[np.newaxis, :]])

    # Update in-memory store and save
    store.df = df
    store.embeddings = embeddings.astype(np.float32)
    store.save()
    print("\n" + "=" * 60)
    print(f"Successfully synced all {len(CURATED_MODERN_BOOKS)} modern books! Final DB count: {len(store.df)}")
    print("=" * 60)

if __name__ == "__main__":
    sync_rich_modern_books()
