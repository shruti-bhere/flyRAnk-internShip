from pydantic import BaseModel, Field
from typing import Optional

class GenerateRequest(BaseModel):
    input_tokens: int = Field(default=100, ge=0)
    cached_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=50, ge=0)
    reasoning_tokens: int = Field(default=0, ge=0)

class UsageResponse(BaseModel):
    tenant_id: str
    plan_name: str
    api_calls_used: int
    api_calls_limit: int
    tokens_used: int
    tokens_limit: int
    total_cost_usd: float