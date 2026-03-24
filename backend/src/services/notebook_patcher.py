import json

def patch_notebook(file_content: bytes, analysis: dict, job_id: str) -> bytes:
    """
    Injects platform-specific code into the notebook before execution.
    For example: Google Drive mount, Structured Metrics logger, Artifact Exporter.
    """
    notebook = json.loads(file_content)
    
    # 1. Inject Mount Drive Cell (if needed)
    if analysis.get("needs_drive_mount", True):
        mount_cell = {
            "cell_type": "code",
            "metadata": {},
            "source": [
                "from google.colab import drive\n",
                "drive.mount('/content/drive')"
            ],
            "outputs": [],
            "execution_count": None
        }
        notebook["cells"].insert(0, mount_cell)

    # 2. Inject structured metrics logger
    logger_cell = {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "import json\n",
            "import os\n",
            "os.makedirs('/content/platform_artifacts', exist_ok=True)\n",
            "def log_metric(name, value, step=None):\n",
            "    with open('/content/platform_artifacts/metrics.jsonl', 'a') as f:\n",
            "        f.write(json.dumps({'name': name, 'value': value, 'step': step}) + '\\n')"
        ],
        "outputs": [],
        "execution_count": None
    }
    notebook["cells"].insert(1, logger_cell)

    # 3. Inject artifact exporter at the end
    export_cell = {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "import shutil\n",
            "import os\n",
            f"EXPORT_DIR = '/content/drive/MyDrive/platform_runs/{job_id}/'\n",
            "os.makedirs(EXPORT_DIR, exist_ok=True)\n",
            "for artifact in ['model.pth', 'model.h5', '/content/platform_artifacts/metrics.jsonl']:\n",
            "    if os.path.exists(artifact):\n",
            "        shutil.copy(artifact, os.path.join(EXPORT_DIR, os.path.basename(artifact)))"
        ],
        "outputs": [],
        "execution_count": None
    }
    notebook["cells"].append(export_cell)

    return json.dumps(notebook, indent=1).encode("utf-8")
