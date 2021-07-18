from enum import Enum, auto
from typing import Generic, Literal, NewType, TypeVar, Union
from ctypes import c_void_p

FtHandle = NewType('FtHandle', c_void_p)


class ResultTag(Enum):
    OK = auto()
    ERR = auto()


T = TypeVar('T')
E = TypeVar('E')


class Ok(Generic[T]):
    tag: Literal[ResultTag.OK] = ResultTag.OK
    result: T

    def __init__(self, result: T):
        self.result = result


class Err(Generic[E]):
    tag: Literal[ResultTag.ERR] = ResultTag.ERR
    err: E

    def __init__(self, err: E):
        self.err = err


Result = Union[Ok[T], Err[E]]
