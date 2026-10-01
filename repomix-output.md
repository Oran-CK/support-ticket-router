This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
data/
  sample_tickets.json
src/
  ticket_system/
    models/
      __init__.py
      api.py
      enum.py
      llm.py
    __init__.py
    demo.py
    main.py
    services.py
.gitignore
.python-version
pyproject.toml
README.md
```

# Files

## File: data/sample_tickets.json
```json
[
  {
    "id": "TCK-001",
    "text": "EMERGENCY: The main API database is throwing 504 gateway timeouts. All European checkout services are completely down for customers."
  },
  {
    "id": "TCK-002",
    "text": "Hello, I noticed I was charged twice for invoice #9402 on my credit card this morning. Can someone please process a refund for the extra charge?"
  },
  {
    "id": "TCK-003",
    "text": "Hi there, where in the dashboard settings can I change my profile email address and enable dark mode?"
  }
]
```

## File: src/ticket_system/models/enum.py
```python
from enum import Enum

class Department(str, Enum):
    INFRASTRUCTURE = "Infrastructure"
    BILLING = "Billing"
    SECURITY = "Security"
    SUPPORT = "Support"

class Urgency(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
```

## File: src/ticket_system/models/llm.py
```python
from pydantic import BaseModel, Field

from ticket_system.models.enum import (
    Department,
    Urgency
)

class ClassificationOutput(BaseModel):
    department: Department = Field(
        ...,
        description=(
            "Primary operational team to handle this request: "
            "Infrastructure for server/database/network downtime, "
            "Billing for payments/invoices/refunds, "
            "Security for unauthorized access/vulnerabilities, "
            "or Support for user accounts/how-to guidance."
        ),
    )
    urgency: Urgency = Field(
        ...,
        description=(
            "Operational severity: "
            "CRITICAL for production outages and system-wide downtime, "
            "HIGH for severe degradation or blocked workflows, "
            "MEDIUM for billing issues or single-user bugs, "
            "LOW for general questions and cosmetic requests."
        ),
    )
```

## File: src/ticket_system/__init__.py
```python

```

## File: .gitignore
```
# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
```

## File: .python-version
```
3.14
```

## File: README.md
```markdown

```

## File: src/ticket_system/demo.py
```python
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
```

## File: src/ticket_system/services.py
```python
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
```

## File: src/ticket_system/models/__init__.py
```python
from ticket_system.models.llm import ClassificationOutput
from ticket_system.models.api import (
    ClassificationRequest,
    ClassificationResponse
)

__all__ = [
    "ClassificationOutput",
    "ClassificationRequest",
    "ClassificationResponse",
]
```

## File: pyproject.toml
```toml
[project]
name = "ticket-system"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Oran-CK", email = "oran889@gmail.com" }
]
requires-python = ">=3.14"
dependencies = [
    "fastapi[standard]>=0.141.1",
    "httpx2>=2.13.1",
    "ollama>=0.6.3",
]

[build-system]
requires = ["uv_build>=0.12.15,<0.13.0"]
build-backend = "uv_build"
```

## File: src/ticket_system/models/api.py
```python
from pydantic import BaseModel, Field

from ticket_system.models.enum import (
    Department,
    Urgency
)

class ClassificationRequest(BaseModel):
    ticket_id: str = Field(..., examples=["TCK-001"])
    text: str = Field(..., examples=["I can't access your website, please help"])

class ClassificationResponse(BaseModel):
    ticket_id: str = Field(..., examples=["TCK-001"])
    urgency: Urgency = Field(..., examples=["low"])
    department: Department = Field(..., examples=["Support"])
```

## File: src/ticket_system/main.py
```python
from fastapi import FastAPI, HTTPException

from ticket_system.models import (
    ClassificationRequest,
    ClassificationResponse
)
from ticket_system.services import (
    classify_ticket,
    ServiceError
)

app = FastAPI(
    title="ticket_system",
    version="0.1",
    description="LLM powered support ticket department and urgency classify"
)

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
```
