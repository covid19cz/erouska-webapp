import csv
from io import StringIO
from threading import RLock

import firebase_admin
from firebase_admin import firestore, storage
from starlette.requests import Request

from ..config import FIREBASE_STORAGE_BUCKET

MAX_IN_QUERY_LENGTH = 10


def get_users_batched(collection, ids):
    users = []
    for start in range(0, len(ids), MAX_IN_QUERY_LENGTH):
        subset = ids[start:start + MAX_IN_QUERY_LENGTH]
        users.extend(d.to_dict() for d in collection.where("buid", "in", subset).get())
    return users


def get_user_proximity(bucket, user):
    uid = user['fuid']
    files = sorted(bucket.list_blobs(prefix=f"proximity/{uid}/",
                                     fields="items(name)",
                                     max_results=100),
                   key=lambda b: b.name,
                   reverse=True)
    files = [f for f in files if f.name.endswith(".csv")]
    if not files:
        return None
    most_recent = files[0]
    content = most_recent.download_as_string()
    reader = csv.DictReader(StringIO(content.decode()))
    return sorted(reader, key=lambda record: record["timestamp"])


class Firebase:
    def __init__(self, bucket: str):
        # bucket takes a very long time to initialize, so it is cached here
        self.bucket = storage.bucket(bucket)
        self.client = firestore.client()
        self.users = self.client.collection("users")

    def get_user_by_phone(self, phone: str):
        for doc in self.users.where("phone", "==", phone).stream():
            return doc.to_dict()
        return None

    def get_proximity_by_phone(self, phone: str):
        user = self.get_user_by_phone(phone)
        if user is None:
            return None
        return get_user_proximity(self.bucket, user)

    def mark_as_infected(self, phone: str):
        user = self.get_user_by_phone(phone)
        if user is None:
            return False
        user.set({
            "infected": True
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
