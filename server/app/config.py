from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv
from pydantic import BaseModel

SERVER_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SERVER_DIR.parent
load_dotenv(SERVER_DIR / ".env")


def _path(name: str, default: str) -> Path:
    value = Path(os.getenv(name, default))
    return value.resolve() if value.is_absolute() else (SERVER_DIR / value).resolve()


class Settings(BaseModel):
    project_root: Path = PROJECT_ROOT
    data_root: Path = _path("DATA_ROOT", "../data")
    products_path: Path = _path("PRODUCTS_PATH", "../data/processed/products.json")
    rag_docs_path: Path = _path("RAG_DOCS_PATH", "../data/processed/rag_documents.json")
    chroma_dir: Path = _path("CHROMA_DIR", "../data/vectorstore/chroma")
    raw_dataset_dir: Path = _path("DATA_ROOT", "../data") / "raw/ecommerce_agent_dataset"
    doubao_api_key: str = os.getenv("DOUBAO_API_KEY", "")
    doubao_base_url: str = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3/")
    doubao_model: str = os.getenv("DOUBAO_MODEL", "")
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))


@lru_cache
def get_settings() -> Settings:
    return Settings()

