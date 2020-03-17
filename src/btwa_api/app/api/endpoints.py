import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.security import HTTPBasicCredentials
from azure.storage.blob import BlobServiceClient

from ..db.database import Database
from ..db.utils import get_db
from ..security import check_handler_auth, security

router = APIRouter()


@router.get("/register/{guid}")
def register(guid: str,
             credentials: HTTPBasicCredentials = Depends(security),
             db: Database = Depends(get_db)):
    check_handler_auth(db, credentials)
    if db.add_user(guid):
        return True
    else:
        raise HTTPException(status_code=400, detail="GUID already exists")


@router.post("/data")
def data(guid: str,
         file: UploadFile = File(...),
         db: Database = Depends(get_db)):
    user = db.get_user_by_guid(guid)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    directory = guid[0:2]
    blob_file = "./data/" + directory + "/" + guid + ".json"

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_file)
    blob_client.upload_blob(file.file, overwrite=True)

    # TODO: Handle errors

    return True
