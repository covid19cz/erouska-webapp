import secrets

from fastapi import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

security = HTTPBasic()


def check_basic_auth(credentials: HTTPBasicCredentials):
    username = secrets.compare_digest(credentials.username, "foo")
    password = secrets.compare_digest(credentials.password, "bar")
    if not (username and password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
