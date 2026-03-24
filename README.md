# NotebookRunner - Colab Orchestrator Platform

A SaaS platform designed to orchestrate and automate Jupyter Notebook training workflows against Google Colab using a scalable architecture.

## Overview

NotebookRunner allows users to upload Jupyter Notebooks and execute them remotely on Google Colab hardware. The system features:
- **FastAPI Backend:** Handles Workspaces, Projects, API Endpoints, and strictly typed ORM models (SQLAlchemy).
- **React Frontend:** A modern, Vite-powered Dashboard with Tailwind CSS and Zustand state management.
- **Playwright Execution Worker:** Headless browser automation that injects Colab sessions, handles Google account authentication securely, and parses DOM status.
- **Message Broker:** Asynchronous routing with RabbitMQ (`aio-pika`), fully decoupling frontend requests from synchronous notebook runs.

## Architecture Stack

- **Backend:** Python + FastAPI + PostgreSQL + SQLAlchemy + Alembic
- **Frontend:** React + Vite + Tailwind CSS + Recharts (Live status graphs)
- **Infrastructure:** Docker Compose, Redis (Caching/Sockets), RabbitMQ (Queues), MinIO (Blob Object Storage / Model Registry)
- **Automations:** Playwright async

## Setup & Startup Instructions

### 1. Requirements
Ensure you have Docker and Docker Compose installed. Node.js (>=18) and Python (>=3.9) are required for manual dev mode.

### 2. Booting Infrastructure
Start PostgreSQL, MinIO, Redis, and RabbitMQ using Docker Compose:
```bash
docker-compose up -d
```

### 3. Backend Setup
Set up the Python environment, migrate databases, and run the server:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the API server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
In a new terminal window, start the RabbitMQ Playwright Consumer:
```bash
cd backend
source .venv/bin/activate
python -m src.workers.queue.consumer
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The React app will be live on `http://localhost:5173`. Play around with the Workspaces and Notebook runners!

## Testing Coverage
Comprehensive `pytest` test suites exist in `backend/tests/`. To run:
```bash
cd backend
python -m pytest tests/
```
