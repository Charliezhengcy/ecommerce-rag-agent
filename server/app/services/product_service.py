from pathlib import Path

from app.utils.json_utils import read_json


class ProductService:
    def __init__(self, products_path: Path):
        self.products_path = products_path
        self.products = read_json(products_path) if products_path.exists() else []
        self.by_id = {item["product_id"]: item for item in self.products}

    def reload(self):
        self.__init__(self.products_path)

    @staticmethod
    def price_text(product: dict) -> str:
        low, high = product["min_sku_price"], product["max_sku_price"]
        return f"¥{low:g} 起" if low != high else f"¥{low:g}"

    def card(self, product: dict, reason: str = "该商品与当前需求匹配，可点击查看详情。") -> dict:
        return {
            "product_id": product["product_id"], "title": product["title"], "brand": product["brand"],
            "category": product["category"], "sub_category": product["sub_category"],
            "price": product["min_sku_price"], "price_text": self.price_text(product),
            "image_url": product["image_url"], "reason": reason, "tags": product.get("tags", []),
        }

    def list(self, category=None, sub_category=None, keyword=None, limit=20) -> list[dict]:
        result = self.products
        if category:
            result = [item for item in result if item["category"] == category]
        if sub_category:
            result = [item for item in result if item["sub_category"] == sub_category]
        if keyword:
            result = [item for item in result if keyword.lower() in item["search_text"].lower()]
        return [dict(item, price_text=self.price_text(item)) for item in result[:limit]]

    def get(self, product_id: str) -> dict | None:
        item = self.by_id.get(product_id)
        return dict(item, price_text=self.price_text(item)) if item else None

