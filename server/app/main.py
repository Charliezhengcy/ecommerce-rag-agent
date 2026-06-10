from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import chat, health, products
from app.config import get_settings
from app.dependencies import get_agent_service, get_product_service, get_session_service

settings = get_settings()
app = FastAPI(title="Ecommerce RAG Agent", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(products.router)
app.include_router(chat.router)
if settings.raw_dataset_dir.exists():
    app.mount("/static/dataset", StaticFiles(directory=settings.raw_dataset_dir), name="dataset")


@app.on_event("startup")
def initialize_services():
    get_product_service()
    get_session_service()
    get_agent_service()

