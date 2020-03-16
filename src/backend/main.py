import pathlib

import statsd
import uvicorn
from app.config import statsd
from app.db.session import Session
from app.tracing import router as trace_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import HTMLResponse

FILE_DIR = pathlib.Path(__file__).absolute().parent
SRC_DIR = FILE_DIR.parent
STATIC_PATH = SRC_DIR / "btwa_frontend" / "public" / "res"

app = FastAPI()
app.mount("/res", StaticFiles(directory=STATIC_PATH), name="static")
app.include_router(trace_router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


# app.add_middleware(HTTPSRedirectMiddleware) TODO


@app.get("/", response_class=HTMLResponse)
def index():
    statsd.incr("main-page-loaded")
    with open(SRC_DIR / "btwa_frontend" / "public" / "index.html") as f:
        return f.read()


@app.get("/status")
def healthcheck():
    statsd.incr("healthchecked")
    return {"app": "", "healthy": True}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
