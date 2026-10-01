# RESEARCH.md

This document outlines the key decisions, learning processes, challenges, and architectural choices made throughout the development of the Ticket Classification Service.

---

## 1. Local LLM Selection & Structured Extraction

### What Needed to Be Learned & Why
* **Local Inference vs. Cloud APIs:** Decided to implement `llama3.2:1b` locally using Ollama rather than relying on commercial cloud APIs (e.g., OpenAI or Anthropic).
* **Motivations:**
  1. **Data Privacy & Compliance:** Help desk tickets routinely contain sensitive personal details, billing references, and credentials. Processing requests locally ensures no user data leaves the network perimeter.
  2. **Reviewer Friction:** Relying on paid cloud providers requires reviewers to configure environment variables and API keys. A local model guarantees a self-contained, reproducible testing environment.
  3. **Technical Exploration:** Re-engaging with local model inference after previously needing to pivot to APIs during MSc dissertation work due to time constraints.

### Investigation & Evaluation
* Drawing on previous academic experience with Retrieval-Augmented Generation (RAG) pipelines, attempts to enforce structure on small parameter models solely via plaintext prompting frequently lead to verbose outputs, hallucinated formatting, and inconsistent JSON structures.
* Evaluated Ollama’s structured schema decoding by supplying `format=ClassificationOutput.model_json_schema()`.

### Findings & Key Takeaway
* Prompt engineering small language models without schema enforcement produces inconsistent, fragile outputs.
* Enforcing JSON schemas directly at the inference layer via Pydantic model schemas ensures 100% adherence to domain enums (`Department`, `Urgency`), eliminating output parsing failures and keeping the service deterministic.

---

## 2. Architecture & Service Layer Error Boundaries

### What Needed to Be Learned & Why
* Determining the cleanest contract between the internal inference service (`services.py`) and the public API routing layer (`main.py`).

### Approaches Tested & Problems Encountered
* **Result Tuples & `None` Returns:** Initially considered returning tuples `(status, message)` or `None` on inference or parsing failures. 
* **Issues:** This pattern polluted callers with repetitive conditional checks, masked upstream tracebacks, and passed untyped error strings down the execution chain. It also prevented clean schema serialization in FastAPI endpoints.

### Solution: Domain Exceptions (`ServiceError`)
* Implemented a dedicated domain exception `ServiceError` within the service module to capture LLM connection drops or validation issues.
* **Separation of Concerns:** Internal exceptions remain strictly internal, while the API transport layer maps those domain failures to clear outward-facing HTTP status codes (`502 Bad Gateway`). This keeps code readable and prevents internal programming bugs from being masked as generic API responses.

---

## 3. Test Isolation & CI Pipeline Strategy

### What Needed to Be Learned & Why
* Ensuring that integration tests and automated checks can run reliably across different machines and continuous integration (CI) runners without needing local GPU hardware or an active Ollama instance.

### Implementation & Issues Encountered
1. **In-Memory Testing with `TestClient`:**
   * Used FastAPI's `TestClient` inside `demo.py` and `pytest` suites to execute the complete FastAPI middleware, validation, and serialization pipeline in-memory, avoiding the need for an external web server process.
2. **Deprecation Warnings:**
   * During early test execution, Starlette’s test client emitted deprecation warnings regarding the underlying `httpx` transport. Identified the migration path and installed `httpx2` to keep test outputs clean.
3. **Data Path Normalization:**
   * Early versions used hardcoded relative paths for `sample_tickets.json`, which caused lookup errors when commands were run outside the module folder. Switched to path resolution relative to the repository root.
4. **CI Isolation via Mocking:**
   * In GitHub Actions, installing and running Ollama on ephemeral runners would add unnecessary runtime, high compute costs, and flakiness. Mocked the `classify_ticket` boundary during automated endpoint tests to validate routing, error codes, and Pydantic validation cleanly and quickly.

---

## 4. Modern Tooling & GitHub Actions CI

### Tooling Adoption (`uv`)
* Utilized `uv` for dependency management and environment isolation based on prior experience using it during an MSc dissertation to eliminate cross-platform dependency resolution issues for assessors.
* Leveraged `uv sync` and `uv run` to guarantee deterministic builds across local development and GitHub Actions runners.

### GitHub Actions Troubleshooting
* **Directory Structure Syntax:** Initial CI runs failed to register on GitHub due to creating the workflow folder path with a singular name (`.github/workflow/`) instead of the required `.github/workflows/`.
* **Workflow Detection:** Configured `workflow_dispatch` alongside `push` triggers to force the GitHub interface to detect the workflow and allow immediate manual verification runs from the Actions tab.

---

## Summary of Core Takeaways
* **Strict Schemas Over Prompt Tweaking:** Pydantic JSON schemas are essential for reliable production behavior when working with small, local language models.
* **Layered Boundaries:** Keep internal service errors decoupled from outward-facing HTTP constructs.
* **CI Simplicity:** Fast, isolated tests mocking external infrastructure dependencies provide superior feedback loops compared to running heavy models inside CI runners.