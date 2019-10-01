import pathlib
import shutil
import uuid

import pytest

TEST_DIR_PATH = pathlib.Path('/', 'tmp', 'flake8_pylint_comparison_test')


@pytest.fixture(scope='session', autouse=True)
def test_dir():
    if TEST_DIR_PATH.is_dir():
        # If there is such directory for some reason (badly finished tests, for example) - remove it
        shutil.rmtree(str(TEST_DIR_PATH))
    TEST_DIR_PATH.mkdir()
    yield
    shutil.rmtree(str(TEST_DIR_PATH))


@pytest.fixture(scope='function')
def file_to_lint():
    file_name = 'tmp_{0}.py'.format(str(uuid.uuid4()).replace('-', ''))
    path = TEST_DIR_PATH.joinpath(file_name)
    yield path
    path.unlink()
