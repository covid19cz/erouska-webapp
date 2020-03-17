import os
import random

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
def data(file: UploadFile = File(...)):
    # TODO: Check if the upload is allowed based on phone number

    # TODO: Check format of the file

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # TODO: generate name based on phone number fetched by check
    directory = random.randrange(0, 9, 1)  # Ideally should be a prefix of phone number
    blob_file = "./data/" + str(directory) + "/" + file.filename

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_file)
    blob_client.upload_blob(file.file, overwrite=True)

    return True
