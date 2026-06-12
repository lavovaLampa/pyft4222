import hashlib
import importlib.resources as res
import platform
import sys
from ctypes import CDLL, cdll
from dataclasses import dataclass
from typing import Final

from pyft4222.wrapper import OS_TYPE

if sys.version_info >= (3, 11):
    from importlib.resources.abc import Traversable
else:
    from importlib.abc import Traversable

ftlib: CDLL
"""LibFT4222 library."""
d2lib: CDLL
"""D2XX library."""

_COMMON_DLL_PREFIX: str = "pyft4222.wrapper.dll."


class BundledDll:
    """Bundled dynamic library."""

    path: Final[Traversable]
    version: Final[str]
    hash: Final[str]  # sha256

    def __init__(self, path: str, name: str, version: str, hash: str):
        self.path = res.files(_COMMON_DLL_PREFIX + path).joinpath(name)
        self.hash = hash
        self.version = version

    def _actual_hash(self) -> str:
        """Return hash of library as stored on disk."""
        return hashlib.sha256(self.path.read_bytes()).hexdigest()

    def load(self) -> CDLL:
        """Load a bundled shared library.

        Raises:
            OSError -      Issue loading library.
            RuntimeError - Library file hash mismatch.
        """
        actual_hash = self._actual_hash()

        if actual_hash != self.hash:
            raise RuntimeError(
                "Library hash is invalid!"
                f"\n\tExpected: {self.hash}"
                f"\n\tActual: {actual_hash}"
            )

        with res.as_file(self.path) as lib:
            return cdll.LoadLibrary(str(lib))


@dataclass
class SystemDll:
    """System-provided dynamic library."""

    name: str

    def load(self) -> CDLL:
        """Load system shared library.

        Raises:
            OSError - Issue loading library.
        """
        return cdll.LoadLibrary(self.name)


@dataclass
class DllDescription:
    ft4222: BundledDll
    d2xx: "BundledDll | SystemDll | None"


_DLL_IMPORT_MAP: Final[dict[tuple[str, str], DllDescription]] = {
    # Windows
    ("Windows", "AMD64"): DllDescription(
        BundledDll(
            "win.amd64",
            "LibFT4222-64.dll",
            "1.4.8",
            "9b9e381e87b44084e03eb9d22d1c87a5f9edbaaeed897e749031506307c390b5",
        ),
        SystemDll("ftd2xx.dll"),
    ),
    ("Windows", "ARM64"): DllDescription(
        BundledDll(
            "win.arm64",
            "LibFT4222-64.dll",
            "1.4.8",
            "2f00028118263e4cb4fa63ab0a4623e37533d639271780c11bcb2ebb74fcdeac",
        ),
        SystemDll("ftd2xx.dll"),
    ),
    # Linux
    ("Linux", "x86_64"): DllDescription(
        BundledDll(
            "linux.amd64",
            "libft4222.so.1.4.4.232",
            "1.4.4.232",
            "2d4ea24277fe41013a185c46dafe70a4ddeb77853396ce93de43b4f73da67725",
        ),
        None,  # D2xx library part of libft4222 on linux
    ),
    ("Linux", "aarch64"): DllDescription(
        BundledDll(
            "linux.aarch64",
            "libft4222.so.1.4.4.232",
            "1.4.4.232",
            "85663df63f882b715971789bfee77450f182997bd59eab3af87f06c9b53c97d2",
        ),
        None,  # D2xx library part of libft4222 on linux
    ),
    # macOs
    ("Darwin", "x86_64"): DllDescription(
        BundledDll(
            "osx.universal",
            "libft4222.1.4.4.221.dylib",
            "1.4.4.221",
            "11b8066dfc595d5a4e1fb9a63b2870484e49194f675562a343e377f1281f9b52",
        ),
        BundledDll(
            "osx.universal",
            "libftd2xx.dylib",
            "1.4.4.221",
            "e89fbc2b1313072e6b0eaa3d45d7ed6ab7f31970662af1b19b0d1e18e9b7e1f5",
        ),
    ),
    ("Darwin", "arm64"): DllDescription(
        BundledDll(
            "osx.universal",
            "libft4222.1.4.4.221.dylib",
            "1.4.4.221",
            "11b8066dfc595d5a4e1fb9a63b2870484e49194f675562a343e377f1281f9b52",
        ),
        BundledDll(
            "osx.universal",
            "libftd2xx.dylib",
            "1.4.4.221",
            "e89fbc2b1313072e6b0eaa3d45d7ed6ab7f31970662af1b19b0d1e18e9b7e1f5",
        ),
    ),
}

_dll_path = _DLL_IMPORT_MAP.get((OS_TYPE, platform.machine()))


def init_libraries() -> None:
    """Load dynamic libraries based on current OS and CPU architecture.

    Raises:
        OSError -      Issue loading library.
        RuntimeError - Unsupported OS/CPU combination or bundled library hash mismatch.
    """
    global ftlib
    global d2lib

    if _dll_path is None:
        raise RuntimeError("Unsupported OS/CPU combination!")

    if "d2lib" not in globals() or "ftlib" not in globals():
        if _dll_path.d2xx is not None:
            # Load D2XX first so that it's preloaded when libft4222 requires it on macOS
            d2lib = _dll_path.d2xx.load()
            ftlib = _dll_path.ft4222.load()
        else:
            ftlib = _dll_path.ft4222.load()
            d2lib = ftlib


init_libraries()
