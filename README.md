# Support Ticket Router / ticket_system

FastAPI service for classifying support tickets by urgency and department using a local LLM.

## Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Ollama](https://ollama.com/) running locally with the `llama3.2:1b` model:
  ```bash
  ollama pull llama3.2:1b

## Running the application

Run the following commands within the root directory of the project

1. `uv sync`
2. `uv run fastapi dev src/ticket_system/main.py`
3. `uv run python -m ticket_system.demo`
4. `uv run pytest`

## What Was Built and Why
Manual ticket triage requires support staff to read every inbound request simply to determine the correct department, creating a bottleneck that delays resolution. This service automates triage into an always-on background routing layer to ensure immediate classification.

An LLM was chosen over regular expressions for two reasons:
* **Coverage vs. Brittleness:** Rule-based regex requires manually coding patterns for every scenario and inevitably fails on edge cases. LLMs generalize across varied natural language phrasing without ongoing rule maintenance.
* **Domain Alignment:** Leveraging an LLM aligned with postgraduate NLP work, offering a more flexible architecture than static pattern matching while leaving open the possibility of future hybrid regex/LLM pipelines.

## How It Works
1. **Ingestion & Validation:** A client submits a JSON payload (`ticket_id` and ticket `text`) to `POST /ticket/classify`, which is validated by FastAPI against `ClassificationRequest`.
2. **Inference Orchestration:** The route passes the ticket text to `services.py`, which injects it into a triage system prompt and sends it to Ollama running `llama3.2:1b`.
3. **Constrained Schema Decoding:** The inference call uses a JSON schema generated from the `ClassificationOutput` model (`Department` and `Urgency` enums).
4. **Validation & Exception Handling:** The raw JSON output is parsed by Pydantic. If validation fails or Ollama is offline, a domain `ServiceError` is raised and mapped to an HTTP `502 Bad Gateway`.
5. **Response Delivery:** On success, the endpoint returns a `ClassificationResponse` combining the original `ticket_id` with the assigned `department` and `urgency`.

## What Could Be Improved With More Time
* **External Configuration:** Move the model selection, system prompt, departments, and urgency tiers to a single YAML/JSON configuration file so organizations can adapt routing without changing source code.
* **Explainability:** Extend the output schema to include the model's reasoning or confidence score to assist with human auditing.
* **Rate Limiting & Concurrency Queues:** Implement request queuing (e.g., Redis or Celery) to prevent concurrent requests from overloading local hardware inference.
* **Batch Processing:** Add a `/ticket/batch` endpoint to classify bulk tickets from uploaded JSON or Excel files.
* **Structured Logging:** Add structured JSON logging with latency metrics and request tracing.

## Additional Considerations
* **Middleware Design:** The service is designed as stateless middleware intended solely to sit as an API between customer-facing frontends and internal ticketing backends.
* **Demo vs. CI Separation:** `demo.py` executes live inference against Ollama to demonstrate local LLM parsing in one command. The test suite mocks this boundary so continuous integration tests run quickly and reliably on remote runners without requiring GPU/model hardware.