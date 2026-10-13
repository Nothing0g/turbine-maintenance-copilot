from fastapi.testclient import TestClient
from turbine_copilot.api import app

client = TestClient(app)

def test_health_contract():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_diagnosis_contract():
    response = client.get('/assets/LP-BRG-02/diagnosis?hours=24')
    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 'review_required'
    assert body['human_review_required'] is True
