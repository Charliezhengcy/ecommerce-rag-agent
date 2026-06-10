from typing import Any
from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    model_config = ConfigDict(extra="allow")
    product_id: str
    title: str
    brand: str
    category: str
    sub_category: str
    base_price: float
    min_sku_price: float
    max_sku_price: float
    image_url: str
    tags: list[str] = []
    skus: list[dict[str, Any]] = []

