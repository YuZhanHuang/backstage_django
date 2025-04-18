import pytest
from pytest_factoryboy import register

from .factories import UserFactory

register(UserFactory)


@pytest.fixture(scope="function", autouse=True)
def tmp_media(tmpdir, settings):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")
