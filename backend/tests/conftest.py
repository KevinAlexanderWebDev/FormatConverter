import sys
from pathlib import Path

import pytest

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from fastapi.testclient import TestClient
from app.converter import convert_file
from app.main import app


@pytest.fixture
def client():
    # TestClient simula peticiones HTTP sin levantar la API
    return TestClient(app)


@pytest.fixture
def sample_docx() -> Path:
    path = BACKEND_ROOT / "tests" / "fixtures" / "sample.docx"
    if not path.exists():
        pytest.skip("Falta crear backend/tests/fixtures/sample.docx")
    return path


@pytest.fixture(scope="session")
def sample_pdf(tmp_path_factory) -> Path:
    docx_path = BACKEND_ROOT / "tests" / "fixtures" / "sample.docx"
    if not docx_path.exists():
        pytest.skip("Falta crear backend/tests/fixtures/sample.docx")
    out_dir = tmp_path_factory.mktemp("pdf")
    return convert_file(docx_path, out_dir, ".docx", "pdf")