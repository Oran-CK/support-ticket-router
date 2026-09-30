from fastapi import FastAPI, HTTPException

from ticket_system.models import (
    classificationRequest,
    classificationResponse
)
from ticket_system.services import (
    classify_ticket,
    ServiceError
)

app = FastAPI()

@app.post("/ticket/classify", response_model=classificationResponse)
def classify_ticket_endpoint(payload: classificationRequest):
    try:
        classification = classify_ticket(payload.text)
        print ("\n\n---\n\n",classification,"\n\n---\n\n")
        return classificationResponse(
            ticket_id=payload.ticket_id,
            department=classification.department,
            urgency=classification.urgency
        )
    except ServiceError as se:
            raise HTTPException(status_code=502, detail=str(se))