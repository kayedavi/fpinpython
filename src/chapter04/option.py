from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

from common.list import List, Nil, Cons

A = TypeVar('A', covariant=True)
B = TypeVar('B')
C = TypeVar('C')
Nothing = TypeVar('Nothing')


class Option(Generic[A]):
    def map(self, f: Callable[[A], B]) -> Option[A]:
        match self:
            case Nonentity():
                return Nonentity()
            case Some(a):
                return Some(f(a))

    def get_or_else(self, default: Callable[[], A]) -> A:
        match self:
            case Nonentity():
                return default()
            case Some(a):
                return a

    def flat_map(self, f: Callable[[A], Option[B]]) -> Option[B]:
        return self.map(f).get_or_else(Nonentity)

    def or_else(self, ob: Callable[[], Option[A]]) -> Option[A]:
        return self.map(lambda it: Some(it)).get_or_else(ob)

    def filter(self, f: Callable[[A], bool]) -> Option[A]:
        match self:
            case Some(a) if f(a):
                return self
            case _:
                return Nonentity()


@dataclass
class Nonentity(Option[Nothing]):
    pass


@dataclass
class Some(Option[A]):
    get: A


def map2(a: Option[A], b: Option[B], f: Callable[[A, B], C]) -> Option[C]:
    return a.flat_map(lambda aa: b.map(lambda bb: f(aa, bb)))


def sequence(a: List[Option[A]]) -> Option[List[A]]:
    return traverse(a, lambda it: it)


def traverse(a: List[A], f: Callable[[A], Option[B]]) -> Option[List[B]]:
    return a.fold_right(Some(Nil()), (lambda h, t: map2(f(h), t, Cons)))  # type: ignore
