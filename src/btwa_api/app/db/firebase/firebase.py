import csv
import io
import re
import traceback
import zipfile
from io import StringIO
from threading import RLock
from typing import List

import firebase_admin
from firebase_admin import firestore, storage, auth
from google.cloud.firestore_v1 import CollectionReference
from starlette.requests import Request

from ...config import FIREBASE_STORAGE_BUCKET, logger

MAX_IN_QUERY_LENGTH = 10
ALLOWED_USER_STATUSES = {"unknown", "infected", "cured"}


def get_phones_by_buids(users: CollectionReference,
                        registrations: CollectionReference,
                        buids: List[str]):
    phone_by_buid = {}

    for buid in buids:
        doc = registrations.document(buid).get(["fuid"])
        if not doc.exists:
            continue
        fuid = doc.get("fuid")
        doc = users.document(fuid).get(["phoneNumber"])
        if not doc.exists:
            continue
        phone_by_buid[buid] = doc.get("phoneNumber")

    return phone_by_buid


def get_most_recent_proximity(registrations: CollectionReference, bucket, fuid: str):
    records = {}

    for buid_doc in registrations.where("fuid", "==", fuid).stream():
        buid = buid_doc.id
        files = bucket.list_blobs(prefix=f"proximity/{fuid}/{buid}/", max_results=100)
        files = [f for f in files if f.name.endswith(".csv")]
        for file in files:
            content = file.download_as_string()
            try:
                reader = csv.DictReader(StringIO(content.decode()))
                for record in reader:
                    records[record["timestampStart"]] = record
            except csv.Error:
                logger.warning(f"Error during CSV parsing: {traceback.format_exc()}")
    return sorted(records.values(), key=lambda r: r["timestampStart"])


class Firebase:
    def __init__(self, bucket: str):
        # bucket takes a very long time to initialize, so it is cached here
        self.bucket = storage.bucket(bucket)
        self.client = firestore.client()
        self.users = self.client.collection("users")
        self.registrations = self.client.collection("registrations")

    def get_user_by_phone(self, phone: str):
        user = auth.get_user_by_phone_number(phone)
        if user:
            document = {"fuid": user.uid}
            return document
        else:
            return None

    def get_user_by_fuid(self, fuid: str):
        return self.users.document(fuid).get().to_dict()

    def get_proximity_records(self, fuid: str):
        proximity = get_most_recent_proximity(self.registrations, self.bucket, fuid)
        if not proximity:
            return []
        buids = list(set(record["buid"] for record in proximity if "buid" in record))
        phones_by_buids = get_phones_by_buids(self.users, self.registrations, buids)

        valid_records = []
        for record in proximity:
            buid = record.get("buid")
            if buid and buid in phones_by_buids:
                record["phoneNumber"] = phones_by_buids[buid]
                record["buid"] = buid
                valid_records.append(record)
        return valid_records

    def get_user_data(self, phone):
        user = self.get_user_by_phone(phone)
        if not user:
            return None
        fuid = user["fuid"]
        logger.info(fuid)
        files = self.bucket.list_blobs(prefix=f"proximity/{fuid}/", max_results=100)
        files = [f for f in files if f.name.endswith(".csv")]

        bytes = io.BytesIO()
        with zipfile.ZipFile(bytes, "w", compression=zipfile.ZIP_DEFLATED) as zip:
            for file in files:
                match = CSV_REGEX.match(file.name)
                if not match:
                    continue
                buid = match.group(1)
                timestamp = match.group(2)
                filename = f"{buid}-{timestamp}.csv"
                content = file.download_as_string().decode()
                zip.writestr(filename, content)
        return bytes


CSV_REGEX = re.compile(r"^proximity/.*/(.*)/(\d+)\.csv$")

FIREBASE_INSTANCE = None
FIREBASE_LOCK = RLock()


def get_firebase(request: Request) -> Firebase:
    global FIREBASE_INSTANCE

    # try to initialize Firebase, reads from GOOGLE_APPLICATION_CREDENTIALS
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app()

    if FIREBASE_INSTANCE is None:
        with FIREBASE_LOCK:
            if FIREBASE_INSTANCE is None:
                FIREBASE_INSTANCE = Firebase(FIREBASE_STORAGE_BUCKET)
    return FIREBASE_INSTANCE
