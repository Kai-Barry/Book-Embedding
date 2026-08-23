import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
WEB_DIR = BASE_DIR / "web"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# Embedding Configuration
# Top-tier high quality model: BAAI/bge-large-en-v1.5 (1024 dims), fallback: all-MiniLM-L6-v2 (384 dims)
DEFAULT_LOCAL_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "text-embedding-004"

# Device Configuration: CUDA for RTX 4080 if available, otherwise CPU
DEVICE = os.getenv("DEVICE", "cuda")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "64"))

# API Server Configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
