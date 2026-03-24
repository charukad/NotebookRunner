# Colab Orchestrator Platform - Master Task List

This document breaks down the NotebookRunner project into manageable development phases and actionable tasks. To enforce good version control practices, **20 specific GitHub commit and push milestones** have been distributed throughout the project, strictly adhering to the project's commit message conventions.

---

## Phase 1: Project Initialization & Documentation

- [x] Initialize Python virtual environment and basic directory structure (`backend/` and `frontend/`).
- [x] Initialize the React project with Vite/Next.js and Tailwind CSS in the `frontend` folder.
- [x] Initialize FastAPI app structure in `backend`.
- [x] **Git Task 1**: Commit and push initial scaffolding.
  - *Command*: `git commit -m "chore(setup): initialize backend and frontend monolithic folders" && git push`
- [x] Add all architecture and requirement `.md` files to the repository docs.
- [x] **Git Task 2**: Commit and push project documentation.
  - *Command*: `git commit -m "docs(architecture): add complete project documentation and implementation plans" && git push`

## Phase 2: Database & Core Infrastructure

- [x] Set up Docker Compose file with PostgreSQL, Redis, RabbitMQ, and MinIO.
- [x] Configure Python ORM (e.g., SQLAlchemy/Prisma) and connect to the PostgreSQL database.
- [x] Create database models for `Users`, `Workspaces`, and `Projects`.
- [x] **Git Task 3**: Commit and push user/project schemas.
  - *Command*: `git commit -m "feat(db): setup PostgreSQL schemas for users and projects" && git push`
- [x] Create database models for `Notebooks`, `Jobs`, `Metrics`, and `Models`.
- [x] **Git Task 4**: Commit and push system-specific schemas.
  - *Command*: `git commit -m "feat(db): setup schemas for notebooks, jobs, and models" && git push`
- [x] Create the S3/MinIO client connection for blob storage and Redis client for caching.
- [x] **Git Task 5**: Commit and push infrastructure integrations.
  - *Command*: `git commit -m "feat(infra): integrate MinIO and Redis connections" && git push`

## Phase 3: Backend API Services (MVP)

- [x] Implement REST endpoints for Workspace and Project CRUD operations.
- [x] **Git Task 6**: Commit and push Workspace APIs.
  - *Command*: `git commit -m "feat(api): implement workspace and project management endpoints" && git push`
- [x] Implement the Notebook Service: API for `.ipynb` file upload to MinIO and validation.
- [x] **Git Task 7**: Commit and push Notebook Service APIs.
  - *Command*: `git commit -m "feat(notebook): implement notebook upload and validation service" && git push`
- [x] Implement the **Notebook Analyzer & Patcher**: Python scripts to parse `.ipynb`, detect frameworks, and inject Google Drive mount/logging code.
- [x] **Git Task 8**: Commit and push Notebook Patcher.
  - *Command*: `git commit -m "feat(analyzer): build smart notebook analyzer and code patcher" && git push`
- [x] Implement the **Job Orchestrator**: Build the status state machine (`created` -> `running` -> `completed`).
- [x] **Git Task 9**: Commit and push Job Orchestrator logic.
  - *Command*: `git commit -m "feat(jobs): create job orchestrator state machine" && git push`

## Phase 4: Execution Connector (Playwright Worker)

- [x] Set up `playwright.async_api` Python worker environment.
- [x] Build the `ColabSessionManager` to manage authenticated Chrome profiles.
- [x] **Git Task 10**: Commit and push Colab session manager. (Skipped per request)
- [x] Build the `NotebookUploader` and `RunController` algorithms for clicking through the Google Colab UI.
- [x] **Git Task 11**: Commit and push Notebook automation execution. (Skipped per request)
- [x] Implement the DOM scraper to extract cell outputs, and broadcast logs via WebSockets mapped in Redis.
- [x] **Git Task 12**: Commit and push Telemetry services. (Skipped per request)
- [x] Build the `ArtifactBridge` to download the final Google Drive files (`model.pth`) and push to MinIO Model Registry.
- [x] **Git Task 13**: Commit and push Artifact collector. (Skipped per request)

## Phase 5: Asynchronous Processing & Message Broker

- [x] Install and configure Pika/Celery for RabbitMQ queues (`job.prepare`, `job.execute`, `job.collect_artifacts`).
- [x] **Git Task 14**: Commit and push RabbitMQ integration. (Skipped per request)
- [x] Refactor the synchronous Job Orchestrator API to strictly publish tasks to RabbitMQ.
- [x] Refactor the Execution Connector into an isolated RabbitMQ consumer worker.
- [x] **Git Task 15**: Commit and push architectural refactoring. (Skipped per request)

## Phase 6: Web Dashboard (React Frontend)

- [ ] Implement generic dashboard layout (Sidebar, TopNav) and Project browsing components.
- [ ] Ensure frontend state management is configured with TanStack Query and Zustand.
- [ ] **Git Task 16**: Commit and push UI layouts.
  - *Command*: `git commit -m "feat(ui): implement dashboard layout, project list, and router" && git push`
- [ ] Build the "Upload Notebook" Drag-and-Drop page with pre-validation UI feedback.
- [ ] **Git Task 17**: Commit and push Uploader UI.
  - *Command*: `git commit -m "feat(ui): build notebook drag-and-drop uploader page" && git push`
- [ ] Build the **Job Terminal Page**: WebSocket terminal for live streaming logs and a Recharts graph for trailing loss metrics.
- [ ] **Git Task 18**: Commit and push Live Terminal UI.
  - *Command*: `git commit -m "feat(ui): implement live job terminal view with charts and streaming logs" && git push`
- [ ] Build the Model Registry page: Showing downloaded models with active download links and history lineage.
- [ ] **Git Task 19**: Commit and push Model Registry UI.
  - *Command*: `git commit -m "feat(ui): add model registry and artifact download capabilities" && git push`

## Phase 7: Security, Testing, & Finalization

- [ ] Implement JWT Authentication mechanisms on both Frontend and Backend API endpoints.
- [ ] Implement Free/Pro tier quota limitations using Redis variables.
- [ ] **Git Task 20**: Commit and push final security layers.
  - *Command*: `git commit -m "feat(auth): integrate JWT authentication and user quotas" && git push`
