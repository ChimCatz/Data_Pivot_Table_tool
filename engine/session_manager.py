import json
import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.getcwd()

SESSION_FOLDER = os.path.join(BASE_DIR, "sessions")


def normalize_session_name(name):
    cleaned = " ".join(str(name).split()).strip()
    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        cleaned = cleaned.replace(char, "_")

    return cleaned


def ensure_folder():
    if not os.path.exists(SESSION_FOLDER):
        os.makedirs(SESSION_FOLDER)


def save_session(name, data):

    ensure_folder()
    session_name = normalize_session_name(name)

    path = os.path.join(
        SESSION_FOLDER,
        f"{session_name}.json"
    )

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    return session_name


def load_session(name):

    session_name = normalize_session_name(name)

    path = os.path.join(
        SESSION_FOLDER,
        f"{session_name}.json"
    )

    with open(path, "r") as f:
        return json.load(f)


def list_sessions():

    ensure_folder()

    return sorted([
        f.replace(".json", "")
        for f in os.listdir(SESSION_FOLDER)
        if f.endswith(".json")
    ], key=str.casefold)


def delete_session(name):

    session_name = normalize_session_name(name)

    path = os.path.join(
        SESSION_FOLDER,
        f"{session_name}.json"
    )

    if os.path.exists(path):
        os.remove(path)


def rename_session(old_name, new_name):

    old_session_name = normalize_session_name(old_name)
    new_session_name = normalize_session_name(new_name)

    old_path = os.path.join(
        SESSION_FOLDER,
        f"{old_session_name}.json"
    )

    new_path = os.path.join(
        SESSION_FOLDER,
        f"{new_session_name}.json"
    )

    if os.path.exists(old_path):
        os.rename(old_path, new_path)


def session_exists(name):

    ensure_folder()
    session_name = normalize_session_name(name)

    path = os.path.join(
        SESSION_FOLDER,
        f"{session_name}.json"
    )

    return os.path.exists(path)
