
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Persistent ChromaDB storage location
BACKEND_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BACKEND_DIR / "chroma_data"

client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

# Collection containing all course materials
collection = client.get_or_create_collection(
    name="quizora_materials",
    metadata={"hnsw:space": "cosine"}
)

# Embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
