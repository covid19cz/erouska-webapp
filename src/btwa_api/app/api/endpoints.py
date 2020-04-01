from io import BytesIO
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel

from .utils import get_or_404
from ..db.firebase.firebase import Firebase, get_firebase
from ..db.sql.database import Database
from ..db.utils import get_db
from ..security import check_handler_auth, security

router = APIRouter()


class UserLookup(BaseModel):
    phone: str


class User(BaseModel):
    fuid: str
    status: str


@router.post("/get-user", response_model=User)
def get_user(lookup: UserLookup,
             credentials: HTTPBasicCredentials = Depends(security),
             firebase: Firebase = Depends(get_firebase),
             db: Database = Depends(get_db)):
    """Find user by his phone number."""
    check_handler_auth(db, credentials)
    user = get_or_404(firebase.get_user_by_phone(lookup.phone))
    return User(fuid=user["fuid"], status="unknown")


class ProximityRecord(BaseModel):
    buid: str
    start: int
    end: int
    status: str
    phone: str


@router.get("/proximity/{fuid}", response_model=List[ProximityRecord])
def get_proximity(fuid: str,
                  credentials: HTTPBasicCredentials = Depends(security),
                  firebase: Firebase = Depends(get_firebase),
                  db: Database = Depends(get_db)):
    """Return information about proximity of the given user"""
    check_handler_auth(db, credentials)
    records = get_or_404(firebase.get_proximity_records(fuid))
    return [ProximityRecord(
        buid=r["buid"],
        start=r["timestampStart"],
        end=r["timestampEnd"],
        status="unknown",
        phone=r["phoneNumber"]
    ) for r in records]


@router.get("/get-csv/{phone}")
def get_user(phone: str,
             credentials: HTTPBasicCredentials = Depends(security),
             firebase: Firebase = Depends(get_firebase),
             db: Database = Depends(get_db)):
    """Return CSV data for the given telephone number."""
    check_handler_auth(db, credentials)

    content = get_or_404(firebase.get_user_data(phone))
    buffer = content.getvalue()
    length = len(buffer)
    return StreamingResponse(BytesIO(buffer),
                             media_type="application/zip",
                             headers={
                                 "Content-Disposition": f"attachment;filename={phone}.zip",
                                 "Content-Length": str(length)
                             })
