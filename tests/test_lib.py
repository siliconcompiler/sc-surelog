import pathlib
import surelog
from unittest.mock import patch
import pytest


def test_path():
    assert surelog.get_path() == pathlib.Path(surelog.__file__).parent / "bin"


def test_has_system(monkeypatch):
    monkeypatch.setenv("PATH", "")
    assert surelog.has_system_surelog() is False


@pytest.mark.parametrize("platform,ext", [
    ("linux", ""),
    ("darwin", ""),
    ("macos", ""),
    ("win32", ".exe"),
])
def test_get_bin(platform, ext):
    assert surelog.get_bin(platform) == f'surelog{ext}'


@patch('sys.platform', 'linux')
def test_get_bin_linux():
    assert surelog.get_bin() == 'surelog'


@patch('sys.platform', 'darwin')
def test_get_bin_macos():
    assert surelog.get_bin() == 'surelog'


@patch('sys.platform', 'win32')
def test_get_bin_windows():
    assert surelog.get_bin() == 'surelog.exe'


def test_version(monkeypatch):
    import _tools

    assert f"v{surelog.__version__}".startswith(_tools.tools['surelog']["git-commit"])
