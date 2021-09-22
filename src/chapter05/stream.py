from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

import chapter03
from TailCall import TailCall, Return, Suspend
from chapter03.List import List, empty_list
from chapter04.option import Option, Nonentity, Some

A = TypeVar('A', covariant=True)
B = TypeVar('B')
C = TypeVar('C')
Nothing = TypeVar('Nothing')


class Stream(Generic[A]):
    def to_list(self) -> List[A]:
        def go(s: Stream[A], acc: List[A]) -> TailCall[List[A]]:
            match s:
                case Cons(h, t):
                    return Suspend(lambda: go(t(), chapter03.List.Cons(h(), acc)))
                case _:
                    return Return(acc)

        return go(self, empty_list()).eval().reverse()

    def take(self, n: int) -> Stream[A]:
        match self:
            case Cons(h, t) if n > 1:
                return Cons(h, lambda: t().take(n - 1))
            case Cons(h, _) if n == 1:
                return Cons(h, Empty)
            case _:
                return Empty()

    def drop(self, n: int) -> Stream[A]:
        match self:
            case Cons(_, t) if n > 0:
                return t().drop(n - 1)
            case _:
                return self

    def take_while(self, f: Callable[[A], bool]) -> Stream[A]:
        match self:
            case Cons(h, t) if f(h()):
                return Cons(h, lambda: t().take_while(f))
            case _:
                return Empty()

    def fold_right(self, z: Callable[[], B], f: Callable[[A, Callable[[], B]], B]) -> B:
        match self:
            case Cons(h, t):
                return f(h(), lambda: t().fold_right(z, f))
            case _:
                return z()

    def map(self, f: Callable[[A], B]) -> Stream[B]:
        return self.fold_right(
            lambda: Empty(),
            (lambda h, t: Cons(lambda: f(h), t))  # type: ignore
        )

    def head_option(self) -> Option[A]:
        match self:
            case Empty():
                return Nonentity()
            case Cons(h, _):
                return Some(h())

    def exists(self, p: Callable[[A], bool]) -> bool:
        return self.fold_right(lambda: False, (lambda a, b: p(a) or b()))

    def for_all(self, f: Callable[[A], bool]) -> bool:
        return self.fold_right(lambda: True, (lambda a, b: f(a) and b()))

    def filter(self, f: Callable[[A], bool]) -> Stream[A]:
        def go(h: A, t: Callable[[], Stream[A]]) -> Stream[A]:
            if f(h):
                return Cons(lambda: h, t)
            else:
                return t()

        return self.fold_right(stream, go)

    def append(self, sa: Callable[[], Stream[A]]) -> Stream[A]:
        return self.fold_right(sa, (lambda h, t: Cons(lambda: h, t)))

    def flat_map(self, f: Callable[[A], Stream[B]]) -> Stream[B]:
        return self.fold_right(stream, (lambda h, t: f(h).append(t)))


@dataclass
class Empty(Stream[Nothing]):
    pass


@dataclass
class Cons(Stream[A]):
    head: Callable[[], A]
    tail: Callable[[], Stream[A]]


def stream(*elements: A) -> Stream[A]:
    if len(elements) == 0:
        return Empty()
    else:
        return Cons(lambda: elements[0], lambda: stream(*elements[1:]))
