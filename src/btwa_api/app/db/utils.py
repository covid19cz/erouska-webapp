from starlette.requests import Request

from .sql.database import Database


def get_db(request: Request) -> Database:
    return Database(request.state.db)
