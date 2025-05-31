from pathlib import Path

import pytest

@pytest.fixture
def test_folder():
    return Path(__file__).parent / "test_files"