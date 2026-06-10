from app.config import get_settings
from app.rag.structured_filter import StructuredFilter
from app.schemas.chat import ParsedQuery
from app.utils.json_utils import read_json

PRODUCTS = read_json(get_settings().products_path)


def test_hard_filters_and_soft_preferences():
    service = StructuredFilter()
    cheap = service.apply(PRODUCTS, ParsedQuery(price_max=200))
    assert cheap and all(item["min_sku_price"] <= 200 for item in cheap)
    alcohol_free = service.apply(PRODUCTS, ParsedQuery(exclude_terms=["酒精"]))
    assert all("酒精" not in item["search_text"] for item in alcohol_free)
    beauty = service.apply(PRODUCTS, ParsedQuery(category="美妆护肤"))
    assert beauty and all(item["category"] == "美妆护肤" for item in beauty)
    assert service.apply(PRODUCTS, ParsedQuery(include_terms=["不存在的偏好"])) == PRODUCTS

