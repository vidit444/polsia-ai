from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    tenant_id: str
    prompt: str = Field(min_length=1, max_length=8000)
    context: dict = Field(default_factory=dict)


class AIChatResponse(BaseModel):
    provider: str
    message: str
    debug_review_interval_seconds: int
    payment_qr_url: str
