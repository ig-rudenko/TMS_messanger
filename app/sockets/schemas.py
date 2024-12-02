from pydantic import Field, BaseModel


class MessageRequestSchema(BaseModel):
    type: str
    status: str
    message: str
    recipient_id: int | None = Field(None)


class MessageResponseSchema(BaseModel):
    type: str
    status: str
    message: str
    recipient_id: int
    sender_id: int
    created_at: int
