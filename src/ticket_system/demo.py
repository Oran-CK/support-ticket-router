import json
from pathlib import Path
from fastapi.testclient import TestClient
from ticket_system.main import app

client = TestClient(app)

def load_data():
    sample_data_path = Path("data/sample_tickets.json")
    with sample_data_path.open("r", encoding="utf-8") as file:
        return json.load(file)

def run_demo():

    sample_data = load_data()
    results = []
    
    for ticket in sample_data:

        payload = {
            "ticket_id": ticket["id"],
            "text": ticket["text"]
        }

        response = client.post("/ticket/classify", json=payload)

        print(f"\nStatus Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error:", response.text)
        print("-" * 40)

if __name__ == "__main__":
    run_demo()