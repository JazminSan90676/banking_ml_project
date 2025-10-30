from fastapi.testclient import TestClient
from src.api import main
client = TestClient(main.app)

def test_predict_health():
    payload = {
       "age": 35,
       "job": "technician",
       "marital": "married",
       "education": "secondary",
       "default": "no",
       "balance": 1000.0
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code in (200, 422)
