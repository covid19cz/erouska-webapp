from starlette.requests import Request
from .database import Database


def get_db(request: Request) -> Database:
    return Database(request.state.db)
