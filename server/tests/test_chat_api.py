from fastapi.testclient import TestClient
from app.main import app


def test_chat_sse_contains_required_events():
    response = TestClient(app).post("/api/chat/stream", json={
        "session_id": "pytest-demo", "message": "推荐一款适合油皮的护肤品",
    })
    assert response.status_code == 200
    body = response.text
    for event in ["message_start", "message_delta", "product_cards", "message_done"]:
        assert f"event: {event}" in body

