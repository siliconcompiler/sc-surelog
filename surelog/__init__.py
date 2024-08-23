import pathlib
import shutil
import sys


__version__ = "1.84"


def has_system_surelog():
    return shutil.which(get_bin()) is not None


def get_path():
    return pathlib.Path(__file__).parent / "bin"


def get_bin():
    exe = "surelog"
    if sys.platform.startswith("win32"):
        exe = f"{exe}.exe"

    return exe
