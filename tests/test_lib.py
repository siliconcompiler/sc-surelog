import pathlib
import surelog
from unittest.mock import patch


def test_path():
    assert surelog.get_path() == pathlib.Path(surelog.__file__).parent / "bin"


def test_has_system(monkeypatch):
    monkeypatch.setenv("PATH", "")
    assert surelog.has_system_surelog() is False


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

    assert _tools.tools['surelog']["git-commit"] == f"v{surelog.__version__}"
