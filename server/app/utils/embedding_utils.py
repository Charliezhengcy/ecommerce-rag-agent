import hashlib
import math


def hash_embedding(text: str, dimensions: int = 384) -> list[float]:
    """Deterministic offline embedding used only when the preferred local MiniLM model is unavailable."""
    vector = [0.0] * dimensions
    normalized = "".join(text.lower().split())
    for index in range(max(1, len(normalized) - 1)):
        token = normalized[index:index + 2] or normalized
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        slot = int.from_bytes(digest[:4], "big") % dimensions
        vector[slot] += -1.0 if digest[4] & 1 else 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]

