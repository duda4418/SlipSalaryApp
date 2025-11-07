import uuid
import pytest
from fastapi.testclient import TestClient

from app_factory import create_app
from auth.deps import require_manager
from db import session as db_session


class DummyManager:
    def __init__(self):
        self.id = uuid.uuid4()
        self.is_manager = True
        self.is_active = True
        self.email = "manager@example.com"


class DummyDB:
    """Minimal stand-in for a SQLAlchemy Session used in tests.

    Only implements attributes/methods that could be accidentally
    touched by unmocked code paths. All operations are no-ops.
    """
    def __init__(self):
        self.committed = False

    def add(self, obj):
        return None

    def commit(self):
        self.committed = True

    def rollback(self):
        self.committed = False

    def close(self):
        pass

    # Query-like interface stubs
    def query(self, *args, **kwargs):  # pragma: no cover - safety stub
        class _Q(list):
            def filter(self, *a, **k):
                return self
            def all(self):
                return []
            def first(self):
                return None
        return _Q()

    def get(self, model, ident):
        return None


@pytest.fixture
def app():
    return create_app()


@pytest.fixture(autouse=True)
def override_dependencies(app):
    # Bypass auth/manager requirement
    app.dependency_overrides[require_manager] = lambda: DummyManager()

    # Replace real DB session dependency with dummy session to avoid network connection
    def _dummy_get_db():
        db = DummyDB()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[db_session.get_db] = _dummy_get_db

    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    return TestClient(app)
