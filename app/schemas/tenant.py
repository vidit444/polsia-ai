from pydantic import BaseModel, Field


class TenantOnboardRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    plan: str = Field(min_length=2, max_length=100)
    status: str = Field(min_length=2, max_length=50)


class TenantResponse(BaseModel):
    id: str
    name: str
    plan: str
    status: str
