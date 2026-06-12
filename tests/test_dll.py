"""Hardware-free smoke tests for the bundled dynamic-library loader.

Importing ``pyft4222.wrapper.dll`` runs ``init_libraries()`` at import time,
which loads and hash-verifies the shared libraries for the current platform.
These tests therefore exercise the loader without needing an FT4222 device:

* import succeeds (catches import-time breakage, e.g. the Python 3.9 union
  annotation regression);
* the bundled-binary hashes still match (catches a silent binary/hash drift,
  which would otherwise abort import via ``sys.exit``);
* ``ftlib``/``d2lib`` point at the right libraries (catches the loader
  assigning the D2XX handle to ``ftlib`` and vice versa).

Note: ``ftlib`` and ``d2lib`` are the same object on Linux (the combined
``libft4222`` exports both symbol sets), so the swap check only has teeth on
platforms where the two libraries are distinct (Windows, macOS). Running CI on
those platforms is what makes the swap regression observable.
"""

import platform
from ctypes import CDLL

import pytest

from pyft4222.wrapper import OS_TYPE

try:
    from pyft4222.wrapper import dll
except RuntimeError as exc:  # Unsupported OS/CPU combination.
    pytest.skip(f"unsupported platform: {exc}", allow_module_level=True)


def test_libraries_loaded() -> None:
    assert isinstance(dll.ftlib, CDLL)
    assert isinstance(dll.d2lib, CDLL)


def test_ftlib_exposes_ft4222_symbols() -> None:
    # ``ftlib`` must be LibFT4222; guards against an ftlib/d2lib assignment swap.
    assert hasattr(dll.ftlib, "FT4222_GetVersion")


def test_d2lib_exposes_d2xx_symbols() -> None:
    # ``d2lib`` must be the D2XX library; guards against the same swap.
    assert hasattr(dll.d2lib, "FT_CreateDeviceInfoList")


def test_bundled_library_hashes_match() -> None:
    description = dll._DLL_IMPORT_MAP[(OS_TYPE, platform.machine())]

    bundled = [description.ft4222]
    if isinstance(description.d2xx, dll.BundledDll):
        bundled.append(description.d2xx)

    for lib in bundled:
        assert lib._actual_hash() == lib.hash, f"hash mismatch for {lib.path}"
