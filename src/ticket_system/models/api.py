from pydantic import BaseModel

class classificationRequest(BaseModel):
    ticket_id: str
    text: str