import asyncio

class RunController:
    """Handles the 'Run All' command and GPU configuration."""
    
    def __init__(self, page):
        self.page = page

    async def request_gpu(self):
        """Attempts to open runtime settings and select GPU if not allocated."""
        # This is UI intensive and brittle. Ideal pseudo-logic:
        # Runtime -> Change runtime type -> Hardware accelerator -> GPU -> Save
        pass

    async def run_all_cells(self):
        """Simulates the Run All command."""
        # Meta+F9 is mapped to run all in Colab
        await self.page.keyboard.press("Meta+F9")
        
        # Colab often warns "Warning: This notebook was not authored by Google."
        try:
            warning_run = self.page.get_by_role("button", name="Run Anyway")
            await warning_run.click(timeout=3000)
        except:
            pass # No warning
            
        await asyncio.sleep(2)
