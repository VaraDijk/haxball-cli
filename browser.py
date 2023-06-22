import json
import os

from pyppeteer import launch


class Browser:
    def __init__(self):
        with open("config.json") as f:
            config = json.load(f)

        self._executablePath = config.get('executablePath', '/usr/bin/chromium')
        self._browser = None

    async def __aenter__(self):
        if not os.path.exists(self._executablePath):
            raise ValueError(f"Invalid executable path: {self._executablePath}")

        if not self._browser:
            options = {
                'executablePath': self._executablePath,
                'headless': True,
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu'
                ]
            }

            self._browser = await launch(options)

        return self._browser

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._browser:
            await self._browser.close()
