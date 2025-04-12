from pydantic import BaseModel


class ClientMessages(BaseModel):
    content: str | None
    conversation_id: str | None
    created_at: str | None
    id: str | None
    role: str | None
