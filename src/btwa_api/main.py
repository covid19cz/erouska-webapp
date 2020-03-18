import pathlib

import uvicorn
from btwa_api.app.api.endpoints import router as trace_router
from btwa_api.app.api.frontend import router as frontend_router
from btwa_api.app.api.healthcheck import router as healthcheck_router
from btwa_api.app.config import sentry, statsd
from btwa_api.app.db.sql.session import Session
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.requests import Request

FILE_DIR = pathlib.Path(__file__).absolute().parent
SRC_DIR = FILE_DIR.parent
STATIC_PATH = SRC_DIR / "btwa_frontend" / "public" / "res"

app = FastAPI()
app.mount("/res", StaticFiles(directory=STATIC_PATH), name="static")
app.include_router(frontend_router)
app.include_router(trace_router)
app.include_router(healthcheck_router)


@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    path = request.url.path
    safe_path = path.lstrip("/").translate(str.maketrans("./", "-_"))
    if safe_path == "":
        safe_path = "_root_"

    with sentry.configure_scope() as scope:
        scope.set_extra("endpoint", path)

        with statsd.timer(f"endpoints.{safe_path}"):
            response = await call_next(request)

    return response


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


app.add_middleware(SentryAsgiMiddleware)


def webserver(module):
    uvicorn.run(module, host="0.0.0.0", port=5000, log_level="info", reload=True)


def serve():
    webserver("btwa_api.main:app")


if __name__ == "__main__":
    webserver("main:app")
