from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_zip():
    response = client.post("/upload", files={"file": ("test.zip", open("test.zip", "rb"))})
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_publications():
    response = client.get("/publications")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_publication_by_id():
    response = client.get("/publications/1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["id"] == 1

def test_invalid_zip_upload():
    response = client.post("/upload", files={"file": ("invalid.txt", open("invalid.txt", "rb"))})
    assert response.status_code == 400
    assert "error" in response.json()