from pydantic import BaseModel

from ticket_system.models.enum import (
    Department,
    Urgency
)

class ClassificationRequest(BaseModel):
    ticket_id: str
    text: str

class ClassificationResponse(BaseModel):
    ticket_id: str
    urgency: Urgency
    department: Department