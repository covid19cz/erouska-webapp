import pathlib

import uvicorn
from btwa_api.app.api.endpoints import router as trace_router
from btwa_api.app.api.frontend import router as frontend_router
from btwa_api.app.api.healthcheck import router as healthcheck_router
from btwa_api.app.db.session import Session
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


# app.add_middleware(HTTPSRedirectMiddleware) TODO


def serve():
    uvicorn.run("btwa_api:app", host="127.0.0.1", port=5000, log_level="info")


if __name__ == "__main__":
    serve()
