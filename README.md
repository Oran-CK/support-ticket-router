# Support Ticket Router / ticket_system

FastAPI API for classififying support tickets based on urgency and department using an llm.

## Architecture Overview
- **API Layer (`main.py`)**: FastAPI interface handling request validation, routing, and HTTP exception mappings.
- **Service Layer (`services.py`)**: Decoupled domain service isolating LLM orchestration and Pydantic schema validation.
- **Models (`models/`)**: Structured schemas separating external API payloads from internal LLM outputs and domain Enums.

## Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Ollama](https://ollama.com/) running locally with the `llama3.2:1b` model:
  ```bash
  ollama pull llama3.2:1b

## Running the application

1.
```
uv sync

```
2.
```
uv run fastapi dev src/ticket_system/main.py
```
3.
```
uv run python -m ticket_system.demo
```
4.
```
uv run pytest
```