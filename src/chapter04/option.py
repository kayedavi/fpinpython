from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Any

from common.list import List, Nil, Cons, empty_list

A = TypeVar('A', covariant=True)
B = TypeVar('B')
C = TypeVar('C')


class Option(Generic[A]):
    def map(self, f: Callable[[A], B]) -> Option[A]:
        match self:
            case Nothing():
                return Nothing()
            case Some(a):
                return Some(f(a))

    def getOrElse(self, default: Callable[[], A]) -> A:
        match self:
            case Nothing():
                return default()
            case Some(a):
                return a

    def flatMap(self, f: Callable[[A], Option[B]]) -> Option[B]:
        return self.map(f).getOrElse(Nothing)

    # Of course, we can also implement `flatMap` with explicit pattern matching.
    def flatMap_1(self, f: Callable[[A], Option[B]]) -> Option[B]:
        match self:
            case Nothing():
                return Nothing()
            case Some(a):
                return f(a)

    def orElse(self, ob: Callable[[], Option[A]]) -> Option[A]:
        return self.map(lambda it: Some(it)).getOrElse(ob)

    # Again, we can implement this with explicit pattern matching.
    def orElse_1(self, ob: Callable[[], Option[B]]) -> Option[B]:
        match self:
            case Nothing():
                return ob()
            case _:
                return self

    def filter(self, f: Callable[[A], bool]) -> Option[A]:
        match self:
            case Some(a) if f(a):
                return self
            case _:
                return Nothing()

    # This can also be defined in terms of `flatMap`.
    def filter_1(self, f: Callable[[A], bool]) -> Option[A]:
        return self.flatMap(lambda a: Some(a) if f(a) else Nothing())


@dataclass
class Nothing(Option[A]):
    pass


@dataclass
class Some(Option[A]):
    get: A


def some(a: A) -> Option[A]:
    return Some(a)


def failingFn(i: int) -> int:
    # y: int = ...` declares `y` as having type `int`, and sets it equal to the right hand side of the `=`.
    y: int = throw(Exception('fail!'))
    try:
        x = 42 + 5
        return x + y
    # A `catch` block is just a pattern matching block like the ones we've seen. `case e: Exception` is a pattern
    # that matches any `Exception`, and it binds this value to the identifier `e`. The match returns the value 43.
    except Exception as e:
        return 42


def failingFn2(i: int) -> int:
    try:
        x = 42 + 5
        # A thrown Exception can be given any type; here we're annotating it with the type `int`
        return x + throw(Exception("fail!"))
    except Exception as e:
        return 43


def throw(exception: Exception) -> Any:
    raise exception


def mean(xs: List[float]) -> Option[float]:
    return Some(xs.sum() / xs.length()) if xs else Nothing()


def variance(xs: List[float]) -> Option[float]:
    return mean(xs).flatMap(lambda m: mean(xs.map(lambda x: math.pow(x - m, 2))))


# a bit later in the chapter we'll learn nicer syntax for
# writing functions like this
def map2(a: Option[A], b: Option[B], f: Callable[[A, B], C]) -> Option[C]:
    return a.flatMap(lambda aa: b.map(lambda bb: f(aa, bb)))


# Here's an explicit recursive version:
def sequence(a: List[Option[A]]) -> Option[List[A]]:
    match a:
        case Nil():
            return Some(Nil())
        case Cons(h, t):
            return h.flatMap(lambda hh: sequence(t).map(lambda tt: Cons(hh, tt)))


# It can also be implemented using `foldRight` and `map2`. The type annotation on `foldRight` is needed here; otherwise
# Scala wrongly infers the result type of the fold as `Some[Nil.type]` and reports a type error (try it!). This is an
# unfortunate consequence of Scala using subtyping to encode algebraic data types.
# a.foldRight[Option[List[A]]](Some(Nil))((x,y) => map2(x,y)(_ :: _))
def sequence_1(a: List[Option[A]]) -> Option[List[A]]:
    return a.fold_right(some(empty_list()), (lambda x, y: map2(x, y, (lambda hh, tt: Cons(hh, tt)))))


def traverse(a: List[A], f: Callable[[A], Option[B]]) -> Option[List[B]]:
    return a.fold_right(some(empty_list()), (lambda h, t: map2(f(h), t, Cons)))


def traverse_1(a: List[A], f: Callable[[A], Option[B]]) -> Option[List[B]]:
    return a.fold_right(some(empty_list()), (lambda h, t: map2(f(h), t, Cons)))


def sequenceViaTraverse(a: List[Option[A]]) -> Option[List[A]]:
    return traverse(a, lambda a: a)
