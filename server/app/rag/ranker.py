class Ranker:
    def rank(self, products: list[dict], query: str, include_terms: list[str], vector_ids: list[str] | None = None) -> list[dict]:
        vector_ids = vector_ids or []
        vector_score = {product_id: len(vector_ids) - index for index, product_id in enumerate(vector_ids)}

        def score(item):
            text = item["search_text"].lower()
            soft = sum(5 for term in include_terms if term.lower() in text)
            query_hits = sum(1 for token in query.lower().replace("的", " ").split() if token and token in text)
            return soft + query_hits + vector_score.get(item["product_id"], 0)

        return sorted(products, key=score, reverse=True)

