# tests/conftest.py
from .fixtures.authenticate_fixture import *  # noqa: F403, F401
from .fixtures.logging_fixture import *  # noqa: F403, F401
from .fixtures.db_fixture import *  # noqa: F403, F401
import os
import time

# タイムゾーンをJST（日本標準時）に設定
os.environ['TZ'] = 'Asia/Tokyo'
time.tzset()
