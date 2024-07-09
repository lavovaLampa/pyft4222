from __future__ import annotations

import importlib.resources as res
import platform
import sys
from collections.abc import Mapping
from ctypes import CDLL, cdll
from typing import Final

from pyft4222.wrapper import OS_TYPE

ftlib: CDLL
d2lib: CDLL

_COMMON_DLL_PREFIX: str = "pyft4222.wrapper.dll."

_DLL_IMPORT_MAP: Final[Mapping[tuple[str, str], tuple[str, str]]] = {
    # Windows
    ("Windows", "AMD64"): (_COMMON_DLL_PREFIX + "win.amd64", "LibFT4222-64.dll"),
    # Linux
    ("Linux", "x86_64"): (_COMMON_DLL_PREFIX + "linux.amd64", "libft4222.so"),
    ("Linux", "aarch64"): (_COMMON_DLL_PREFIX + "linux.aarch64", "libft4222.so"),
    # macOs
    ("Darwin", "x86_64"): (_COMMON_DLL_PREFIX + "osx.amd64", "libft4222.dylib"),
    ("Darwin", "arm64"): (_COMMON_DLL_PREFIX + "osx.arm64", "libft4222.dylib"),
}

_dll_path = _DLL_IMPORT_MAP.get((OS_TYPE, platform.machine()))


def _get_ft4222_lib() -> CDLL:
    if _dll_path is None:
        raise RuntimeError("Unsupported OS/CPU combination!")

    try:
        path = res.files(_dll_path[0]).joinpath(_dll_path[1])
        with res.as_file(path) as f:
            return cdll.LoadLibrary(str(f))
    except OSError as e:
        print("Unable to load shared library!", file=sys.stderr)
        print(e)
        sys.exit(1)


def _get_d2xx_lib() -> CDLL | None:
    if _dll_path is not None:
        if OS_TYPE == "Windows":
            try:
                return cdll.LoadLibrary("ftd2xx.dll")
            except OSError as e:
                print(
                    "Unable to load D2XX shared library (required on Windows)!",
                    file=sys.stderr,
                )
                print(e)
                sys.exit(1)
        else:
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
