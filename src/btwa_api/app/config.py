import logging
import pathlib
import sys
import urllib

import statsd
from pyhocon import ConfigFactory

import os

ROOT_DIR = pathlib.Path(__file__).absolute().parent.parent
DATABASE_URI = os.environ.get("DATABASE_URI", f"sqlite:///{ROOT_DIR / 'test.db'}")

mssql_prefix = "mssql+pyodbc:///?odbc_connect="
if DATABASE_URI.startswith(mssql_prefix):
    DATABASE_URI = f"{mssql_prefix}{urllib.parse.quote_plus(DATABASE_URI[len(mssql_prefix):])}"

config = ConfigFactory.parse_file(ROOT_DIR / "config.conf")
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
statsd = statsd.StatsClient(config.get_string("statsd.host"), 8125,
                            prefix=config.get_string("statsd.prefix"))
