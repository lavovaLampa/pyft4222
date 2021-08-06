from pathlib import Path
from typing import Final, Mapping, Tuple

import platform
import sys

from ctypes import cdll

MODULE_PATH: Final[Path] = Path(__file__).parent
DLL_ROOT_DIR: Final[Path] = MODULE_PATH / 'dll'

MACHINE_TYPE: Final = platform.machine()
OS_TYPE: Final = platform.system()

DLL_PATH_MAP: Final[Mapping[Tuple[str, str], Path]] = {
    # Windows
    ("Windows", "amd64"): DLL_ROOT_DIR / 'win' / 'amd64' / 'LibFT4222-64.dll',

    # Linux
    ("Linux", "x86_64"): DLL_ROOT_DIR / 'linux' / 'amd64' / 'libft4222.so.1.4.4.44',
    ("Linux", "aarch64"): DLL_ROOT_DIR / 'linux' / 'aarch64' / 'libft4222.so.1.4.44'

    # macOS
    # TODO: Implement!
}

dll_path = DLL_PATH_MAP.get((OS_TYPE, MACHINE_TYPE))
if dll_path is not None:
    try:
        ftlib = cdll.LoadLibrary(str(dll_path))
    except OSError as e:
        print("Unable to load shared library!", file=sys.stderr)
        exit(1)
else:
    raise RuntimeError("Unsupported OS/CPU combination!")
