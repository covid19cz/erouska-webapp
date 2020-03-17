import bcrypt
import firebase_admin
from fastapi import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError
from starlette import status

from .db.database import Database

security = HTTPBasic()


def check_password(user_password: str, db_password: str):
    return bcrypt.checkpw(user_password.encode(), db_password)


def check_handler_auth(db: Database, credentials: HTTPBasicCredentials):
    db_password = db.get_handler_hashed_password(credentials.username)
    if db_password:
        if check_password(credentials.password, db_password):
            return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def get_firebase_uid(request):
    try:
        decoded_token = auth.verify_id_token(request)
        return decoded_token['uid']
    except InvalidIdTokenError:
        return None
