import pathlib

import aiofiles
from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()

SRC_DIR = pathlib.Path(__file__).absolute().parent.parent.parent.parent


@router.get("/", response_class=HTMLResponse)
async def index():
    async with aiofiles.open(SRC_DIR / "btwa_frontend" / "public" / "index.html") as file:
        return await file.read()
