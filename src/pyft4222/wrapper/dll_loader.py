from __future__ import annotations

import hashlib
import importlib.resources as res
import platform
import sys
from ctypes import CDLL, cdll
from typing import Final

from pyft4222.wrapper import OS_TYPE

try:
    # Python 3.11+
    from importlib.resources.abc import Traversable
except ImportError:
    # Python 3.10 and lower
    from importlib.abc import Traversable

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
        "1.4.8",
        "9b9e381e87b44084e03eb9d22d1c87a5f9edbaaeed897e749031506307c390b5",
    ),
    ("Windows", "ARM64"): DllMeta(
        "win.arm64",
        "LibFT4222-64.dll",
        "1.4.8",
        "2f00028118263e4cb4fa63ab0a4623e37533d639271780c11bcb2ebb74fcdeac"
    ),
    # Linux
    ("Linux", "x86_64"): DllMeta(
        "linux.amd64",
        "libft4222.so.1.4.4.232",
        "1.4.4.232",
        "2d4ea24277fe41013a185c46dafe70a4ddeb77853396ce93de43b4f73da67725",
    ),
    ("Linux", "aarch64"): DllMeta(
        "linux.aarch64",
        "libft4222.so.1.4.4.232",
        "1.4.4.232",
        "85663df63f882b715971789bfee77450f182997bd59eab3af87f06c9b53c97d2",
    ),
    # macOs
    ("Darwin", "x86_64"): DllMeta(
        "osx.universal",
        "libft4222.1.4.4.221.dylib",
        "1.4.4.221",
        "11b8066dfc595d5a4e1fb9a63b2870484e49194f675562a343e377f1281f9b52",
    ),
    ("Darwin", "arm64"): DllMeta(
        "osx.universal",
        "libft4222.1.4.4.221.dylib",
        "1.4.4.221",
        "11b8066dfc595d5a4e1fb9a63b2870484e49194f675562a343e377f1281f9b52",
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

    return None


def init_libraries() -> None:
    global ftlib
    global d2lib

    if "ftlib" not in globals():
        ftlib = _get_ft4222_lib()

    if "d2lib" not in globals():
        temp = _get_d2xx_lib()
        d2lib = temp if temp is not None else ftlib


init_libraries()
