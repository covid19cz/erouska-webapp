import asyncio
import pathlib
import logging

from aiohttp import web


class WebServer:
    def __init__(self, statsd, status_handler, port=8080, loop=None):
        self.logger = logging.getLogger(__name__)

        self.port = port
        self.loop = loop
        self.statd = statsd

        if not loop:
            self.loop = asyncio.get_event_loop()

        self.web_app = web.Application()
        self.router = self.web_app.router

        self.router.add_get("/status", status_handler.handle)
        self.router.add_static("/static", pathlib.Path(__file__).parent / "static")
        self.router.add_get("/", self.get_index)

        self.web_app_handler = None
        self.web_server = None

    async def start(self):
        self.web_app_handler = self.web_app.make_handler()
        self.logger.info("Starting webserver")
        self.web_server = await self.loop.create_server(
            self.web_app_handler, "0.0.0.0", self.port
        )

    async def close(self):
        self.web_server.close()
        await self.web_app.shutdown()
        await self.web_app_handler.shutdown()
        await self.web_app.cleanup()

    async def get_index(self, request):
        self.statd.incr("main-page-loaded")
        return web.FileResponse(pathlib.Path(__file__).parent / "static" / "index.html")


class StatusHandler:
    def __init__(self, app_name, healthy_fn):
        self.app_name = app_name
        self.healthy_fn = healthy_fn

    async def handle(self, _):
        healthy = await self.healthy_fn()

        return web.json_response(
            {"app": self.app_name, "healthy": healthy}, status=200 if healthy else 500
        )
