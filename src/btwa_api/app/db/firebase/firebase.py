import csv
from io import StringIO
from threading import RLock

import firebase_admin
from firebase_admin import firestore, storage
from starlette.requests import Request

from ...config import FIREBASE_STORAGE_BUCKET

MAX_IN_QUERY_LENGTH = 10
ALLOWED_USER_STATUSES = {"unknown", "infected", "cured"}


def get_users_batched(collection, ids):
    users = []
    for start in range(0, len(ids), MAX_IN_QUERY_LENGTH):
        subset = ids[start:start + MAX_IN_QUERY_LENGTH]
        users.extend(d.to_dict() for d in collection.where("buid", "in", subset).get())
    return users


def get_user_proximity(bucket, fuid: str):
    files = sorted(bucket.list_blobs(prefix=f"proximity/{fuid}/",
                                     fields="items(name, timeCreated)",
                                     max_results=100),
                   key=lambda b: b.time_created,
                   reverse=True)
    files = [f for f in files if f.name.endswith(".csv")]
    if not files:
        return None
    most_recent = files[0]
    content = most_recent.download_as_string()
    reader = csv.DictReader(StringIO(content.decode()))
    return sorted(reader, key=lambda record: record["timestampStart"])


class Firebase:
    def __init__(self, bucket: str):
        # bucket takes a very long time to initialize, so it is cached here
        self.bucket = storage.bucket(bucket)
        self.client = firestore.client()
        self.users = self.client.collection("users")

    def get_user_by_phone(self, phone: str):
        for doc in self.users.where("phoneNumber", "==", phone).stream():
            document = doc.to_dict()
            document["fuid"] = doc.id
            return document
        return None

    def get_user_by_fuid(self, fuid: str):
        return self.users.document(fuid).get().to_dict()

    def get_proximity(self, fuid: str):
        proximity = get_user_proximity(self.bucket, fuid)
        if not proximity:
            return None
        buids = list(set(record["buid"] for record in proximity))
        nearby_users = {user["buid"]: user for user in get_users_batched(self.users, buids)}
        for record in proximity:
            record["user"] = nearby_users[record["buid"]]
        return proximity

    def change_user_status(self, fuid: str, status: str):
        assert status in ALLOWED_USER_STATUSES

        doc = self.users.document(fuid)
        if not doc.get().exists:
            return False
        doc.update({
            "status": status
        })
        return True


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
