import re
from typing import Iterable


def flatten_text(value) -> str:
    if isinstance(value, dict):
        return " ".join(flatten_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten_text(item) for item in value)
    return str(value or "")


def chunks(text: str, size: int = 12) -> Iterable[str]:
    for index in range(0, len(text), size):
        yield text[index:index + size]


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

