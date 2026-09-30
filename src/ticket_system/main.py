from fastapi import FastAPI

from ticket_system.models import (
    classificationRequest,
    classificationResponse
)
from ticket_system.services import classify_ticket

app = FastAPI()

@app.post("/ticket/classify", response_model=classificationResponse)
def classify_ticket_endpoint(payload: classificationRequest):
    try:
        classification = classify_ticket(payload.text)
        return classificationResponse(
            ticket_id=payload.ticket_id,
            department=classification['department'],
            urgency=classification['urgency']
        )
    except Exception as e:
            print(f"\n\n--------\n\napi error {e}\n\n------\n\n")
            return None