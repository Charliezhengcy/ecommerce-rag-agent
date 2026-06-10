from app.config import get_settings
from app.utils.json_utils import read_json


def test_processed_data_is_complete():
    settings = get_settings()
    products = read_json(settings.products_path)
    docs = read_json(settings.rag_docs_path)
    assert len(products) == 100
    assert len({item["product_id"] for item in products}) == len(products)
    assert len(docs) == len(products)
    for item in products:
        assert all(item[key] for key in ["product_id", "title", "brand", "category", "sub_category", "search_text"])
        assert (settings.raw_dataset_dir / item["image_path"]).exists()

