import inspect
from abc import ABC, abstractmethod
from threading import Thread
from typing import Callable, Literal, cast

import httpx
from flask import Flask
from flask.typing import ResponseReturnValue
from pyngrok import ngrok as ng


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


class HTTPCallbackExploiter(ABC):
    host: str = "localhost"
    port: int = 5000
    callback_url: str

    @staticmethod
    def route(path: str, methods: list[str] | None = None):
        if methods is None:
            methods = ["GET"]

        def decorator(func: Callable):
            setattr(
                func,
                "__http_route__",
                {
                    "path": path,
                    "methods": methods,
                },
            )
            return func

        return decorator

    def __init__(
        self, base_url: str, timeout: float = 10.0, headers: dict | None = None
    ):
        self.client = httpx.AsyncClient(
            base_url=base_url, timeout=timeout, headers=headers
        )
        self.app = Flask(self.__class__.__name__)
        self._register_routes()

    def _register_routes(self):
        for _, method in inspect.getmembers(self, predicate=callable):
            route_info = getattr(method, "__http_route__", None)
            if not route_info:
                continue

            view_func = cast(Callable[..., ResponseReturnValue], method)

            self.app.add_url_rule(
                route_info["path"],
                endpoint=method.__name__,
                view_func=view_func,
                methods=route_info["methods"],
            )

    @abstractmethod
    async def exploit(self):
        raise NotImplementedError

    async def run(
        self,
        *,
        host: str = host,
        port: int = port,
        daemon: bool = True,
        ngrok: Literal["http", "tcp"] | None = None,
    ):
        if ngrok:
            self.callback_url = ng.connect(port, ngrok).public_url
            if ngrok == "tcp":
                self.callback_url = self.callback_url.replace("tcp://", "http://")
        else:
            self.callback_url = f"http://{host}:{port}"

        print(f"[+] CALLBACK URL: {self.callback_url}")

        server = Thread(
            target=self.app.run,
            kwargs={
                "host": host,
                "port": port,
                "use_reloader": False,
                "threaded": True,
            },
            daemon=daemon,
        )
        server.start()

        await self.exploit()
