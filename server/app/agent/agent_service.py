from app.rag.prompt_builder import PromptBuilder
from app.schemas.chat import ParsedQuery


class AgentService:
    def __init__(self, product_service, session_service, retriever, parser, doubao, fallback, compare):
        self.products, self.sessions, self.retriever = product_service, session_service, retriever
        self.parser, self.doubao, self.fallback, self.compare = parser, doubao, fallback, compare
        self.prompts = PromptBuilder()

    def contextual_query(self, parsed, state) -> ParsedQuery:
        # Refine turns inherit category and hard constraints, while a newly named category resets them in SessionService.
        constraints = state["constraints"]
        return ParsedQuery(
            **parsed.model_dump(exclude={"category", "sub_category", "price_min", "price_max", "include_terms", "exclude_terms"}),
            category=parsed.category or state["current_category"],
            sub_category=parsed.sub_category or state["current_sub_category"],
            price_min=parsed.price_min if parsed.price_min is not None else constraints["price_min"],
            price_max=parsed.price_max if parsed.price_max is not None else constraints["price_max"],
            include_terms=constraints["include_terms"], exclude_terms=constraints["exclude_terms"],
        )

    async def answer(self, session_id: str, query: str) -> tuple[str, list[dict]]:
        state = self.sessions.get(session_id)
        parsed = self.parser.parse(query, state)
        if parsed.intent == "compare":
            answer, products = await self.compare.answer(query, state["last_recommended_product_ids"])
            self.sessions.add_turn(session_id, query, answer, [])
            return answer, products

        state = self.sessions.merge(session_id, parsed)
        contextual = self.contextual_query(parsed, state)
        candidates = self.retriever.search(query, contextual)
        if not candidates:
            answer = self.fallback.recommendation([])
        elif self.doubao.configured:
            try:
                answer = await self.doubao.complete(self.prompts.recommendation(query, candidates))
            except Exception:
                answer = self.fallback.recommendation(candidates)
        else:
            answer = self.fallback.recommendation(candidates)
        ids = [item["product_id"] for item in candidates[:3]]
        self.sessions.add_turn(session_id, query, answer, ids)
        return answer, candidates[:3]

