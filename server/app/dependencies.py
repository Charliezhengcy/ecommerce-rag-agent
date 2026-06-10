from functools import lru_cache

from app.agent.agent_service import AgentService
from app.agent.compare_service import CompareService
from app.config import get_settings
from app.llm.doubao_client import DoubaoClient
from app.llm.fallback_client import FallbackClient
from app.rag.query_parser import QueryParser
from app.rag.retriever import Retriever
from app.services.product_service import ProductService
from app.services.session_service import SessionService


@lru_cache
def get_product_service():
    return ProductService(get_settings().products_path)


@lru_cache
def get_session_service():
    return SessionService()


@lru_cache
def get_agent_service():
    settings = get_settings()
    products = get_product_service()
    sessions = get_session_service()
    doubao = DoubaoClient(settings.doubao_api_key, settings.doubao_base_url, settings.doubao_model)
    fallback = FallbackClient()
    compare = CompareService(products, doubao, fallback)
    return AgentService(products, sessions, Retriever(products.products, settings.chroma_dir),
                        QueryParser(products.products), doubao, fallback, compare)

