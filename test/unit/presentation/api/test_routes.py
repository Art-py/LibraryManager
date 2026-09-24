from fastapi.testclient import TestClient

from src.main import app


def test_public_routes_are_preserved():
    paths = app.openapi()['paths']

    assert '/api/v1/users/register' in paths
    assert '/api/v1/users/login' in paths
    assert '/api/v1/users/{user_uid}' in paths
    assert '/healthcheck' in paths


def test_healthcheck():
    response = TestClient(app).get('/healthcheck')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}
