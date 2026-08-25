# 🏛️ LIBRARIS — Architectural Overview

This document provides a concise technical breakdown of the system architecture, mathematical vector formulation, collaborative filtering model, and spatial rendering engine.

---

## 🏗️ High-Level System Architecture

```
[ User Browser / Mobile Device ]
       │  (Vanilla JS, Touch Gestures, Spatial 2D Canvas)
       ▼
[ FastAPI Async Server (uvicorn :8000) ]
  ├── GET  /api/catalog ──► In-Memory Trie & Fuzzy Matcher
  ├── GET  /api/similar ──► Recommender Multi-Vector Scorer
  │                           ├── PyTorch CUDA Cosine Similarity (BGE-Large 1024-d)
  │                           ├── Motif Sub-Cluster Keyword Adjuster
  │                           └── Item2Vec Collaborative Affinity Scorer
  ├── POST /api/bolster ──► Async Live Web Enricher (OpenLibrary / Google Books)
  └── GET  /api/galaxy  ──► 2D UMAP Spatial Coordinates Cache
```

---

## 🧮 1. Multi-Vector Scoring Formulation

When a search is requested for anchor book $A$ against candidate corpus $C$, the composite similarity score $S_{\text{composite}}(A, C)$ is computed as a weighted combination of dense and discrete sub-dimensions:

$$S_{\text{composite}}(A, C) = \frac{\sum_{k} w_k \cdot S_k(A, C)}{\sum_{k} w_k} + \sum_{m \in \text{Boosted}} \delta_m(C) - \sum_{e \in \text{Excluded}} \gamma_e(C)$$

Where:
- $S_{\text{plot}}$: Dense cosine similarity of plot synopses ($1024$-dim `bge-large-en-v1.5` embeddings).
- $S_{\text{tone}}$: Atmospheric & mood sentiment alignment.
- $S_{\text{style}}$: Stylistic DNA match (POV voice parity, prose density, lexical complexity).
- $S_{\text{pacing}}$: Story velocity matching (Slow-burn $\leftrightarrow$ fast-paced propulsive tension).
- $S_{\text{community}}$: Item2Vec collaborative co-reading affinity.
- $w_k \in [0.0, 2.2]$: User-calibrated priority multipliers from Stage 02.
- $\delta_m(C)$: Keyword / motif boost score if motif $m$ is present in candidate $C$.
- $\gamma_e(C)$: Exclusion penalty if excluded keyword $e$ occurs in candidate $C$.

---

## 👥 2. Item2Vec Collaborative Filtering

To capture reader behavioral affinity alongside plot semantics:
- Books are modeled as "tokens" inside reader "baskets" (Goodreads / community lists).
- An **Item2Vec** model is trained using Skip-Gram negative sampling on co-occurrence pairs.
- Yields a dense behavioral embedding space where books frequently enjoyed by the same readers cluster together even when plot keywords diverge.

---

## 🌌 3. 2D Spatial Constellation & Spatial Hashing

- **Dimensionality Reduction**: `UMAP` compresses 1024-dimensional semantic space into 2D $(x, y) \in [-100, 100]$.
- **Spatial Hash Grid ($O(1)$ Lookups)**:
  - Coordinate space is partitioned into uniform grid cells ($10\times 10$ units).
  - Hover and tap events map to cell keys `gridX_gridY` in $O(1)$ time, maintaining steady 60 FPS performance across 25,000+ points.
- **Mobile Touch Engine**:
  - 1-finger velocity drag & pan with boundary damping.
  - 2-finger dynamic pinch zoom calculating Euclidean distance $\Delta d = \sqrt{\Delta x^2 + \Delta y^2}$ ($0.2\times$ to $50.0\times$).
  - Stationary tap vs. drag threshold ($< 5\text{px}$ movement).

---

## 🌐 4. Live Data Bolster Pipeline

When anchor literature lacks synopsis depth or ratings:
1. `DataEnricher` sends parallel asynchronous HTTP queries to **OpenLibrary API** and **Google Books API**.
2. Synopses are merged, cleaned, and re-tokenized.
3. Stylistic metadata (POV, Pacing, Prose density) and community star ratings are extracted and cached in the vector index.

---

## 💻 5. Tech Stack Summary

- **Backend**: Python 3.10+, PyTorch (CUDA), FastAPI, Uvicorn, NumPy, Pandas, PyArrow/Parquet, UMAP-Learn, Transformers.
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design Tokens), ES6+ JavaScript, Lucide Vector Icons, HTML5 Canvas 2D.
- **Deployment**: Docker, Docker Compose, Unraid XML Template.

---

## 🧪 6. Testing & Quality Assurance Architecture

The codebase includes an automated modular test suite covering all critical layers:

| Test Module | Coverage Scope |
| :--- | :--- |
| `test_vector_store.py` | Index persistence, L2 normalization, and cosine nearest neighbor math. |
| `test_collaborative.py` | Item2Vec matrix shape, unit vectors, and global score blending. |
| `test_style_extractor.py` | POV heuristic classification, story velocity meters, and atmospheric mood extraction. |
| `test_data_enricher.py` | Book series regex parsing, popularity tier scoring, and in-memory bolstering. |
| `test_recommender.py` | Multi-vector weighting, motif boosting/exclusion, Rocchio profile centroids, and attribution. |
| `test_api.py` | FastAPI endpoint contracts (`/api/status`, `/api/catalog`, `/api/similar`, `/api/recommend/profile`). |

