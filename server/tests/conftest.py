from pathlib import Path
import sys

SERVER_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER_DIR))
sys.path.insert(0, str(SERVER_DIR / "scripts"))

from data_processing import prepare


def pytest_sessionstart(session):
    prepare()

