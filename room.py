import asyncio


class Room:
    def __init__(self, room_path, browser):
        self.room_path = room_path
        self.browser = browser
        self.room_link_event = asyncio.Event()

    async def _init(self, page):
        # Load the required files and initialize the page
        with open(self.room_path) as f:
            room_script = f.read()

        try:
            await page.goto('https://www.haxball.com/headless', waitUntil='networkidle2')
        except Exception as e:
            raise Exception('Error connecting to Haxball headless page. Check your internet connection.') from e

        await page.addScriptTag(content=room_script)

        # Wait for the iframe to update to check if the room was created successfully
        await asyncio.sleep(2)

        element_handle = await page.querySelector('iframe')
        frame = await element_handle.contentFrame()
        recaptcha = await frame.querySelectorEval('#recaptcha', 'e => e.innerHTML')

        if recaptcha:
            raise Exception("The token is invalid or has expired.")

        return await frame.Jeval('#roomlink a', 'el => el.href')

    async def handle_console_message(self, msg, page):
        print(msg.text)
        if "Hello, World!" in msg.text:
            await page.evaluate(f'room.sendChat("Hello from Python!")')

    async def create_room(self):
        async with self.browser as browser:
            page = await browser.newPage()

            page.on('console', lambda msg: asyncio.ensure_future(self.handle_console_message(msg, page)))

            try:
                room_link = await self._init(page)
                print(f'Room created successfully: {room_link}')

                await self.room_link_event.wait()

            except TimeoutError:
                print("The connection to the server has timed out. Please try again later.")
            except ConnectionError:
                print("There was a connection error. Check your internet connection and try again.")
            except ValueError:
                print("The provided value is invalid.")
            except Exception as e:
                print(f'Error creating room: {e}')
            finally:
                await page.close()
