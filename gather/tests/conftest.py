import pytest
from tempfile import NamedTemporaryFile


@pytest.fixture
def temp_db_file():
    with NamedTemporaryFile('w', buffering=1) as temp_file:
        yield temp_file


@pytest.fixture
def temp_csv_file():
    with NamedTemporaryFile('w', buffering=1, suffix='.csv') as temp_file:
        yield temp_file


@pytest.fixture
def temp_json_file():
    with NamedTemporaryFile('w', buffering=1, suffix='.json') as temp_file:
        yield temp_file
