import asyncio
import time
from .colab_session import ColabSessionManager
from .notebook_uploader import NotebookUploader
from .run_controller import RunController
from .output_monitor import OutputMonitor

class ColabExecutionRunner:
    """The central orchestrator for a single execution task in the Playwright worker."""
    
    def __init__(self, job_payload: dict):
        self.job_payload = job_payload
        self.started_at = time.time()
        self.session = ColabSessionManager()

    async def execute(self):
        page = await self.session.create()
        try:
            uploader = NotebookUploader(page)
            await uploader.upload_notebook(self.job_payload["patched_notebook_path"])

            runner = RunController(page)
            if self.job_payload.get("requested_gpu"):
                await runner.request_gpu()
            await runner.run_all_cells()

            monitor = OutputMonitor(page)
            # Watch loop
            timeout = self.job_payload.get("timeout_seconds", 14400)
            while True:
                if time.time() - self.started_at > timeout:
                    raise TimeoutError("Job timed out")

                text = await monitor.poll()
                state = monitor.classify_state(text)

                if state == "error":
                    # Potentially snapshot the error string
                    raise RuntimeError(f"Notebook execution failed with traceback: {text[:200]}")
                elif state == "runtime_disconnected":
                    raise ConnectionError("Colab runtime disconnected")
                
                # Check actual file readiness instead of text heuristics for completion
                # Break condition depends on exact integration
                
                await asyncio.sleep(5)
        finally:
            await self.session.close()

if __name__ == "__main__":
    # Example execution stub
    payload = {
        "job_id": "job_001",
        "patched_notebook_path": "/tmp/dummy.ipynb",
        "requested_gpu": False
    }
    # asyncio.run(ColabExecutionRunner(payload).execute())
