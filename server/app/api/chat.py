import time
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies import get_agent_service, get_product_service
from app.schemas.chat import ChatRequest
from app.utils.sse_utils import sse_event
from app.utils.text_utils import chunks

router = APIRouter(prefix="/api/chat")


@router.post("/stream")
async def chat_stream(request: ChatRequest, agent=Depends(get_agent_service), products=Depends(get_product_service)):
    async def events():
        message_id = f"assistant-{int(time.time() * 1000)}"
        yield sse_event("message_start", {"session_id": request.session_id, "message_id": message_id})
        try:
            answer, candidates = await agent.answer(request.session_id, request.message)
            # The backend owns cards; the LLM never controls product facts.
            for delta in chunks(answer, 12):
                yield sse_event("message_delta", {"text": delta})
            if candidates:
                yield sse_event("product_cards", {"products": [products.card(item) for item in candidates]})
        except Exception:
            yield sse_event("error", {"message": "模型服务暂时不可用，请稍后再试。"})
        yield sse_event("message_done", {"message_id": message_id})

    return StreamingResponse(events(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no",
    })

