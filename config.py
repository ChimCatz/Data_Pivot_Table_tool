from pathlib import Path
import sys


APP_NAME = "Data Pivot Table Tool"
BUILD_VERSION = "Build Version 3"
BUILD_DATE = "May 2026"
CREATOR = "Created by: CZ Catalan"


def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


BASE_DIR = get_base_dir()
ASSETS_DIR = BASE_DIR / "assets"
APP_ICON_PATH = ASSETS_DIR / "data-pivot.ico"
