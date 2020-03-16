import pathlib

import aiofiles
from fastapi import APIRouter
from starlette.responses import HTMLResponse

from ..config import statsd

router = APIRouter()

SRC_DIR = pathlib.Path(__file__).absolute().parent.parent.parent.parent


@router.get("/", response_class=HTMLResponse)
async def index():
    statsd.incr("main-page-loaded")
    async with aiofiles.open(SRC_DIR / "btwa_frontend" / "public" / "index.html") as file:
        return await file.read()
