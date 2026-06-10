from pydantic import BaseModel


class MessageDelta(BaseModel):
    text: str


class MessageDone(BaseModel):
    message_id: str

