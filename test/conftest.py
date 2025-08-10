import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.main import app
from src.repository.repo import repo
from src.database.db_repo import db_repo
from src.database.model import HeroModel


@pytest.fixture(scope="session")
def mock_db():
    mock_object = AsyncMock()
    mock_object.return_value = False
    setattr(db_repo, "check_hero", mock_object)

    mock_object = AsyncMock()
    mock_object.return_value = None
    setattr(db_repo, "save_heroes", mock_object)

    mock_object = AsyncMock()
    mock_object.return_value = [HeroModel(id=1, name="Test Hero")]
    setattr(db_repo, "get_hero", mock_object)

    return db_repo


@pytest.fixture(scope="session")
def mock_external_api():
    mock_object = AsyncMock()
    mock_object.return_value = {"results": [{"id": 1, "name": "Test Hero"}]}
    setattr(repo, "_get_from_external_api", mock_object)


@pytest.fixture(scope="session")
def test_app(mock_db, mock_external_api):
    return TestClient(app)
