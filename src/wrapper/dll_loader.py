from pathlib import Path
from typing import Final, Mapping, Tuple

import platform
import sys

from ctypes import cdll

_MODULE_PATH: Final[Path] = Path(__file__).parent
_DLL_ROOT_DIR: Final[Path] = _MODULE_PATH / "dll"

_MACHINE_TYPE: Final = platform.machine()
OS_TYPE: Final = platform.system()

_DLL_PATH_MAP: Final[Mapping[Tuple[str, str], Path]] = {
    # Windows
    ("Windows", "amd64"): _DLL_ROOT_DIR / "win" / "amd64" / "LibFT4222-64.dll",

    # Linux
    ("Linux", "x86_64"): _DLL_ROOT_DIR / "linux" / "amd64" / "libft4222.so.1.4.4.44",
    ("Linux", "aarch64"): _DLL_ROOT_DIR / "linux" / "aarch64" / "libft4222.so.1.4.44"

    # macOS
    # TODO: Implement!
}

_dll_path = _DLL_PATH_MAP.get((OS_TYPE, _MACHINE_TYPE))
if _dll_path is not None:
    try:
        ftlib = cdll.LoadLibrary(str(_dll_path))
    except OSError as e:
        print("Unable to load shared library!", file=sys.stderr)
        sys.exit(1)
else:
    raise RuntimeError("Unsupported OS/CPU combination!")
