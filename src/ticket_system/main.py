from fastapi import FastAPI, HTTPException

from ticket_system.models import (
    ClassificationRequest,
    ClassificationResponse
)
from ticket_system.services import (
    classify_ticket,
    ServiceError
)

app = FastAPI()

@app.get("/health")
def api_health():
    return {"status": "ok"}

@app.post("/ticket/classify", response_model=ClassificationResponse)
def classify_ticket_endpoint(payload: ClassificationRequest):
    try:
        classification = classify_ticket(payload.text)
        return ClassificationResponse(
            ticket_id=payload.ticket_id,
            department=classification.department,
            urgency=classification.urgency
        )
    except ServiceError as se:
            raise HTTPException(status_code=502, detail=str(se))