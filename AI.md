# AI.md

This document outlines how AI tools were utilized during the development of the Ticket Classification Service, noting their role in architectural decisions, where suggestions proved unhelpful or out of scope, and how every technical addition was validated.

---

## 1. Tools Used and Primary Use Cases

* **Primary Tool:** Gemini
* **Architectural Sounding Board / "Intelligent Rubber Duck":** 
  * Used primarily as a technical conversational partner to think through problems out loud. Articulating requirements and reviewing counter-arguments helped iterate on architectural boundaries, particularly decoupling the service layer (`services.py`) from FastAPI routing (`main.py`).
* **CI/CD Pipeline & Test Suite Scaffolding:** 
  * Used to refresh syntax and best practices for setting up GitHub Actions with `uv` and configuring `pytest` with FastAPI's `TestClient`. While familiar with testing and CI concepts from undergraduate software engineering modules, recent postgraduate NLP work focused primarily on model experimentation rather than test-driven delivery and automated pipelines.
* **Targeted Debugging & Refactoring:** 
  * Consulted for quick syntax references, resolving deprecation warnings (e.g., Starlette's `httpx` to `httpx2` transition), and validating Pydantic model configurations.

---

## 2. Incorrect, Flawed, or Unhelpful Suggestions

* **Over-Engineered Initial Outputs:** 
  * Early prompts prompted large, monolithic blocks of code that introduced out-of-scope features and high complexity. Adopting these generated codebases was rejected immediately; reading, untangling, and verifying pre-built scripts without full conceptual clarity offered no efficiency over building from the ground up.
* **Anti-Patterns in Serialization:** 
  * Some early recommendations suggested stripping Pydantic types using `.model_dump(mode='json')` or dictionaries inside `services.py`. This bypassed Pydantic's type safety and forced calling code to rely on string-keyed dictionary lookups instead of typed object attributes. This was corrected to keep the validated model instance intact throughout the domain layer.
* **Function-Coupled Exceptions:** 
  * Exploring custom exceptions generated suggestions tied to specific function names (e.g., `error_classify_ticket`). This would have led to redundant exception classes across the codebase. It was adjusted to a clean, domain-level `ServiceError` pattern.

---

## 3. Verification & Validation Strategy

To maintain ownership, code clarity, and architectural integrity:

* **Minimal, Granular Adoption:** 
  * AI-generated snippets were strictly limited to small, discrete building blocks (such as individual test cases, configuration syntax, or isolated lines of code) rather than copied implementations.
* **Incremental Execution:** 
  * Every snippet or refactored block was verified immediately in an isolated run before committing. Tests were executed via `uv run pytest`, sample tickets were processed via `uv run python -m ticket_system.demo`, and live API contracts were checked in Swagger UI.
* **Ground-Up Implementation:** 
  * Stepping through code iteratively forced an active understanding of every imported module, exception boundary, and schema definition, ensuring no unexplainable code entered the repository.