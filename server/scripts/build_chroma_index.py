from pathlib import Path
import sys

SERVER_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER_DIR))
from app.config import get_settings
from app.utils.json_utils import read_json
from app.utils.embedding_utils import hash_embedding

try:
    import chromadb
except ImportError as exc:
    raise SystemExit("Install server/requirements.txt before building the Chroma index.") from exc

settings = get_settings()
documents = read_json(settings.rag_docs_path)
client = chromadb.PersistentClient(path=str(settings.chroma_dir))
try:
    client.delete_collection("products")
except Exception:
    pass
mode = "hash"
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", local_files_only=True)
    embeddings = model.encode([item["content"] for item in documents], normalize_embeddings=True).tolist()
    mode = "sentence-transformers"
except Exception:
    embeddings = [hash_embedding(item["content"]) for item in documents]
collection = client.create_collection("products")
collection.add(
    ids=[item["doc_id"] for item in documents],
    documents=[item["content"] for item in documents],
    metadatas=[item["metadata"] for item in documents],
    embeddings=embeddings,
)
(settings.chroma_dir / "embedding_mode.txt").write_text(mode, encoding="utf-8")
print(f"Built Chroma index with {len(documents)} documents at {settings.chroma_dir} (embedding={mode})")
