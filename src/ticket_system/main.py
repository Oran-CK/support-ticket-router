import ollama
import json
from pathlib import Path

from ticket_system.models import (
    ClassificationOutput
)

model_name = "llama3.2:1b"

sample_data_path = Path("data/sample_tickets.json")
with sample_data_path.open("r", encoding="utf-8") as file:
    sample_data = json.load(file)

system_prompt = """
You are an enterprise ticket triage classifier.
Analyze the provided ticket text and extract the department & urgency.
Adhere strictly to the requested schema.
"""

for ticket in sample_data:

    messages = [
        {
            "role": "system", 
            "content": system_prompt
        },
        {
            "role": "user", 
            "content": ticket['text']
        },
    ]

    response = ollama.chat(
        model=model_name, 
        messages=messages,
        format=ClassificationOutput.model_json_schema()
    )

    print ("----------------------------------")
    print("Response:", response.message.content)
    print ("----------------------------------")

