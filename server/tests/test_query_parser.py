from app.rag.query_parser import QueryParser
from app.utils.json_utils import read_json
from app.config import get_settings


def parser():
    return QueryParser(read_json(get_settings().products_path))


def test_demo_queries():
    service = parser()
    assert service.parse("推荐一款适合油皮的护肤品").category == "美妆护肤"
    headphones = service.parse("200 元以下的蓝牙耳机有哪些？")
    assert headphones.price_max == 200 and headphones.category == "数码电子"
    session = {"current_category": "服饰运动"}
    assert service.parse("要轻一点的", session).intent == "refine"
    assert service.parse("预算 500 以内", session).price_max == 500
    excluded = service.parse("推荐防晒霜，但不要含酒精的，也不要日系品牌")
    assert "酒精" in excluded.exclude_terms and "日系品牌" in excluded.exclude_terms
    assert service.parse("对比刚才推荐的前两款，哪个更适合敏感肌？").intent == "compare"

