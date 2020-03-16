import logging
import pathlib
import sys

import statsd
from pyhocon import ConfigFactory

import os

DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///test.db")
FILE_DIR = pathlib.Path(__file__).absolute().parent.parent

config = ConfigFactory.parse_file(FILE_DIR / "config.conf")
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
statsd = statsd.StatsClient(config.get_string("statsd.host"), 8125,
                            prefix=config.get_string("statsd.prefix"))
