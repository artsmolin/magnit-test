import os
import sys

import pytest

from magnit_test import storages
from magnit_test.app import get_web_app

# pylint: disable=invalid-name
pytest_plugins = [
    "aiohttp.pytest_plugin",
]


my_path = os.path.dirname(os.path.abspath(__file__))  # pylint: disable=invalid-name
sys.path.insert(0, my_path + "/../")


@pytest.fixture
async def client(aiohttp_client, loop):  # pylint: disable=unused-argument
    client = await aiohttp_client(get_web_app())
    yield client


@pytest.fixture
async def tasks_storage():
    yield storages.tasks_storage
    storages.tasks_storage.flush()
