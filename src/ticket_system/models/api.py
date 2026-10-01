from pydantic import BaseModel, Field

from ticket_system.models.enum import (
    Department,
    Urgency
)

class ClassificationRequest(BaseModel):
    ticket_id: str = Field(..., examples=["TCK-001"])
    text: str = Field(..., examples=["I can't access your website, please help"])

class ClassificationResponse(BaseModel):
    ticket_id: str = Field(..., examples=["TCK-001"])
    urgency: Urgency = Field(..., examples=["Low"])
    department: Department = Field(..., examples=["Support"])