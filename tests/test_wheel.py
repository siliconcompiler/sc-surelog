import os
import pytest
import surelog


@pytest.mark.wheel
def test_wheel():
    assert os.path.exists(surelog.get_path() / surelog.get_bin())
