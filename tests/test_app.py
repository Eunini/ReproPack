import os
import re
import sys
import zipfile
from pathlib import Path

# Ensure project root (containing main.py) is on sys.path when tests are run
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient  # noqa: E402
from main import app, PACKAGES_DIR  # noqa: E402

client = TestClient(app)


def cleanup_created_packages(ids):
    for pkg_id in ids:
        for f in Path(PACKAGES_DIR).glob(f"*{pkg_id}*.zip"):
            try:
                f.unlink()
            except Exception:
                pass


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "packages_count" in data


def test_create_and_list_and_download_package():
    payload = {
        "project_name": "TestPkg",
        "author": "PyTest",
        "description": "A test package",
        "dependencies": [
            {"name": "requests", "version": "2.31.0"}
        ],
        "environment_variables": {"ENV": "test"},
        "setup_scripts": [
            "echo setting up"
        ],
        "dataset_links": [],
        "instructions": "Run it"
    }
    created_ids = []
    try:
        # Create
        r = client.post("/create-package", json=payload)
        assert r.status_code == 200, r.text
        data = r.json()
        pkg_id = data["package_id"]
        created_ids.append(pkg_id)
        assert data["project_name"] == payload["project_name"]
        zip_path = data["file_path"]
        assert Path(zip_path).exists()

        # List
        r = client.get("/list-packages")
        assert r.status_code == 200
        listing = r.json()
        assert listing["total_count"] >= 1
        assert any(p["package_id"] == pkg_id for p in listing["packages"])

        # Download
        r = client.get(f"/download-package/{pkg_id}")
        assert r.status_code == 200
        assert r.headers.get("content-type") == "application/zip"
        # basic zip validation
        with open("_tmp_download.zip", "wb") as fh:
            fh.write(r.content)
        with zipfile.ZipFile("_tmp_download.zip", "r") as zf:
            names = zf.namelist()
            # expect a metadata file present
            assert any(re.search(r"metadata.*json", n) for n in names)
    finally:
        if Path("_tmp_download.zip").exists():
            Path("_tmp_download.zip").unlink()
        cleanup_created_packages(created_ids)


def test_invalid_package_rejected():
    bad_payload = {
        "project_name": "BadPkg",
        "author": "Tester",
        "dependencies": [
            {"name": "", "version": "1.0"},
            {"name": "valid", "version": ""}
        ]
    }
    r = client.post("/create-package", json=bad_payload)
    # Either 400 from validation we add, or 500 if deeper error (treat as failure)
    assert r.status_code == 400, f"Expected 400, got {r.status_code}: {r.text}"
