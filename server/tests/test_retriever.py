from app.config import get_settings
from app.rag.query_parser import QueryParser
from app.rag.retriever import Retriever
from app.utils.json_utils import read_json


def test_retriever_demo_queries():
    settings = get_settings()
    products = read_json(settings.products_path)
    parser = QueryParser(products)
    retriever = Retriever(products, settings.chroma_dir)
    for query in ["油皮护肤品", "蓝牙耳机 续航", "轻量跑步鞋", "防晒 不含酒精", "低糖零食"]:
        result = retriever.search(query, parser.parse(query))
        assert result
        assert all(item["product_id"] in {p["product_id"] for p in products} for item in result)

