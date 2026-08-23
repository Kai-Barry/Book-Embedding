import os
import json
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from src.config import VECTOR_DB_DIR

class BookVectorStore:
    """
    High-performance in-memory and disk-persisted Vector Store.
    Stores book metadata and normalized embedding vectors for instant Cosine Similarity calculation.
    """
    
    def __init__(self, index_name: str = "book_index"):
        self.index_name = index_name
        self.db_dir = VECTOR_DB_DIR / index_name
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.db_dir / "metadata.parquet"
        self.vectors_file = self.db_dir / "embeddings.npy"
        self.config_file = self.db_dir / "index_config.json"
        
        self.df: Optional[pd.DataFrame] = None
        self.embeddings: Optional[np.ndarray] = None
        self.config: Dict[str, Any] = {}
        
        if self.is_persisted():
            self.load()

    def is_persisted(self) -> bool:
        return self.metadata_file.exists() and self.vectors_file.exists()

    def save(self, df: pd.DataFrame, embeddings: np.ndarray, model_name: str):
        """Saves metadata and dense embeddings to disk."""
        self.df = df.copy()
        self.embeddings = np.ascontiguousarray(embeddings, dtype=np.float32)
        
        # Save dataframe without huge raw texts if needed, but retain summary & metadata
        self.df.to_parquet(self.metadata_file, index=False)
        np.save(self.vectors_file, self.embeddings)
        
        self.config = {
            "count": len(df),
            "dimension": int(self.embeddings.shape[1]),
            "model_name": model_name
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)
            
        print(f"[VectorStore] Saved {len(df)} records with {self.config['dimension']}-dim vectors to {self.db_dir}")

    def load(self):
        """Loads index and metadata into memory."""
        if not self.is_persisted():
            raise FileNotFoundError(f"No persisted index found at {self.db_dir}")
            
        self.df = pd.read_parquet(self.metadata_file)
        self.embeddings = np.load(self.vectors_file)
        
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
                
        print(f"[VectorStore] Loaded {len(self.df)} books and embedding matrix {self.embeddings.shape}")

    def search_by_vector(self, query_vector: np.ndarray, top_k: int = 10, genre_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Calculates cosine similarities against all stored vectors and returns top_k matches.
        Since vectors are L2 normalized, cosine similarity is simply the dot product.
        """
        if self.embeddings is None or self.df is None:
            raise ValueError("Vector store is empty. Ingest data first.")
            
        # Ensure query vector is 1D and normalized
        q_norm = np.linalg.norm(query_vector)
        if q_norm > 0:
            query_vector = query_vector / q_norm
            
        # Matrix multiplication for instant cosine similarity across all books (Dot Product)
        scores = np.dot(self.embeddings, query_vector)
        
        # Apply genre filter if provided
        if genre_filter and genre_filter.strip():
            genre_lower = genre_filter.strip().lower()
            mask = self.df["genres"].str.lower().str.contains(genre_lower, na=False)
            filtered_indices = np.where(mask)[0]
            if len(filtered_indices) == 0:
                return []
            filtered_scores = scores[filtered_indices]
            # Top-k in filtered partition
            top_partition = np.argsort(filtered_scores)[::-1][:top_k]
            top_indices = filtered_indices[top_partition]
            top_scores = filtered_scores[top_partition]
        else:
            # Top-k over entire dataset
            if top_k >= len(scores):
                top_indices = np.argsort(scores)[::-1]
            else:
                # Fast argpartition followed by sort
                partitioned = np.argpartition(scores, -top_k)[-top_k:]
                top_indices = partitioned[np.argsort(scores[partitioned])[::-1]]
            top_scores = scores[top_indices]

        results = []
        coords_file = self.db_dir / "coords_2d.npy"
        coords = np.load(coords_file) if coords_file.exists() and len(np.load(coords_file)) == len(self.df) else None

        for idx, score in zip(top_indices, top_scores):
            r = self.df.iloc[idx]
            pt_x = float(coords[idx][0]) if coords is not None else 0.0
            pt_y = float(coords[idx][1]) if coords is not None else 0.0
            results.append({
                "id": str(r["id"]),
                "title": str(r["title"]),
                "author": str(r["author"]),
                "pub_date": str(r["pub_date"]),
                "genres": str(r["genres"]),
                "summary": str(r["summary"]),
                "similarity_score": float(score),
                "x": round(pt_x, 2),
                "y": round(pt_y, 2)
            })
        return results
            
    def perform_weighted_search(
        self,
        base_vector: np.ndarray,
        concept_query_vector: Optional[np.ndarray] = None,
        top_k: int = 12,
        weight_plot: float = 1.0,
        weight_concept: float = 0.5,
        genre_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes a global re-search across all 25,101 books combining base content embedding
        and active thematic/stylistic concept queries via vectorized GPU/NumPy operations.
        """
        if self.embeddings is None or self.df is None:
            return []

        # Vectorized dot product across all 25,101 books
        base_scores = np.dot(self.embeddings, base_vector)

        if concept_query_vector is not None and weight_concept > 0:
            concept_scores = np.dot(self.embeddings, concept_query_vector)
            total_w = max(0.1, weight_plot + weight_concept)
            composite_scores = (base_scores * weight_plot + concept_scores * weight_concept) / total_w
        else:
            composite_scores = base_scores

        # Genre filtering
        if genre_filter and genre_filter.strip():
            genre_lower = genre_filter.strip().lower()
            mask = self.df["genres"].str.lower().str.contains(genre_lower, na=False)
            filtered_indices = np.where(mask)[0]
            if len(filtered_indices) == 0:
                return []
            filtered_scores = composite_scores[filtered_indices]
            top_partition = np.argsort(filtered_scores)[::-1][:top_k]
            top_indices = filtered_indices[top_partition]
            top_scores = filtered_scores[top_partition]
        else:
            if top_k >= len(composite_scores):
                top_indices = np.argsort(composite_scores)[::-1]
            else:
                partitioned = np.argpartition(composite_scores, -top_k)[-top_k:]
                top_indices = partitioned[np.argsort(composite_scores[partitioned])[::-1]]
            top_scores = composite_scores[top_indices]

        coords_file = self.db_dir / "coords_2d.npy"
        coords = np.load(coords_file) if coords_file.exists() and len(np.load(coords_file)) == len(self.df) else None

        results = []
        for idx, score in zip(top_indices, top_scores):
            r = self.df.iloc[idx]
            pt_x = float(coords[idx][0]) if coords is not None else 0.0
            pt_y = float(coords[idx][1]) if coords is not None else 0.0
            results.append({
                "id": str(r["id"]),
                "title": str(r["title"]),
                "author": str(r["author"]),
                "pub_date": str(r["pub_date"]),
                "genres": str(r["genres"]),
                "summary": str(r["summary"]),
                "similarity_score": float(base_scores[idx]),
                "weighted_score": float(score),
                "x": round(pt_x, 2),
                "y": round(pt_y, 2)
            })
        return results

    def compute_2d_projection(self, n_neighbors: int = 30, min_dist: float = 0.45, spread: float = 1.6) -> np.ndarray:
        """
        Computes 2D UMAP projection with tuned repulsion and spread to eliminate overlapping point clusters.
        """
        coords_file = self.db_dir / "coords_2d.npy"
        if coords_file.exists():
            coords = np.load(coords_file)
            if len(coords) == len(self.embeddings):
                return coords

        print(f"[VectorStore] Computing high-spread 2D projection for {len(self.embeddings)} vectors (repulsion min_dist={min_dist}, spread={spread})...")
        try:
            import umap
            reducer = umap.UMAP(
                n_neighbors=n_neighbors, 
                min_dist=min_dist, 
                spread=spread,
                n_components=2, 
                metric="cosine", 
                random_state=42
            )
            coords = reducer.fit_transform(self.embeddings)
        except Exception as e:
            print(f"[VectorStore] UMAP reduction fallback due to: {e}")
            from sklearn.manifold import TSNE
            tsne = TSNE(n_components=2, perplexity=35, random_state=42)
            coords = tsne.fit_transform(self.embeddings[:min(5000, len(self.embeddings))])

        # Normalize coordinates between -100 and 100 for canvas scaling
        mins = coords.min(axis=0)
        maxs = coords.max(axis=0)
        norm_coords = (coords - mins) / (maxs - mins + 1e-9) * 200 - 100
        np.save(coords_file, norm_coords.astype(np.float32))
        return norm_coords

    def add_book_vector(self, book_data: Dict[str, Any], vector: np.ndarray):
        """Dynamically appends a new book and its embedding vector into the store."""
        if self.df is None or self.embeddings is None:
            raise ValueError("Store not initialized")

        # Check if already exists
        if (self.df["title"].str.lower() == book_data["title"].lower()).any():
            return

        vector = vector.reshape(1, -1).astype(np.float32)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm

        new_row = pd.DataFrame([{
            "id": book_data.get("id", f"dynamic_{len(self.df)}"),
            "title": book_data["title"],
            "author": book_data.get("author", "Unknown"),
            "pub_date": str(book_data.get("pub_date", "Unknown")),
            "genres": book_data.get("genres", "General"),
            "genre_list": book_data.get("genre_list", ["General"]),
            "summary": book_data.get("summary", ""),
            "embedding_text": book_data.get("embedding_text", "")
        }])

        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.embeddings = np.vstack([self.embeddings, vector])
        self.save(self.df, self.embeddings, model_name=self.config.get("model_name", "BAAI/bge-large-en-v1.5"))
        
        # Remove cached 2D coords to trigger recomputation on next view
        coords_file = self.db_dir / "coords_2d.npy"
        if coords_file.exists():
            coords_file.unlink()

    def get_visualization_data(self, max_points: int = 1500) -> List[Dict[str, Any]]:
        """Returns 2D galaxy point data for visualization."""
        if self.embeddings is None or self.df is None:
            return []

        coords = self.compute_2d_projection()
        total = len(self.df)
        step = max(1, total // max_points)
        indices = list(range(0, total, step))[:max_points]

        points = []
        for idx in indices:
            row = self.df.iloc[idx]
            points.append({
                "id": str(row["id"]),
                "title": str(row["title"]),
                "author": str(row["author"]),
                "genres": str(row["genres"]),
                "pub_date": str(row["pub_date"]),
                "summary": str(row["summary"])[:200] + "...",
                "x": round(float(coords[idx][0]), 2),
                "y": round(float(coords[idx][1]), 2)
            })
        return points

    def get_book_info_with_coords(self, book_id_or_title: str) -> Optional[Dict[str, Any]]:
        """Returns full metadata and 2D coordinates for a given book."""
        if self.df is None:
            return None
        matches = self.df.index[
            (self.df["id"] == book_id_or_title) | 
            (self.df["title"].str.lower() == book_id_or_title.lower())
        ].tolist()
        if not matches:
            return None
            
        idx = matches[0]
        row = self.df.iloc[idx]
        coords_file = self.db_dir / "coords_2d.npy"
        coords = np.load(coords_file) if coords_file.exists() and len(np.load(coords_file)) == len(self.df) else None
        pt_x = float(coords[idx][0]) if coords is not None else 0.0
        pt_y = float(coords[idx][1]) if coords is not None else 0.0
        
        return {
            "id": str(row["id"]),
            "title": str(row["title"]),
            "author": str(row["author"]),
            "pub_date": str(row["pub_date"]),
            "genres": str(row["genres"]),
            "summary": str(row["summary"]),
            "x": round(pt_x, 2),
            "y": round(pt_y, 2)
        }

    def find_similar_by_book_id(self, book_id: str, top_k: int = 10, genre_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Finds most similar books to a specific book in the database."""
        if self.df is None or self.embeddings is None:
            raise ValueError("Vector store is empty.")
            
        matches = self.df.index[self.df["id"] == book_id].tolist()
        if not matches:
            # Try by title exact match
            matches = self.df.index[self.df["title"].str.lower() == book_id.lower()].tolist()
            
        if not matches:
            raise ValueError(f"Book '{book_id}' not found in database.")
            
        book_idx = matches[0]
        book_vector = self.embeddings[book_idx]
        
        # Search for top_k + 1 to account for the book itself
        results = self.search_by_vector(book_vector, top_k=top_k + 1, genre_filter=genre_filter)
        
        # Filter out the source book itself
        filtered_results = [r for r in results if r["id"] != self.df.iloc[book_idx]["id"]][:top_k]
        return filtered_results
