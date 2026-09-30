from pydantic import BaseModel

class classificationRequest(BaseModel):
    ticket_id: str
    text: str

class classificationResponse(BaseModel):
    ticket_id: str
    urgency: str
    department: str