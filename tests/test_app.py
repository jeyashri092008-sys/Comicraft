from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home_page():
    res = client.get("/")
    assert res.status_code == 200
    assert "Create Your Comic" in res.text
