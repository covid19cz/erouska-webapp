from app.db.database import Database
from app.db.utils import get_db
from app.security import check_basic_auth, security
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials

router = APIRouter()


@router.get("/register/{guid}")
def register(guid: str,
             credentials: HTTPBasicCredentials = Depends(security),
             db: Database = Depends(get_db)):
    check_basic_auth(credentials)
    if db.add_user(guid):
        return True
    else:
        raise HTTPException(status_code=400, detail="GUID already exists")
