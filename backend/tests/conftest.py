import sys
from pathlib import Path
import pytest

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from fastapi.testclient import TestClient 
from app.main import app

@pytest.fixture
def client():
    #TestClient Simula Peticiones HTTP sin levantar la API
    return TestClient(app)

@pytest.fixture
def sample_docx() -> Path:
    path = BACKEND_ROOT / "tests" / "fixtures" / "sample.docx"
    if not path.exists():
        pytest.skip("Falta crear backend/tests/fixtures/sample.docx")
    return path