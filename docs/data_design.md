# 数据设计

`inspect_dataset.py` 只读取路径含 `data` 的 JSON，并忽略 `__MACOSX`、`.DS_Store`、`._*`。`prepare_data.py` 生成标准商品、单商品 RAG 文档和图片映射。

`min_sku_price`/`max_sku_price` 来自 SKU；摘要仅截取真实评论；标签由固定关键词抽取；`search_text` 汇总商品、FAQ、评论和 SKU。

