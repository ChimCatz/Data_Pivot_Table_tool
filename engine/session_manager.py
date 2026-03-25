import json
import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.getcwd()

SESSION_FOLDER = os.path.join(BASE_DIR, "sessions")


def ensure_folder():
    if not os.path.exists(SESSION_FOLDER):
        os.makedirs(SESSION_FOLDER)


def save_session(name, data):

    ensure_folder()

    path = os.path.join(
        SESSION_FOLDER,
        f"{name}.json"
    )

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_session(name):

    path = os.path.join(
        SESSION_FOLDER,
        f"{name}.json"
    )

    with open(path, "r") as f:
        return json.load(f)


def list_sessions():

    ensure_folder()

    return [
        f.replace(".json", "")
        for f in os.listdir(SESSION_FOLDER)
        if f.endswith(".json")
    ]

def delete_session(name):

    path = os.path.join(
        SESSION_FOLDER,
        f"{name}.json"
    )

    if os.path.exists(path):
        os.remove(path)


def rename_session(old_name, new_name):

    old_path = os.path.join(
        SESSION_FOLDER,
        f"{old_name}.json"
    )

    new_path = os.path.join(
        SESSION_FOLDER,
        f"{new_name}.json"
    )

    if os.path.exists(old_path):
        os.rename(old_path, new_path)