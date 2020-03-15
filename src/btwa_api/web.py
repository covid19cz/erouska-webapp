import asyncio
import pathlib
import logging

from aiohttp import web


class WebServer:
    def __init__(self, statsd, status_handler, trace_handler, port=8080, loop=None):
        self.logger = logging.getLogger(__name__)

        self.port = port
        self.loop = loop
        self.statsd = statsd

        if not loop:
            self.loop = asyncio.get_event_loop()

        self.web_app = web.Application()
        self.router = self.web_app.router

        self.router.add_get("/status", status_handler.handle)
        self.logger.info(pathlib.Path(__file__))
        self.router.add_static("/res", pathlib.Path(__file__).parent.parent / "btwa_frontend" / "public" / "res")
        self.router.add_get("/", self.get_index)
        self.router.add_post("/trace", trace_handler.handle)

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
        self.statsd.incr("main-page-loaded")
        return web.FileResponse(pathlib.Path(__file__).parent.parent / "btwa_frontend" / "public" / "index.html")


class StatusHandler:
    def __init__(self, app_name, healthy_fn):
        self.app_name = app_name
        self.healthy_fn = healthy_fn

    async def handle(self, _):
        healthy = await self.healthy_fn()

        return web.json_response(
            {"app": self.app_name, "healthy": healthy}, status=200 if healthy else 500
        )


class TraceHandler:
    def __init__(self, statsd):
        self.statsd = statsd

    async def handle(self, _):
        return web.json_response(  # TODO
            {
                "231764D9-7FD2-BB6B-5F5D-B6F20E6F8F83": "2XX XXX XXX",
                "0A8B054C-D11F-B06C8EFB-D99701FB3443": "0XX XXX XXX",
                "A3AE7F23-0F34-A0D5-CF4D-41D0F39526AC": "AXX XXX XXX",
                "0E09F5EF-6439-42AE-F59A-C6CD2731DB5F": "0XX XXX XXX",
                "2AFB2F04-0404-9508-02B4-1D86A1E9519A": "2XX XXX XXX",
                "B3DDB275-E497-4FFF-F7F5-425A27E5BAE3": "BXX XXX XXX",
                "998E892C-151F-FCCD-D0F4-FD7E8D12C9E0": "9XX XXX XXX",
                "998E89C2-151F-FCCD-D0F4-FD7E8D12C9E0": "9XX XXX XXX",
                "65A708D6-1A05-AE0A-6A48-53ECFB6E81E9": "6XX XXX XXX",
                "CD0F37D9-735D-60FC-2C09-A80A48BF11E3": "CXX XXX XXX",
                "58B315DE-8465-5FA8-A77B-F894F5A81FDC": "5XX XXX XXX",
                "23209EC7-E57A-C64A-902F-161961EF3A0F": "2XX XXX XXX",
                "56529EC7-E57A-C64A-902F-161961EF3A0F": "5XX XXX XXX",
                "231764D9-7FD2-BB6B-5F5D-B6F20E6F8F83": "2XX XXX XXX",
                "2B9FFE76-BB57-0DAB-50BE-DFBEEC964033": "2XX XXX XXX",
                "5ED98494-006D-185F-9433-2445FD72FE70": "5XX XXX XXX",
                "F13D1BE7-3335-79BA-BE99-0C54111691C2": "FXX XXX XXX",
                "CE8A34AE-FD21-B671-59F9-0618406B6044": "CXX XXX XXX",
                "BC417990-D813-D785-1203-8DC79A82E26B": "BXX XXX XXX"
            }, status=200
        )
