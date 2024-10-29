import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate("firebase_creds.json")
default_app = firebase_admin.initialize_app(
    cred_obj, {"databaseURL": "https://platform-arena-2-default-rtdb.firebaseio.com/"}
)


def user_exists(user):
    return user in db.reference(f"users").get()


def slot_exists(user, slot):
    return slot in db.reference(f"users/{user}").get()


def get_slot(user, slot):
    if not user_exists(user):
        create_user(user)
    return db.reference(f"users/{user}/{slot}").get()


def create_user(user):
    db.reference(f"users/{user}").set({0: 0, 1: 100000000315194000124019500})


def set_slot(user, slot, value):
    if not user_exists(user):
        create_user(user)
    db.reference(f"users/{user}/{slot}").set(value)
