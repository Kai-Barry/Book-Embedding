# 🌌 LIBRARIS — The Narrative Observatory

> **High-Dimensional Semantic Vector Search & Multi-Vector Literary Discovery Engine**  
> Powered by PyTorch CUDA (RTX 4080 / CPU), BAAI `bge-large-en-v1.5`, UMAP Spatial Projections, and Item2Vec Collaborative Filtering.

---

## ⚡ Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Vector Embeddings** | `BAAI/bge-large-en-v1.5` / Google Gemini | 1024-dim dense semantic vector embeddings |
| **Compute & Acceleration** | PyTorch CUDA (RTX 4080 16GB) | Sub-millisecond tensor cosine similarity batching |
| **Dimensionality Reduction**| UMAP (Uniform Manifold Approximation) | 2D geometric projection of 25,000+ book space |
| **Collaborative Filtering** | Item2Vec (Word2Vec Skip-Gram on Co-Reads)| Reader co-taste and readership cluster affinity |
| **Backend API** | FastAPI + Uvicorn (Asynchronous) | High-concurrency REST endpoints with caching |
| **Data & Storage** | PyArrow / Parquet + NumPy Memmap | Memory-mapped dense vector matrices & catalog |
| **Data Enrichment** | OpenLibrary API & Google Books API | Live web metadata, synopsis & rating bolstering |
| **Frontend UI** | HTML5, Vanilla CSS3, JavaScript (ES6+) | Obsidian & Amber editorial UI, Lucide Icons |
| **Containerization** | Docker & Docker Compose | Containerized deployment on Linux, Windows & Unraid |

---

## 🚀 Key Features

1. **Multi-Dimensional Vector Tuning (Stage 02)**:
   - Dynamic weight calibration across 5 narrative dimensions: **Plot Premise**, **Atmospheric Tone**, **Style & POV**, **Pacing Velocity**, and **Audience Co-Taste**.
   - 1-Click Calibration Presets (*Balanced*, *Narrative Depth*, *Audience Cluster*, *Prose Twin*, *Atmospheric Aura*).
   - Thematic motif boosting (`+1.0x`, `+1.6x`, `+2.2x`) and exclusion (`-1.5x`).
2. **Interactive 2D Semantic Constellation (Stage 03)**:
   - GPU-projected 2D coordinate space for 25,101 books.
   - Spatial Hash Grid (`O(1)` hover detection at 60 FPS).
   - Touch gesture engine with 1-finger panning, 2-finger pinch-to-zoom (0.2x–50x), and stationary star tap detection.
3. **Vector Decomposition & Explainability**:
   - 4-bar breakdown meters revealing exact sub-vector match percentages.
   - Narrative DNA tags (POV, Pacing Meter, Writing Craft, Tone Aura).
4. **Live Web Bolstering**:
   - 1-click real-time data enrichment fetching plot summaries and community metrics from OpenLibrary & Google Books.

---

## 🛠️ Quickstart

### 1. Installation
```bash
git clone https://github.com/Kai-Barry/Book-Embedding.git
cd Book-Embedding
pip install -r requirements.txt
```

### 2. Ingest Data & Generate Embeddings (GPU / CPU)
```bash
# Ingest catalog with BGE-Large (1024-dim) on CUDA GPU
python -m scripts.ingest --batch-size 64
```

### 3. Launch Web Observatory & API
```bash
python -m uvicorn src.api:app --reload --port 8000
```
Open **`http://127.0.0.1:8000`** in your browser.

---

## 🐳 Docker Deployment

```bash
docker-compose up -d --build
```

---

## 📡 API Endpoints

- `GET /api/status` — GPU hardware telemetry and indexed corpus status.
- `GET /api/catalog?q={query}` — Typo-tolerant autocomplete across 25,101 books.
- `GET /api/book/{id}` — Full metadata, style profile, and thematic subclusters.
- `GET /api/similar/{id}` — Multi-weighted cosine vector similarity search.
- `POST /api/bolster/{id}` — Live web data enrichment via OpenLibrary/Google Books.
## 🧪 Automated Testing

Execute the comprehensive test suite across vector math, collaborative filtering, style extraction, profile recommendations, and API endpoints:

```bash
python -m unittest discover -s tests -v
```

---

## 📜 Architecture & Design
For details on vector decomposition mathematics, Item2Vec co-occurrence modeling, and spatial indexing, see [ARCHITECTURE.md](ARCHITECTURE.md).

