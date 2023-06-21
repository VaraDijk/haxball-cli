import asyncio

from browser import Browser
from room import Room

if __name__ == '__main__':
    browser = Browser()
    room = Room("haxball.js", browser)

    asyncio.run(room.create_room())
