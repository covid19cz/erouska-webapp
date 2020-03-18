import logging
import os
import pathlib
import sys
import urllib

import sentry_sdk as sentry
import statsd
from pyhocon import ConfigFactory
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

ROOT_DIR = pathlib.Path(__file__).absolute().parent.parent

# SQL database
DATABASE_URI = os.environ.get("DATABASE_URI", f"sqlite:///{ROOT_DIR / 'test.db'}")

mssql_prefix = "mssql+pyodbc:///?odbc_connect="
if DATABASE_URI.startswith(mssql_prefix):
    DATABASE_URI = f"{mssql_prefix}{urllib.parse.quote_plus(DATABASE_URI[len(mssql_prefix):])}"

# Firebase
FIREBASE_DB_URL = os.environ["FIREBASE_DB_URL"]
FIREBASE_STORAGE_BUCKET = os.environ["FIREBASE_STORAGE_BUCKET"]

# other stuff
config = ConfigFactory.parse_file(ROOT_DIR / "config.conf")

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if config.get_string("sentry.dsn") != "":
    sentry.init(
        config.get_string("sentry.dsn"),
        environment=config.get_string("environment"),
        debug=config.get_bool("sentry.debug"),
        integrations=[SqlalchemyIntegration(), AioHttpIntegration()]
    )

sentry.add_breadcrumb(
    sentry_debug=config.get_bool("sentry.debug"),
    root_dir=ROOT_DIR,
    database_uri=DATABASE_URI,
    statsd='%s:%d/%s' % (
        config.get_string("statsd.host"), 8125, config.get_string("statsd.prefix"))
)

statsd = statsd.StatsClient(config.get_string("statsd.host"), 8125,
                            prefix=config.get_string("statsd.prefix"))
