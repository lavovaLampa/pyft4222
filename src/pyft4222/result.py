from dataclasses import dataclass
from typing import Any, Callable, Generic, NoReturn, Self, TypeAlias, TypeVar, Union

E = TypeVar("E")
R = TypeVar("R")
T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True)
class Ok(Generic[T]):
    val: T

    def map(self, fun: Callable[[T], R]) -> "Ok[R]":
        return Ok(fun(self.val))

    def flat_map(self, fun: Callable[[T], "Result[U, R]"]) -> "Result[U, R]":
        return fun(self.val)

    def unwrap(self, fun: Callable[[U], Exception] = ValueError) -> T:
        return self.val

    __rshift__ = flat_map


@dataclass(frozen=True)
class Err(Generic[T]):
    err: T

    def map(self, _: Callable[[Any], Any]) -> Self:
        return self

    def flat_map(self, _: Callable[[Any], Any]) -> Self:
        return self

    def unwrap(self, fun: Callable[[T], Exception] = ValueError) -> NoReturn:
        """Try to unwrap and return contained value.

        In case of error, raise given exception.

        Args:
            fun:    Function that will receive wrapped error and return an exception

        Return:
            Wrapped value (if any)
        """
        raise fun(self.err)

    __rshift__ = flat_map


Result: TypeAlias = Union[Ok[R], Err[E]]
