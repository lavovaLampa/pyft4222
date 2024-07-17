from __future__ import annotations

import hashlib
import importlib.resources as res
import platform
import sys
from ctypes import CDLL, cdll
from importlib.abc import Traversable
from typing import Final

from pyft4222.wrapper import OS_TYPE

ftlib: CDLL
d2lib: CDLL

_COMMON_DLL_PREFIX: str = "pyft4222.wrapper.dll."


class DllMeta:
    path: Traversable
    version: str
    hash: str  # sha256

    def __init__(self, path: str, name: str, version: str, hash: str):
        self.path = res.files(_COMMON_DLL_PREFIX + path)
        self.path = self.path.joinpath(name)
        self.path = res.files(_COMMON_DLL_PREFIX + path).joinpath(name)
        self.hash = hash
        self.version = version

    def load(self) -> CDLL:
        actual_hash = self.actual_hash()

        if actual_hash != self.hash:
            print(
                "Library hash is invalid!"
                f"\n\tExpected: {self.hash}"
                f"\n\tActual: {actual_hash}",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            with res.as_file(self.path) as lib:
                return cdll.LoadLibrary(str(lib))
        except OSError as e:
            print("Unable to load shared library!", file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)

    def actual_hash(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()


_DLL_IMPORT_MAP: Final[dict[tuple[str, str], DllMeta]] = {
    # Windows
    ("Windows", "AMD64"): DllMeta(
        "win.amd64",
        "LibFT4222-64.dll",
        "1.4.6.1",
        "23dcb848297ec160d04bec1024f6d842b0fc6c75189a914ebe0df7b1c33e34d1",
    ),
    # Linux
    ("Linux", "x86_64"): DllMeta(
        "linux.amd64",
        "libft4222.so.1.4.4.188",
        "1.4.4.188",
        "2a90bb6c880b119191582d21f3e527940c604cc0af6dbf117178f9689633405e",
    ),
    ("Linux", "aarch64"): DllMeta(
        "linux.aarch64",
        "libft4222.so.1.4.4.188",
        "1.4.4.188",
        "1d1990880ab769ef5dba378e1887897576a6062b8c86e098681fe422a0bf5b4f",
    ),
    # macOs
    ("Darwin", "x86_64"): DllMeta(
        "osx.universal",
        "libft4222.1.4.4.190.dylib",
        "1.4.4.190",
        "31d0310eda14f9006725104d3bf0733e07c7e33643bec38c2812160f6ba2da54",
    ),
    ("Darwin", "arm64"): DllMeta(
        "osx.universal",
        "libft4222.1.4.4.190.dylib",
        "1.4.4.190",
        "31d0310eda14f9006725104d3bf0733e07c7e33643bec38c2812160f6ba2da54",
    ),
}

_dll_path = _DLL_IMPORT_MAP.get((OS_TYPE, platform.machine()))


def _get_ft4222_lib() -> CDLL:
    if _dll_path is None:
        raise RuntimeError("Unsupported OS/CPU combination!")

    return _dll_path.load()


def _get_d2xx_lib() -> CDLL | None:
    if _dll_path is not None and OS_TYPE == "Windows":
        try:
            return cdll.LoadLibrary("ftd2xx.dll")
        except OSError as e:
            print(
                "Unable to load D2XX shared library (required on Windows)!",
                file=sys.stderr,
            )
            print(e)
            sys.exit(1)


def init_libraries() -> None:
    global ftlib
    global d2lib

    if "ftlib" not in globals():
        ftlib = _get_ft4222_lib()

    if "d2lib" not in globals():
        temp = _get_d2xx_lib()
        d2lib = temp if temp is not None else ftlib


init_libraries()
