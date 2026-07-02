import pytest
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.db.session import SessionLocal


def test_register_and_login(client):
    response = client.post('/api/auth/register', json={
        'username': 'admin',
        'password': 'secret',
        'role': 'central_admin',
    })
    assert response.status_code == 200
    assert response.json()['username'] == 'admin'

    response = client.post('/api/auth/login', json={'username': 'admin', 'password': 'secret'})
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_invalid_login(client):
    response = client.post('/api/auth/login', json={'username': 'missing', 'password': 'x'})
    assert response.status_code == 401
