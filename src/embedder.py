import os
import torch
import numpy as np
from typing import List, Union, Optional
from abc import ABC, abstractmethod
from src.config import DEFAULT_LOCAL_MODEL, GEMINI_API_KEY, GEMINI_MODEL, DEVICE, BATCH_SIZE

class BaseEmbedder(ABC):
    """Abstract base class for book embedding models."""
    
    @abstractmethod
    def embed_texts(self, texts: List[str], batch_size: int = BATCH_SIZE) -> np.ndarray:
        """Generates embedding vectors for a list of text strings."""
        pass
        
    @abstractmethod
    def embed_query(self, query: str) -> np.ndarray:
        """Generates embedding vector for a single query."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Returns the dimensionality of the embeddings."""
        pass


class LocalGPUEmbedder(BaseEmbedder):
    """
    High-performance GPU & CPU-accelerated embedder using Sentence-Transformers & PyTorch.
    Default model: BAAI/bge-large-en-v1.5 (1024-dim, state-of-the-art)
    """
    def __init__(self, model_name: str = DEFAULT_LOCAL_MODEL, device: Optional[str] = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._query_cache = {}
        
        # Optimize CPU multi-threading if running on NAS / CPU without GPU
        if self.device == "cpu":
            num_cores = os.cpu_count() or 4
            # Use optimal physical core threads for Intel 12th Gen P-cores
            opt_threads = min(8, max(2, num_cores // 2))
            torch.set_num_threads(opt_threads)
            print(f"[Embedder] Initializing Local CPU Embedder: {model_name} with {opt_threads} PyTorch CPU threads (AVX2/VNNI enabled)")
        else:
            print(f"[Embedder] Initializing Local GPU Embedder: {model_name} on device: {self.device}")
            if torch.cuda.is_available():
                print(f"[Embedder] Utilizing GPU: {torch.cuda.get_device_name(0)} (VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f} GB)")

        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name, device=self.device)
        self._dim = self.model.get_sentence_embedding_dimension()

    @property
    def dimension(self) -> int:
        return self._dim

    def embed_texts(self, texts: List[str], batch_size: int = BATCH_SIZE) -> np.ndarray:
        """Generates normalized embeddings in batches."""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=len(texts) > 10,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """Encodes query for retrieval with in-memory caching for repeat concept keywords."""
        if query in self._query_cache:
            return self._query_cache[query]

        # For BGE models, retrieval queries can benefit from instruction prefix if required
        if "bge" in self.model_name.lower():
            query_text = f"Represent this sentence for searching relevant passages: {query}"
        else:
            query_text = query
            
        emb = self.model.encode(
            [query_text],
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        vec = emb[0]
        # Keep cache compact (up to 500 queries)
        if len(self._query_cache) < 500:
            self._query_cache[query] = vec
        return vec


class GeminiEmbedder(BaseEmbedder):
    """
    Google Gemini Cloud Embedder using text-embedding-004.
    """
    def __init__(self, api_key: Optional[str] = None, model_name: str = GEMINI_MODEL):
        self.api_key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please provide a valid Gemini API key or use LocalGPUEmbedder.")
        
        self.model_name = model_name
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self._genai = genai
        self._dim = 768  # text-embedding-004 standard dimension
        print(f"[Embedder] Initialized Gemini Cloud Embedder ({model_name})")

    @property
    def dimension(self) -> int:
        return self._dim

    def embed_texts(self, texts: List[str], batch_size: int = 50) -> np.ndarray:
        all_embeddings = []
        # Batch requests
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            result = self._genai.embed_content(
                model=f"models/{self.model_name}",
                content=batch,
                task_type="retrieval_document"
            )
            all_embeddings.extend(result["embedding"])
        
        arr = np.array(all_embeddings, dtype=np.float32)
        # Normalize
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        return arr / np.maximum(norms, 1e-12)

    def embed_query(self, query: str) -> np.ndarray:
        result = self._genai.embed_content(
            model=f"models/{self.model_name}",
            content=query,
            task_type="retrieval_query"
        )
        vec = np.array(result["embedding"], dtype=np.float32)
        return vec / max(np.linalg.norm(vec), 1e-12)


def get_embedder(provider: str = "local", model_name: Optional[str] = None) -> BaseEmbedder:
    """Factory function to instantiate the requested embedder."""
    if provider.lower() == "gemini":
        return GeminiEmbedder(model_name=model_name or GEMINI_MODEL)
    return LocalGPUEmbedder(model_name=model_name or DEFAULT_LOCAL_MODEL)
