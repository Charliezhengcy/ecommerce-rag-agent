from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ParsedQuery(BaseModel):
    intent: str = "unknown"
    category: str | None = None
    sub_category: str | None = None
    price_min: float | None = None
    price_max: float | None = None
    include_terms: list[str] = []
    exclude_terms: list[str] = []
    raw_query: str = ""

