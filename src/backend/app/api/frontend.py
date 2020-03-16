import pathlib

from app.config import statsd
from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()

SRC_DIR = pathlib.Path(__file__).absolute().parent.parent.parent.parent


@router.get("/", response_class=HTMLResponse)
def index():
    statsd.incr("main-page-loaded")
    with open(SRC_DIR / "btwa_frontend" / "public" / "index.html") as f:
        return f.read()
