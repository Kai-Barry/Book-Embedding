# Multi-stage lightweight CPU & GPU compatible Dockerfile for Book-Embedding Engine
FROM python:3.11-slim

# System setup & Intel OpenMP / BLAS acceleration libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies (CPU-optimized PyTorch with AVX2/VNNI support)
COPY requirements.txt .
# Filter out CUDA wheel index for compact CPU NAS footprint, install torch + sentence-transformers
RUN grep -v "\-\-extra-index-url" requirements.txt > reqs_cpu.txt && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r reqs_cpu.txt

# Copy source code and web assets
COPY src/ /app/src/
COPY web/ /app/web/
COPY scripts/ /app/scripts/

# Default Environment Variables (Customizable via Unraid WebUI or Docker -e)
ENV PORT=8000 \
    HOST=0.0.0.0 \
    DEVICE=cpu \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=4 \
    MKL_NUM_THREADS=4

# Expose default port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:${PORT}/api/status || exit 1

# Start FastAPI server dynamically binding to $PORT and $HOST
CMD python -m uvicorn src.api:app --host ${HOST} --port ${PORT}
