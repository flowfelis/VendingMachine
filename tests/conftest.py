import pytest
from sqlalchemy import StaticPool
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base
from app.database import get_db
from app.main import app
from app.security import authenticate


@pytest.fixture(name="db")
def session_fixture():
    SQLALCHEMY_DATABASE_URL = "sqlite://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        yield db


@pytest.fixture(name="client")
def client_fixture(db: Session):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[authenticate] = lambda: None
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
