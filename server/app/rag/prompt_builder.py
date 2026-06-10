class PromptBuilder:
    SYSTEM = """你是电商智能导购。只能基于候选商品回答。
禁止编造商品、价格、优惠券、库存、促销、功能、成分、材质或效果。
价格、标题、品牌以候选商品为准；回复简洁，说明匹配点和可能不适合之处。"""

    def product_context(self, product: dict, index: int) -> str:
        faq = "；".join(f"{x.get('question','')} {x.get('answer','')}" for x in product.get("official_faq", [])[:2])
        return f"""候选商品 {index}：
product_id: {product['product_id']}
商品名：{product['title']}
品牌：{product['brand']}
一级类目：{product['category']}
二级类目：{product['sub_category']}
展示价格：{product['min_sku_price']} 元起
价格范围：{product['min_sku_price']}-{product['max_sku_price']} 元
商品描述：{product['marketing_description'][:500]}
FAQ摘要：{faq[:400]}
评论摘要：{product['review_summary'][:400]}
标签：{'、'.join(product['tags'])}"""

    def recommendation(self, query: str, products: list[dict]) -> list[dict]:
        context = "\n\n".join(self.product_context(item, index + 1) for index, item in enumerate(products))
        return [{"role": "system", "content": self.SYSTEM},
                {"role": "user", "content": f"用户需求：{query}\n\n{context}\n请推荐最多三款并解释。"}]

    def comparison(self, query: str, products: list[dict]) -> list[dict]:
        context = "\n\n".join(self.product_context(item, index + 1) for index, item in enumerate(products))
        return [{"role": "system", "content": self.SYSTEM},
                {"role": "user", "content": f"{query}\n{context}\n从价格、品牌、卖点、场景、评价、不适合人群和最终建议对比，不用表格。"}]
