from copy import deepcopy
from threading import Lock


EMPTY = {
    "history": [], "current_intent": None, "current_category": None, "current_sub_category": None,
    "constraints": {"price_min": None, "price_max": None, "include_terms": [], "exclude_terms": []},
    "last_recommended_product_ids": [],
}


class SessionService:
    def __init__(self):
        self.sessions: dict[str, dict] = {}
        self.lock = Lock()

    def get(self, session_id: str) -> dict:
        with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = dict(deepcopy(EMPTY), session_id=session_id)
            return self.sessions[session_id]

    def merge(self, session_id: str, parsed) -> dict:
        state = self.get(session_id)
        old_category = state["current_category"]
        if parsed.category and old_category and parsed.category != old_category:
            state["constraints"] = deepcopy(EMPTY["constraints"])
            state["current_sub_category"] = None
        if parsed.category:
            state["current_category"] = parsed.category
        if parsed.sub_category:
            state["current_sub_category"] = parsed.sub_category
        state["current_intent"] = parsed.intent
        for key in ("price_min", "price_max"):
            value = getattr(parsed, key)
            if value is not None:
                state["constraints"][key] = value
        for key in ("include_terms", "exclude_terms"):
            state["constraints"][key] = list(dict.fromkeys(state["constraints"][key] + getattr(parsed, key)))
        return state

    def add_turn(self, session_id: str, user: str, assistant: str, product_ids: list[str]):
        state = self.get(session_id)
        state["history"].extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])
        state["history"] = state["history"][-12:]
        if product_ids:
            state["last_recommended_product_ids"] = product_ids

