from playwright.async_api import async_playwright
import os

class ColabSessionManager:
    """Manages the persistent Chromium context mapping to a logged-in Google Profile."""
    
    def __init__(self, profile_dir: str = "./profiles/colab-user-1"):
        self.profile_dir = profile_dir
        self.playwright = None
        self.browser = None
        self.page = None

    async def create(self):
        os.makedirs(self.profile_dir, exist_ok=True)
        self.playwright = await async_playwright().start()
        # Launching persistent context ensures cookies/sessions from a Google login persist.
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_dir,
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        self.page = await self.browser.new_page()
        # Navigate to Colab
        await self.page.goto("https://colab.research.google.com/", wait_until="domcontentloaded")
        return self.page

    async def close(self):
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
