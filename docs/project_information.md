# Colab Orchestrator Platform (NotebookRunner) - Project Information

## Core Concept
The platform is a SaaS application designed for distributed notebook-training orchestration. It enables users to upload Jupyter Notebooks (`.ipynb`), automatically patches them, securely executes them on remote environments like Google Colab, streams metrics/logs, and collects resulting model artifacts (like `.pth` or `.h5` files) into a managed registry.

## Target Users
- **Free users**: Utilizing the Google Colab execution backend.
- **Advanced users**: Utilizing a Local GPU execution backend.
- **Paid users**: Utilizing Cloud (AWS/GCP) dedicated backends.

## Platform Features

### 1. Workspace and Project Management
- Group notebooks, jobs, models, and datasets logically into projects.
- Support for individual workspaces and team-based collaboration.

### 2. Notebook Management
- Drag-and-drop `.ipynb` file uploading.
- Version control for notebook iterations.
- **Smart Analyzer & Patcher**: Automatically detects the ML framework (PyTorch/TensorFlow) and injects essential initialization code (e.g., Google Drive mounting, structured logging, and automatic model export scripts) before remote execution.

### 3. Remote Execution Orchestration
- Uses headless browser automation (Playwright/Puppeteer) to securely manage Google Colab sessions on the backend without official API access.
- Managed leasing of runtime sessions and auto-reconnection in case of disconnections.

### 4. Live Monitoring & Telemetry
- Real-time streaming of execution logs to the frontend via WebSockets/SSE.
- Live visualization of evaluation metrics (e.g., training loss, accuracy curves) extracted in real-time from the running environment.

### 5. Artifact & Model Registry
- Automatic collection of compiled models, checkpoints, logs, and evaluation reports.
- Immutable model registries with lineage tracking (connecting an artifact back to the exact notebook version and job run).
- 1-click downloads for trained model binaries.

### 6. Billing and Quota System
- Subscription tier limitations: Limits on concurrent jobs, maximum daily runs, and artifact storage capacity.

## User Interface Pages
- **Dashboard**: High-level stats, active/recent jobs, recent models, and quota usage.
- **Projects List & Detail**: Grid of workspaces and detailed view of a project's notebooks, jobs, and models.
- **Notebook Upload**: User-friendly drag-and-drop with pre-validation and patch suggestions.
- **Job Detail**: The core "terminal" interface featuring top summary bar, timeline, streaming live logs, metric charts, and artifact list upon completion.
- **Model Registry & Detail**: Searchable database of trained models and specific version downloads.
