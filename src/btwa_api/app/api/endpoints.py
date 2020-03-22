from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .utils import get_or_404
from ..db.firebase.firebase import Firebase, get_firebase


router = APIRouter()


class UserLookup(BaseModel):
    phone: str


class User(BaseModel):
    fuid: str
    status: str


@router.post("/get-user", response_model=User)
def get_user(lookup: UserLookup,
             firebase: Firebase = Depends(get_firebase)):
    """Find user by his phone number."""
    user = get_or_404(firebase.get_user_by_phone(lookup.phone))
    return User(fuid=user["fuid"], status=user["status"])


class ProximityRecord(BaseModel):
    buid: str
    start: int
    end: int
    status: str
    phone: str


@router.get("/proximity/{fuid}", response_model=List[ProximityRecord])
def get_proximity(fuid: str,
                  firebase: Firebase = Depends(get_firebase)):
    """Return information about proximity of the given user"""
    records = get_or_404(firebase.get_proximity_records(fuid))
    return [ProximityRecord(
        buid=r["buid"],
        start=r["timestampStart"],
        end=r["timestampEnd"],
        status=r["user"]["status"],
        phone=r["user"]["phoneNumber"]
    ) for r in records]


class UserStatus(BaseModel):
    status: str


@router.post("/change-user-status/{fuid}")
def change_user_status(fuid: str,
                       status: UserStatus,
                       firebase: Firebase = Depends(get_firebase)):
    """Change the infected status of a user"""
    if not firebase.change_user_status(fuid, status.status):
        raise HTTPException(status_code=404)
