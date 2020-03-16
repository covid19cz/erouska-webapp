from os.path import join, dirname, realpath
import logging
import asyncio
import argparse
import statsd
import sys
from concurrent.futures import ThreadPoolExecutor
from .web import StatusHandler, WebServer, TraceHandler
from pyhocon import ConfigFactory


class App:
    def __init__(self, loop):
        self.loop = loop

        self.config = ConfigFactory.parse_file(join(dirname(realpath(__file__)), "config.conf"))

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        self.statsd = statsd.StatsClient(self.config.get_string("statsd.host"), 8125, prefix=self.config.get_string("statsd.prefix"))

    async def setup(self, port):
        # webserver
        status_handler = StatusHandler(self.config.get_string("app_name"), self.healthcheck)
        trace_handler = TraceHandler(self.statsd)

        self.web_server = WebServer(
            self.statsd, status_handler, trace_handler, loop=self.loop, port=port
        )

    async def healthcheck(self):
        self.logger.debug("Healthcheck called")
        self.statsd.incr("healthchecked")
        return True  # TODO

    async def run(self):
        await self.web_server.start()

    async def close(self):
        await self.web_server.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', help="Webserver port (defaults to 8080)", default=8080, required=False)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=10))

    app = App(loop)
    loop.run_until_complete(app.setup(args.port))

    try:
        loop.run_until_complete(app.run())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(app.close())


if __name__ == "__main__":
    main()
