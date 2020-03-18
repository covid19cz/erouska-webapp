import contextlib
import time

from .config import logger


@contextlib.contextmanager
def measure(name):
    start = time.time()
    yield
    duration = time.time() - start
    logger.info(f"{name}: {duration} s")
