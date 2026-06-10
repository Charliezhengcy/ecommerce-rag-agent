class StructuredFilter:
    """Enforces facts the LLM is never allowed to relax: price and exclusions."""

    def apply(self, products: list[dict], parsed, relax_sub_category: bool = False) -> list[dict]:
        result = products
        if parsed.category:
            result = [item for item in result if item["category"] == parsed.category]
        if parsed.sub_category and not relax_sub_category:
            result = [item for item in result if item["sub_category"] == parsed.sub_category]
        if parsed.price_min is not None:
            result = [item for item in result if item["max_sku_price"] >= parsed.price_min]
        if parsed.price_max is not None:
            result = [item for item in result if item["min_sku_price"] <= parsed.price_max]
        for term in parsed.exclude_terms:
            normalized = term.replace("日系品牌", "日系")
            result = [item for item in result if normalized.lower() not in
                      f"{item['title']} {item['brand']} {item['search_text']}".lower()]
        return result

