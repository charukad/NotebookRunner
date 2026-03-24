# Colab Orchestrator Platform - Master Implementation Guide

## Development Workflow Overview
The development of the NotebookRunner platform progresses from a basic monolithic execution engine to an event-driven microservices architecture. All logic focuses critically on managing the fragile Google Colab automation connection smoothly.

## Phased Implementation Plan

### Phase 1: The Core Execution MVP
*Goal: Establish the absolute happy path from upload to model physical retrieval.*
- **Backend Setup**: Single FastAPI application housing the API and execution logic.
- **Storage**: Set up PostgreSQL for metadata relationships and MinIO or standard local filesystem (for dev) for blob storage.
- **Playwright Worker**: Construct the `ColabExecutionRunner` to successfully:
  1. Boot a persistent browser profile.
  2. Upload `.ipynb` to a new Colab runtime.
  3. Dispatch "Run All".
  4. Scrape the DOM for completion / error strings.
- **Frontend**: Scaffolding the React app with simple drag-drop file upload, job running overlay, and model download links.

### Phase 2: Observability & Asynchronous Architecture
*Goal: Ensure the API remains responsive while model training runs for hours.*
- **Queue System**: Introduce **RabbitMQ** to replace sync API calls. The `POST /jobs` endpoint simply queues an event and returns immediately.
- **State Machine**: Introduce the Job Orchestrator domain handling the `queued` -> `preparing` -> `launching` -> `running` states.
- **Live Telemetry**: Setup **Redis**. Use Playwright's DOM scraping to pull streaming print statements and broadcast them to React via WebSockets.
- **Notebook Patcher**: Build the Python service that modifies uploaded notebooks seamlessly to export structured `{ "step": 1, "loss": 0.5 }` logs instead of just plain text.

### Phase 3: SaaS Platform Features
*Goal: Evolve the utility into a multi-tenant product.*
- **Authentication**: JWT based user authentication, Projects, and Workspaces.
- **Model Registry**: Formalize the outputs. Instead of just files, create Model entities, track versions, lineages, and best accuracy metrics natively in UI.
- **Billing & Quotas**: Implement constraints. E.g., Free Tier limits a user to 1 active concurrent job, using Redis distributed locks (`acquire_job_slot(user_id)`).

### Phase 4: Scaling & Auto-healing (Production Check)
*Goal: Bulletproof the orchestrator against Colab bans, timeouts, and network drops.*
- **Microservices Shift**: Separate the Execution Connector into completely isolated containers from the API gateway.
- **Dead Letter Handling & Retries**: Only retry transient failures (like Playwright failing to locate the "Run" button). Let Python Tracebacks inside the notebook fail gracefully and display directly to the end-user.

## Critical Component: Execution Connector Worker
Because Google Colab lacks an official automation API, the system depends on an external browser automation service.
- Use `playwright.async_api` to manage chrome contexts.
- Prefer a deterministic **Artifact Export** strategy: Inject Python code that writes directly to Google Drive instead of relying on downloading files directly via browser buttons which are prone to UI changes.
- Employ screenshots / HTML dumps whenever the automaton catches an exception, for deep backend debugging.
