from pathlib import Path

PROJECT_NAME = "store_kit"

BASE_DIR = (Path(__file__).parent / ".." / "..").resolve()
PROJECT_DIR = BASE_DIR / PROJECT_NAME
SUPPORTED_LOCALS = (
    "en",
    "no_NB",
)
