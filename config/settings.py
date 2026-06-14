import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LANCEDB_PATH = str(BASE_DIR / "knowledge_base" / "lancedb_data")
SOURCES_DIR = str(BASE_DIR / "knowledge_base" / "sources")
REFERENCE_IMAGES_DIR = str(BASE_DIR / "knowledge_base" / "sources" / "reference_images")

CLIP_MODEL_NAME = "ViT-B-32"
CLIP_PRETRAINED = "laion2b_s34b_b79k"
EMBEDDING_DIM = 512

DEFAULT_LLM_MODEL = "openai/gpt-4o-mini"
AVAILABLE_MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "anthropic/claude-sonnet-4-20250514",
    "google/gemini-2.0-flash-001",
]

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

TEXT_CHUNK_SIZE = 500
TEXT_CHUNK_OVERLAP = 50
TEXT_TOP_K = 10
IMAGE_TOP_K = 5

MAX_IMAGE_SIZE = 1024

# Qdrant Cloud (persistent shared history). When QDRANT_URL is set, the history
# store uses Qdrant; otherwise it falls back to a local on-disk LanceDB store.
QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_HISTORY_COLLECTION = os.getenv("QDRANT_HISTORY_COLLECTION", "design_history")
