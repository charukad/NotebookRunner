class OutputMonitor:
    """Scrapes the DOM continuously to identify logs, step metrics, and fatal errors."""
    
    def __init__(self, page):
        self.page = page

    async def poll(self) -> str:
        """Pulls the entire visible notebook text."""
        try:
            text = await self.page.locator("body").inner_text()
            return text
        except Exception:
            return ""

    def classify_state(self, text: str) -> str:
        """Determines the current execution sequence state based on output heuristics."""
        if "Traceback" in text or "Exception" in text:
            return "error"
        if "Runtime disconnected" in text:
            return "runtime_disconnected"
        if "Out of memory" in text:
            return "oom_error"
        # The artifact export cell finishes last - signaling a true completion
        if "EXPORT_DIR" in text and "completed" in text.lower() or "100%" in text:
            # This is heuristic based. A proper implementation would look for a specific success print string
            return "running" 
        return "running"
