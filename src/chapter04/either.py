from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

E = TypeVar('E')
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
Nothing = TypeVar('Nothing')


class Either(Generic[E, A]):
    def map(self, f: Callable[[A], B]) -> Either[E, B]:
        match self:
            case Right(a):
                return Right(f(a))
            case Left(e):
                return Left(e)

    def flat_map(self, f: Callable[[A], Either[E, B]]) -> Either[E, B]:
        match self:
            case Left(e):
                return Left(e)
            case Right(a):
                return f(a)

    def or_else(self, b: Callable[[], Either[E, A]]) -> Either[E, A]:
        match self:
            case Left(_):
                return b()
            case Right(a):
                return Right(a)

    def map2(self, b: Either[E, B], f: Callable[[A, B], C]) -> Either[E, C]:
        return self.flat_map(lambda a: b.map(lambda b1: f(a, b1)))


def Try(a: Callable[[], A]) -> Either[Exception, A]:
    try:
        return Right(a())
    except Exception as e:
        return Left(e)


@dataclass
class Left(Either[E, Nothing]):
    get: E


@dataclass
class Right(Either[Nothing, A]):
    get: A
