import json
from collections import namedtuple
from threading import RLock

import firebase_admin
from firebase_admin import firestore, storage
from google.cloud.firestore_v1 import DocumentReference
from starlette.requests import Request

from ..config import FIREBASE_STORAGE_BUCKET


class Firebase:
    def __init__(self, bucket: str):
        # bucket takes a very long time to initialize, so it is cached here
        self.bucket = storage.bucket(bucket)
        self.client = firestore.client()
        self.users = self.client.collection("users")

    def get_user_by_phone(self, phone: str) -> DocumentReference:
        for doc in self.users.where("phone", "==", phone).stream():
            return doc
        return None

    def get_proximity_by_phone(self, phone: str):
        user = self.get_user_by_phone(phone)
        if user is None:
            return None
        filepath = f"proximity/{user.get('uid')}.json"
        blob = self.bucket.get_blob(filepath)
        if blob is not None:
            return json.loads(blob.download_as_string())
        return None

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
