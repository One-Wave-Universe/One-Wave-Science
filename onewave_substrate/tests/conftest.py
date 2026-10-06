import pytest

from onewave.storage.sqlite import Storage


@pytest.fixture
def db():
    storage = Storage(":memory:")
    yield storage
    storage.close()
