from . import OS_TYPE

import sys
import platform

from ctypes import CDLL, cdll
from typing import Final, Mapping, Optional, Tuple

if sys.version_info < (3, 9):
    import importlib_resources as res
else:
    import importlib.resources as res


ftlib: CDLL
d2lib: CDLL

_COMMON_DLL_PREFIX: str = "pyft4222.wrapper.dll."

_DLL_IMPORT_MAP: Final[Mapping[Tuple[str, str], Tuple[str, str]]] = {
    # Windows
    ("Windows", "AMD64"): (_COMMON_DLL_PREFIX + "win.amd64", "LibFT4222-64.dll"),
    # Linux
    ("Linux", "x86_64"): (_COMMON_DLL_PREFIX + "linux.amd64", "libft4222.so"),
    ("Linux", "aarch64"): (_COMMON_DLL_PREFIX + "linux.aarch64", "libft4222.so"),
    # macOs
    # TODO: Implement!
}

_dll_path = _DLL_IMPORT_MAP.get((OS_TYPE, platform.machine()))


def _get_ft4222_lib() -> CDLL:
    if _dll_path is not None:
        try:
            path = res.files(_dll_path[0]).joinpath(_dll_path[1])
            with res.as_file(path) as fjel:
                return cdll.LoadLibrary(str(fjel))
        except OSError as e:
            print("Unable to load shared library!", file=sys.stderr)
            print(e)
            sys.exit(1)
    else:
        raise RuntimeError("Unsupported OS/CPU combination!")


def _get_d2xx_lib() -> Optional[CDLL]:
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
        if temp is not None:
            d2lib = temp
        else:
            d2lib = ftlib


init_libraries()
