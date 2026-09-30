from fastapi import FastAPI

from ticket_system.models import (
    classificationRequest
)
from ticket_system.services import classify_ticket

app = FastAPI()

@app.post("/ticket/classify")
def classify_ticket_endpoint(payload: classificationRequest):

    classification = classify_ticket(payload.text)
    return (classification)