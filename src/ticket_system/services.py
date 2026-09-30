import ollama

from ticket_system.models import (
    ClassificationOutput
)

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
        print(f"\n\n--------\n\nFailed to validate model output: {e}\n\n------\n\n")
        return None





