import asyncio

class NotebookUploader:
    """Handles parsing the Colab UI to automate File Uploads."""
    
    def __init__(self, page):
        self.page = page

    async def open_upload_dialog(self):
        # Depending on Colab's current UI, this might be under File -> Upload or the welcome screen
        try:
            await self.page.get_by_text("Upload").click(timeout=5000)
        except:
            # Fallback if welcome modal is missing: Menu -> File -> Upload notebook
            await self.page.get_by_text("File", exact=True).click()
            await self.page.get_by_text("Upload notebook").click()

    async def upload_notebook(self, file_path: str):
        await self.open_upload_dialog()
        
        file_chooser_future = self.page.wait_for_event("filechooser")
        # In the iframe or modal for upload:
        await self.page.get_by_text("Browse").click()
        
        file_chooser = await file_chooser_future
        await file_chooser.set_files(file_path)
        
        # Wait for network idle assuming the notebook takes a few seconds to load
        await self.page.wait_for_load_state("networkidle")
        await asyncio.sleep(3) # safe padding
