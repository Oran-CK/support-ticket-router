import ollama
import json
from pathlib import Path

from ticket_system.models import (
    ClassificationOutput
)

def load_data():
    sample_data_path = Path("data/sample_tickets.json")
    with sample_data_path.open("r", encoding="utf-8") as file:
        return json.load(file)

model_name = "llama3.2:1b"

def classify_ticket(ticket: str):

    system_prompt = """
    You are an enterprise ticket triage classifier.
    Analyze the provided ticket text and extract the department & urgency.
    Adhere strictly to the requested schema.
    """

    messages = [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": ticket }
    ]

    response = ollama.chat(
        model=model_name, 
        messages=messages,
        format=ClassificationOutput.model_json_schema()
    )
    response = response.message.content

    try:
        validated_output = ClassificationOutput.model_validate_json(response)
        return validated_output.model_dump(mode='json')
    except Exception as e:
        print(f"Failed to validate model output: {e}")
        return None

def run_classification():

    sample_data = load_data()
    results = []
    
    for ticket in sample_data:
        classification = classify_ticket(ticket["text"])

        results.append(
            {
                "id": ticket["id"],
                "classification": classification,
            }
        )

    return results

if __name__ == "__main__":
    results = run_classification()

    for r in results:
        print (r)



