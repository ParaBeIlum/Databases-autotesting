import shutil
import pytest
from models.db_model import *
from definitions import SHIPS_DB_PATH, SHIPS_DB_COPY_PATH


@pytest.fixture(scope='session')
def prepare_db_for_compare():
    shutil.copy(SHIPS_DB_PATH, SHIPS_DB_COPY_PATH)
    randomize_db(database_for_compare)
    yield
    database.close()
    database_for_compare.close()
