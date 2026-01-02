from abc import ABC, abstractmethod

import httpx


class HttpExploiter(ABC):
    def __init__(
        self, base_url: str, timeout: float = 10.0, headers: dict | None = None
    ):
        self.client = httpx.AsyncClient(
            base_url=base_url, timeout=timeout, headers=headers
        )

    @abstractmethod
    async def exploit(self):
        raise NotImplementedError
