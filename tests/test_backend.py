# tests/test_backend.py
import json
import tempfile
import os
import pytest
from app import app as flask_app
import storage

@pytest.fixture(autouse=True)
def isolated_data(tmp_path, monkeypatch):
    # use a temporary JSON file for storage during tests
    tmp_file = tmp_path / "media_store.json"
    tmp_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(storage, "DATA_FILE", tmp_file)
    yield
    # cleanup done by tmp_path

def test_create_and_get_media():
    client = flask_app.test_client()
    payload = {
        "name": "Test Book",
        "publication_date": "2020-01-01",
        "author": "Author A",
        "category": "Book"
    }
    r = client.post("/media", json=payload)
    assert r.status_code == 201
    created = r.get_json()
    assert created["name"] == payload["name"]
    # GET by id
    r2 = client.get(f"/media/{created['id']}")
    assert r2.status_code == 200
    assert r2.get_json()["author"] == "Author A"

def test_list_and_delete_media():
    client = flask_app.test_client()
    # create two items
    for i in range(2):
        client.post("/media", json={
            "name": f"Item {i}",
            "publication_date": "2021-01-01",
            "author": f"Auth{i}",
            "category": "Film" if i == 0 else "Magazine"
        })
    r = client.get("/media")
    assert r.status_code == 200
    items = r.get_json()
    assert len(items) == 2
    # delete first
    first_id = items[0]["id"]
    rdel = client.delete(f"/media/{first_id}")
    assert rdel.status_code == 200
    r_after = client.get("/media")
    assert len(r_after.get_json()) == 1
