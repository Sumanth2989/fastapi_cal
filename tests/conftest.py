import os
import subprocess
import sys
import time
import pytest
from fastapi.testclient import TestClient

# Integration tests use TestClient fixture
@pytest.fixture(scope="session")
def app_client():
    # Import lazily so test discovery doesn't import app too early
    from app.main import app
    with TestClient(app) as client:
        yield client

# E2E server fixture – runs uvicorn in a subprocess for Playwright
@pytest.fixture(scope="session")
def live_server():
    env = os.environ.copy()
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # wait briefly for server to boot
    time.sleep(1.5)
    yield "http://127.0.0.1:8000"
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
