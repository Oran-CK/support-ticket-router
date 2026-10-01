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

@app.post("/ticket/classify", response_model=ClassificationResponse)
def classify_ticket_endpoint(payload: ClassificationRequest):
    try:
        classification = classify_ticket(payload.text)
        print ("\n\n---\n\n",classification,"\n\n---\n\n")
        return ClassificationResponse(
            ticket_id=payload.ticket_id,
            department=classification.department,
            urgency=classification.urgency
        )
    except ServiceError as se:
            raise HTTPException(status_code=502, detail=str(se))