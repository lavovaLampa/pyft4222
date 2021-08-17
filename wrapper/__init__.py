from enum import Enum, auto
from typing import Final, Generic, Literal, NewType, TypeVar, Union
from ctypes import c_void_p

import platform

SYSTEM_TYPE: Final[str] = platform.system()

FtHandle = NewType('FtHandle', c_void_p)


class ResType(Enum):
    OK = auto()
    ERR = auto()


T = TypeVar('T')
E = TypeVar('E')


class Ok(Generic[T]):
    tag: Literal[ResType.OK] = ResType.OK
    result: T

    def __init__(self, result: T):
        self.result = result


class Err(Generic[E]):
    tag: Literal[ResType.ERR] = ResType.ERR
    err: E

    def __init__(self, err: E):
        self.err = err


Result = Union[Ok[T], Err[E]]
