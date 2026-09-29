import ollama
import json
from enum import Enum
from pydantic import BaseModel
from pathlib import Path


model_name = "llama3.2:1b"

sample_data_path = Path("data/sample_tickets.json")
with sample_data_path.open("r", encoding="utf-8") as file:
    sample_data = json.load(file)

class Urgency(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class classificationOutput(BaseModel):
    urgency: Urgency


system_prompt = """
    You are an automated ticket triage classifier.
    Analyze the user's ticket text and classify them as either HIGH, MEDIUM or LOW priority
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
        format=classificationOutput.model_json_schema()
    )

    print ("----------------------------------")
    print("Response:", response.message.content)
    print ("----------------------------------")

