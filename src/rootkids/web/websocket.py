from abc import ABC, abstractmethod

import websockets


class WebsocketExploiter(ABC):
    def __init__(self, url: str):
        self.url = url

    async def connect(self):
        async with websockets.connect(self.url) as ws:
            await self.exploit(ws)

    @abstractmethod
    async def exploit(self, ws: websockets.ClientConnection):
        pass
