import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)
