# 📖 Book-Embedding AI Engine (RTX 4080 CUDA & Gemini)

A high-performance Machine Learning semantic search and recommendation engine for books. It indexes book plot synopses and metadata, transforms them into dense vectors using GPU-accelerated embeddings or Google Gemini, and computes real-time nearest-neighbor cosine similarities.

---

## ⚡ Features
- **GPU Accelerated Vectorization**: Leverages NVIDIA GeForce RTX 4080 (16GB VRAM) with PyTorch CUDA to batch-embed thousands of books.
- **Top Embedding Models**:
  - **Local Model**: `BAAI/bge-large-en-v1.5` (1024-dimensional dense vectors, top-ranked on MTEB)
  - **Cloud Model**: Google Gemini `text-embedding-004` (768-dimensional dense vectors)
- **Rich Dataset**: Ingests CMU Book Summaries (~16,500 richly annotated book plots, authors, genres, dates) and supports custom Goodreads CSV imports.
- **Semantic Search**: Natural language query search (e.g. *"cyberpunk detective solving murders in futuristic neo-tokyo"*).
- **Book-to-Book Similarity**: Mathematical cosine distance ranking across the entire book catalog.
- **Modern Glassmorphic Web App**: Interactive dashboard with real-time latency stats and genre filtering.

---

## 🚀 Quickstart

### 1. Ingest Data & Generate Embeddings on GPU
Run the batch ingestion script on your RTX 4080:
```bash
# Ingest CMU Book Summaries with BGE-Large (1024-dim) on GPU
python -m scripts.ingest --batch-size 64
```
*Optional: Ingest a sample first for quick testing:*
```bash
python -m scripts.ingest --sample 1000
```
*Optional: Use Google Gemini embeddings instead:*
```bash
python -m scripts.ingest --provider gemini
```

### 2. Launch the Web App & API Server
```bash
python -m uvicorn src.api:app --reload --port 8000
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:8000`**

---

## 📁 Project Architecture
```
Book-Embedding/
├── data/
│   ├── raw/                 # Downloaded dataset cache
│   └── vector_db/           # Persisted vector database & parquet metadata
├── src/
│   ├── config.py            # Device (CUDA) & model settings
│   ├── data_loader.py       # CMU & Goodreads dataset parser
│   ├── embedder.py          # RTX 4080 CUDA embedder & Gemini API client
│   ├── vector_store.py      # High-performance cosine similarity engine
│   ├── recommender.py       # Recommender logic and catalog search
│   └── api.py               # FastAPI web endpoints
├── web/
│   ├── index.html           # Modern glassmorphism UI
│   ├── styles.css           # Dark-mode styling and animations
│   └── app.js               # Search controller and autocomplete
├── scripts/
│   └── ingest.py            # Batch vector ingestion CLI
├── requirements.txt         # Dependencies
└── README.md
```
