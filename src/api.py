import time
import torch
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
from src.config import WEB_DIR, DEFAULT_LOCAL_MODEL
from src.vector_store import BookVectorStore
from src.embedder import get_embedder
from src.recommender import BookRecommender

app = FastAPI(title="Book Semantic Embedding & Recommender Engine", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
vector_store = BookVectorStore()
embedder = None
recommender = None

@app.on_event("startup")
async def startup_event():
    global embedder, recommender
    print("[API] Initializing Recommender Backend...")
    try:
        embedder = get_embedder(provider="local")
        recommender = BookRecommender(vector_store, embedder)
        print("[API] Successfully initialized Recommender.")
    except Exception as e:
        print(f"[API Warning] Embedder could not be loaded at startup: {e}")
        recommender = BookRecommender(vector_store, None)

# Serve Web UI Static Files
app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

@app.get("/")
async def get_index():
    return FileResponse(WEB_DIR / "index.html")

@app.get("/api/status")
async def get_status():
    gpu_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if gpu_available else "CPU"
    vram_total = f"{torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f} GB" if gpu_available else "N/A"
    
    indexed_count = len(vector_store.df) if vector_store.df is not None else 0
    dim = vector_store.config.get("dimension", 0) if vector_store.config else 0
    model = vector_store.config.get("model_name", DEFAULT_LOCAL_MODEL)
    
    return {
        "status": "ready" if indexed_count > 0 else "needs_ingestion",
        "gpu": {
            "available": gpu_available,
            "name": gpu_name,
            "vram": vram_total
        },
        "index": {
            "books_count": indexed_count,
            "vector_dimension": dim,
            "model_name": model
        }
    }

@app.get("/api/genres")
async def get_genres():
    if not recommender:
        return []
    return recommender.get_all_genres()

@app.get("/api/catalog")
async def search_catalog(q: str = Query(..., min_length=1), limit: int = 15):
    if not recommender:
        raise HTTPException(status_code=503, detail="Service not ready")
    return recommender.search_catalog_titles(q, limit=limit)

class SearchQuery(BaseModel):
    query: str
    top_k: int = 12
    genre_filter: Optional[str] = None

@app.post("/api/semantic-search")
async def semantic_search(payload: SearchQuery):
    if not recommender or not recommender.embedder:
        raise HTTPException(status_code=503, detail="Vector index or embedder is not ready. Ingest dataset first.")
    
    t0 = time.perf_counter()
    results = recommender.search_books_by_text(
        query=payload.query,
        top_k=payload.top_k,
        genre_filter=payload.genre_filter
    )
    duration_ms = (time.perf_counter() - t0) * 1000.0
    
    return {
        "query": payload.query,
        "genre_filter": payload.genre_filter,
        "count": len(results),
        "latency_ms": round(duration_ms, 2),
        "results": results
    }

@app.get("/api/visualize")
async def get_visualization_data(max_points: int = 1500):
    if not vector_store or vector_store.df is None:
        raise HTTPException(status_code=503, detail="Vector index is empty.")
    points = vector_store.get_visualization_data(max_points=max_points)
    return {"points": points, "total": len(points)}

class AddBookRequest(BaseModel):
    title: str
    author: Optional[str] = "Unknown"
    genres: Optional[str] = "General"
    summary: str
    pub_date: Optional[str] = "Unknown"

@app.get("/api/book/{book_id}")
async def get_single_book_details(book_id: str):
    if not recommender:
        raise HTTPException(status_code=503, detail="Service not ready")
    details = recommender.get_book_details(book_id)
    if not details:
        raise HTTPException(status_code=404, detail="Book not found")
    return details

@app.post("/api/add-book")
async def add_book_dynamically(payload: AddBookRequest):
    if not recommender or not recommender.embedder:
        raise HTTPException(status_code=503, detail="Recommender service not ready.")
    
    embed_text = f"Title: {payload.title}\nAuthor: {payload.author}\nGenres: {payload.genres}\nDescription: {payload.summary}"
    vector = recommender.embedder.embed_texts([embed_text])[0]
    
    book_data = {
        "id": f"dyn_{payload.title.lower().replace(' ', '_')}",
        "title": payload.title,
        "author": payload.author,
        "genres": payload.genres,
        "genre_list": [g.strip() for g in payload.genres.split(",")],
        "summary": payload.summary,
        "pub_date": payload.pub_date,
        "embedding_text": embed_text
    }
    vector_store.add_book_vector(book_data, vector)
    return {"status": "success", "message": f"Added '{payload.title}' to vector database."}

@app.get("/api/similar/{book_id}")
async def get_similar_books(
    book_id: str, 
    top_k: int = 12, 
    genre: Optional[str] = None,
    weight_plot: float = 1.0,
    weight_tone: float = 1.0,
    weight_style: float = 1.0,
    weight_pacing: float = 1.0,
    weight_motifs: float = 1.0,
    weight_community: float = 1.0,
    boost_keywords: Optional[str] = None,
    exclude_keywords: Optional[str] = None,
    keywords: Optional[str] = None
):
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender service not ready")
    
    t0 = time.perf_counter()
    boost_list = [k.strip() for k in boost_keywords.split(",") if k.strip()] if boost_keywords else None
    if boost_list is None and keywords:
        boost_list = [k.strip() for k in keywords.split(",") if k.strip()]
    exclude_list = [k.strip() for k in exclude_keywords.split(",") if k.strip()] if exclude_keywords else None
    
    try:
        rec_data = recommender.recommend_similar_to_book(
            book_id_or_title=book_id,
            top_k=top_k,
            genre_filter=genre,
            weight_plot=weight_plot,
            weight_tone=weight_tone,
            weight_style=weight_style,
            weight_pacing=weight_pacing,
            weight_motifs=weight_motifs,
            weight_community=weight_community,
            boost_keywords=boost_list,
            exclude_keywords=exclude_list
        )
    except ValueError:
        # Check if we can dynamically fetch and embed it
        from src.data_loader import BookDataLoader
        online_book = BookDataLoader.fetch_online_book(book_id)
        if online_book and recommender.embedder:
            vec = recommender.embedder.embed_texts([online_book["embedding_text"]])[0]
            vector_store.add_book_vector(online_book, vec)
            rec_data = recommender.recommend_similar_to_book(
                online_book["id"], 
                top_k=top_k, 
                genre_filter=genre,
                weight_plot=weight_plot,
                weight_tone=weight_tone,
                weight_style=weight_style,
                weight_pacing=weight_pacing,
                weight_motifs=weight_motifs,
                weight_community=weight_community,
                boost_keywords=boost_list,
                exclude_keywords=exclude_list
            )
        else:
            raise HTTPException(status_code=404, detail=f"Book '{book_id}' not found.")
        
    duration_ms = (time.perf_counter() - t0) * 1000.0
    results = rec_data.get("results", [])
    target_book = rec_data.get("target_book", None)
    subclustered_motifs = rec_data.get("subclustered_motifs", {})
    concept_keywords = rec_data.get("concept_keywords", [])
    
    return {
        "book_id": book_id,
        "target_book": target_book,
        "subclustered_motifs": subclustered_motifs,
        "concept_keywords": concept_keywords,
        "count": len(results),
        "latency_ms": round(duration_ms, 2),
        "results": results
    }

@app.post("/api/bolster/{book_id}")
async def bolster_single_book(book_id: str):
    """Fetches real-time authoritative metadata, ratings, and blurbs from OpenLibrary / Google Books."""
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender service not ready")
    
    if recommender.store.df is not None:
        match = recommender.store.df[
            (recommender.store.df["id"] == book_id) | 
            (recommender.store.df["title"].str.lower() == book_id.lower())
        ]
        if not match.empty:
            raw_dict = match.iloc[0].to_dict()
            recommender.enricher.bolster_book(raw_dict, fetch_online=True)

    details = recommender.get_book_details(book_id)
    if not details:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "success", "book": details}
