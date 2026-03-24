# Colab Orchestrator Platform - Technical Architecture Reference

## Technology Stack
- **Frontend**: React (TanStack Query for server state caching)
- **Backend API & Framework**: FastAPI (Python)
- **Message Broker**: RabbitMQ (Task queues, async orchestration)
- **Cache & Real-time State**: Redis (Job states, WebSocket log pub/sub)
- **Primary Database**: PostgreSQL (Relational metadata)
- **Object Storage**: MinIO / S3 (Notebook files, trained model binaries, logs)
- **Remote Automation**: Playwright (Headless browser automation for Colab manipulation)

## Core Microservices Architecture
The system employs an event-driven architecture using RabbitMQ to decouple long-running ML jobs from the API surface.
1. **API Gateway**: Single entry point handling REST and WebSockets.
2. **Auth & Workspace Services**: Identity, roles, JWT, quotas, and limits.
3. **Notebook Service**: Validates, versions, and stores raw uploads.
4. **Notebook Analyzer & Patcher**: Semantically analyzes Python notebooks to detect ML frameworks and injects tracking, storage mounting, and artifact export Python code.
5. **Job Orchestrator State Machine**: Central brain managing the job lifecycle (`created` -> `preparing` -> `patched` -> `launching` -> `running` -> `collecting_artifacts` -> `completed`/`failed`).
6. **Execution Connector**: Dedicated isolated worker running Playwright to securely allocate, monitor, and scrape Colab sessions.
7. **Telemetry Services (Logs/Metrics)**: Ingests streaming standard output and JSON lines injected by the patcher.
8. **Artifact Collector & Model Registry**: Downloads output files, stores them into MinIO, and establishes relational registry in PostgreSQL.

## Database Schema (PostgreSQL Highlights)
- **Users & Auth**: `users`, `sessions`
- **Workspaces & Projects**: `workspaces`, `workspace_members`, `projects`
- **Notebooks**: `notebooks`, `notebook_versions`, `notebook_metadata`
- **Jobs**: `jobs`, `job_status_history`, `job_failues`, `job_config`
- **Telemetry**: `job_logs`, `job_metrics`, `job_summary`
- **Registry**: `artifacts`, `models`, `model_versions`, `model_lineage`

## Message Queue Topics (RabbitMQ)
- `notebook.uploaded`
- `notebook.analyze` / `notebook.patch`
- `job.prepare` / `job.launch` / `job.collect_artifacts`
- `model.register`
- `job.dead_letter`

## Critical Operations & Security
- **Execution Connector Isolation**: The worker executing automation scripts must run in isolated containers; an uploaded notebook should **never** have direct network access to internal backend secrets.
- **State Retry Policies**: The system distinguishes between transparent platform errors (e.g. browser context crash, which should retry) vs user code errors (e.g. Python traceback in Colab, which should fail directly).
- **Artifact Bridge**: Because direct downloading from Colab runtime is unreliable, the Notebook Patcher injects a script forcing Colab to sync outputs directly to a connected Google Drive path, which the Artifact Collector then reads via official APIs.
