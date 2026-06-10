from app.rag.prompt_builder import PromptBuilder


class CompareService:
    def __init__(self, product_service, doubao, fallback):
        self.products = product_service
        self.doubao = doubao
        self.fallback = fallback
        self.prompts = PromptBuilder()

    async def answer(self, query: str, product_ids: list[str]) -> tuple[str, list[dict]]:
        products = [self.products.by_id[item] for item in product_ids[:2] if item in self.products.by_id]
        if len(products) < 2:
            return self.fallback.comparison(products, query), products
        if self.doubao.configured:
            try:
                return await self.doubao.complete(self.prompts.comparison(query, products)), products
            except Exception:
                pass
        return self.fallback.comparison(products, query), products

