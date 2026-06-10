import json
import httpx


class DoubaoClient:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key, self.base_url, self.model = api_key, base_url.rstrip("/"), model

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.model)

    async def complete(self, messages: list[dict]) -> str:
        if not self.configured:
            raise RuntimeError("Doubao is not configured")
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": messages, "stream": False},
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def stream(self, messages: list[dict]):
        if not self.configured:
            raise RuntimeError("Doubao is not configured")
        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream(
                "POST", f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": messages, "stream": True},
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.startswith("data: ") or line == "data: [DONE]":
                        continue
                    data = json.loads(line[6:])
                    text = data["choices"][0].get("delta", {}).get("content", "")
                    if text:
                        yield text

