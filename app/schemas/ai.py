from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    conversation_id: str | None = None
    channel: str = "web"
    model_preference: str | None = None
    context: dict = Field(default_factory=dict)


class AIChatResponse(BaseModel):
    conversation: dict
    user_message: dict
    assistant_message: dict
    debug: dict
