import ollama

from ticket_system.models import (
    ClassificationOutput
)

model_name = "llama3.2:1b"

class ServiceError(Exception):
    def __init__(self, message: str, error: str):
        super().__init__(message)
        self.message = message
        self.error = error

def classify_ticket(ticket: str) -> ClassificationOutput:

    system_prompt = """
    You are an enterprise ticket triage classifier.
    Analyze the provided ticket text and extract the department & urgency.
    Adhere strictly to the requested schema.
    """

    messages = [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": ticket }
    ]
    try:
        response = ollama.chat(
                model=model_name, 
                messages=messages,
                format=ClassificationOutput.model_json_schema()
            )
        response = response.message.content
    except Exception as e:
        raise ServiceError(message="LLM failed to classify ticket", error=e) from e

    try:
        validated_output = ClassificationOutput.model_validate_json(response)
        return validated_output
    except Exception as e:
        raise ServiceError(message="Failed to validate model", error=e) from e




