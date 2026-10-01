from unittest.mock import patch
from fastapi.testclient import TestClient
from ticket_system.main import app
from ticket_system.models.enum import Department, Urgency
from ticket_system.models.llm import ClassificationOutput

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_classify_endpoint_success():
    mock_llm_output = ClassificationOutput(
        department=Department.BILLING,
        urgency=Urgency.HIGH
    )
    
    with patch("ticket_system.main.classify_ticket", return_value=mock_llm_output):
        payload = {"ticket_id": "TCK-100", "text": "Refund request"}
        response = client.post("/ticket/classify", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["ticket_id"] == "TCK-100"
        assert data["department"] == "Billing"
        assert data["urgency"] == "HIGH"