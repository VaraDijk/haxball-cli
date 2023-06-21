import json
from pyppeteer import launch


class Browser:
    def __init__(self):
        with open("config.json") as f:
            config = json.load(f)

        self._executablePath = config.get('executablePath', '/usr/bin/chromium')
        self._browser = None

    async def get_browser(self):
        if not self._browser:
            self._browser = await launch(
                executablePath=self._executablePath,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', "--no-first-run",
                      '--no-zygote', '--single-process', '--disable-accelerated-2d-canvas', '--disable-gpu']
            )

        return self._browser

    async def close_browser(self):
        if self._browser:
            await self._browser.close()
