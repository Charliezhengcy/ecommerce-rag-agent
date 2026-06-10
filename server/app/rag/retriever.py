from pathlib import Path

from app.rag.ranker import Ranker
from app.rag.structured_filter import StructuredFilter
from app.utils.embedding_utils import hash_embedding


class Retriever:
    def __init__(self, products: list[dict], chroma_dir: Path):
        self.products = products
        self.filter = StructuredFilter()
        self.ranker = Ranker()
        self.collection = None
        self.embedding_mode = "hash"
        try:
            import chromadb
            self.collection = chromadb.PersistentClient(path=str(chroma_dir)).get_collection("products")
            mode_path = chroma_dir / "embedding_mode.txt"
            self.embedding_mode = mode_path.read_text(encoding="utf-8").strip() if mode_path.exists() else "hash"
        except Exception:
            # Local fallback keeps the demo functional before the optional embedding model is downloaded.
            self.collection = None

    def vector_ids(self, query: str) -> list[str]:
        if not self.collection:
            return []
        try:
            if self.embedding_mode == "sentence-transformers":
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", local_files_only=True)
                embedding = model.encode([query], normalize_embeddings=True).tolist()
            else:
                embedding = [hash_embedding(query)]
            result = self.collection.query(query_embeddings=embedding, n_results=10)
            return [item.replace("doc_", "") for item in result["ids"][0]]
        except Exception:
            return []

    def search(self, query: str, parsed, limit: int = 5) -> list[dict]:
        candidates = self.filter.apply(self.products, parsed)
        if not candidates and parsed.sub_category:
            candidates = self.filter.apply(self.products, parsed, relax_sub_category=True)
        return self.ranker.rank(candidates, query, parsed.include_terms, self.vector_ids(query))[:limit]
