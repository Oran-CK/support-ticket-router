from pydantic import BaseModel

class ClassificationRequest(BaseModel):
    ticket_id: str
    text: str

class ClassificationResponse(BaseModel):
    ticket_id: str
    urgency: str
    department: str