from pathlib import Path
import sys

SERVER_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER_DIR))

from app.config import get_settings
from app.utils.json_utils import read_json, write_json
from app.utils.text_utils import compact, flatten_text

TAG_KEYWORDS = [
    "油皮", "干皮", "敏感肌", "混油皮", "保湿", "控油", "修护", "抗初老",
    "淡纹", "紧致", "美白", "提亮", "防晒", "不含酒精", "温和", "清爽",
    "蓝牙", "降噪", "续航", "快充", "轻量", "游戏", "办公", "高刷", "拍照",
    "音质", "便携", "跑步", "跑鞋", "缓震", "透气", "防滑", "运动", "通勤",
    "休闲", "保暖", "速干", "低糖", "无糖", "咖啡", "茶", "零食", "饱腹",
    "健康", "儿童", "早餐",
]


def raw_json_files(root: Path):
    return sorted(
        path for path in root.rglob("*.json")
        if "data" in path.parts and "__MACOSX" not in path.parts and not path.name.startswith("._")
    )


def review_summary(reviews: list[dict]) -> str:
    positive = [compact(item.get("content", "")) for item in reviews if item.get("rating", 0) >= 4][:2]
    negative = [compact(item.get("content", "")) for item in reviews if item.get("rating", 0) <= 2][:2]
    parts = []
    if positive:
        parts.append("好评反馈：" + "；".join(positive))
    if negative:
        parts.append("差评反馈：" + "；".join(negative))
    return "\n".join(parts)


def build_search_text(product: dict) -> str:
    sku_text = "；".join(
        f"{flatten_text(sku.get('properties', {}))} {sku.get('price', '')}元" for sku in product["skus"]
    )
    faq_text = "；".join(
        f"{faq.get('question', '')} {faq.get('answer', '')}" for faq in product["official_faq"]
    )
    review_text = "；".join(review.get("content", "") for review in product["user_reviews"])
    return "\n".join([
        f"商品名：{product['title']}", f"品牌：{product['brand']}",
        f"一级类目：{product['category']}", f"二级类目：{product['sub_category']}",
        f"基础价格：{product['base_price']}", f"价格范围：{product['min_sku_price']}-{product['max_sku_price']}",
        f"SKU：{sku_text}", f"商品描述：{product['marketing_description']}",
        f"官方问答：{faq_text}", f"用户评论：{review_text}",
        f"评论摘要：{product['review_summary']}", f"标签：{'、'.join(product['tags'])}",
    ])


def normalize(raw: dict) -> dict:
    knowledge = raw.get("rag_knowledge") or {}
    skus = raw.get("skus") or []
    prices = [float(sku["price"]) for sku in skus if sku.get("price") is not None]
    base_price = float(raw.get("base_price") or 0)
    source = flatten_text(raw)
    product = {
        "product_id": raw["product_id"], "title": raw.get("title", ""), "brand": raw.get("brand", ""),
        "category": raw.get("category", ""), "sub_category": raw.get("sub_category", ""),
        "base_price": base_price, "min_sku_price": min(prices) if prices else base_price,
        "max_sku_price": max(prices) if prices else base_price, "image_path": raw.get("image_path", ""),
        "image_url": "/static/dataset/" + raw.get("image_path", ""), "skus": skus,
        "marketing_description": knowledge.get("marketing_description", ""),
        "official_faq": knowledge.get("official_faq") or [], "user_reviews": knowledge.get("user_reviews") or [],
    }
    product["review_summary"] = review_summary(product["user_reviews"])
    product["tags"] = [tag for tag in TAG_KEYWORDS if tag in source]
    product["search_text"] = build_search_text(product)
    return product


def rag_document(product: dict) -> dict:
    limited = dict(product)
    limited["official_faq"] = product["official_faq"][:5]
    limited["user_reviews"] = product["user_reviews"][:5]
    content = f"商品ID：{product['product_id']}\n{build_search_text(limited)}"[:3000]
    metadata_keys = ["product_id", "title", "brand", "category", "sub_category", "base_price", "min_sku_price", "max_sku_price"]
    return {"doc_id": f"doc_{product['product_id']}", "product_id": product["product_id"], "content": content,
            "metadata": {key: product[key] for key in metadata_keys}}


def prepare() -> tuple[list[dict], list[dict]]:
    settings = get_settings()
    products = [normalize(read_json(path)) for path in raw_json_files(settings.raw_dataset_dir)]
    ids = [item["product_id"] for item in products]
    if len(ids) != len(set(ids)):
        raise ValueError("product_id must be unique")
    documents = [rag_document(product) for product in products]
    images = {p["product_id"]: {"image_path": p["image_path"], "image_url": p["image_url"]} for p in products}
    write_json(settings.products_path, products)
    write_json(settings.rag_docs_path, documents)
    write_json(settings.data_root / "processed/product_image_map.json", images)
    return products, documents

