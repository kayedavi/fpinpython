from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

from TailCall import TailCall, Return, Suspend

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
Nothing = TypeVar('Nothing')


class List(Generic[A]):

    def append(self, r: List[A]) -> List[A]:
        return self.fold_right(r, (lambda h, t: Cons(h, t)))

    def fold_right(self, z: B, f: Callable[[A, B], B]) -> B:
        return self.fold(lambda b: b, (lambda g, a: lambda b: g(f(a, b))))(z)

    def tail(self) -> List[A]:
        match self:
            case Nil():
                raise Exception("tail of empty list")
            case Cons(_, xs):
                return xs

    def head(self) -> A:
        match self:
            case Nil():
                raise Exception("head of empty list")
            case Cons(x, _):
                return x

    def set_head(self, h: A) -> List[A]:
        match self:
            case Nil():
                raise Exception("set_head on empty list")
            case Cons(_, t):
                return Cons(h, t)

    def drop(self, n: int) -> List[A]:
        def go(xs: List[A], p: int) -> TailCall[List[A]]:
            if p <= 0:
                return Return(xs)
            else:
                match xs:
                    case Nil():
                        return Return(xs)
                    case Cons(_, t):
                        return Suspend(lambda: go(t, p - 1))

        return go(self, n).eval()

    def drop_while(self, f: Callable[[A], bool]) -> List[A]:
        match self:
            case Cons(h, t) if f(h):
                return t.drop_while(f)
            case _:
                return self

    def init(self) -> List[A]:
        match self:
            case Nil():
                raise Exception('init of empty list')
            case Cons(_, Nil()):
                return Nil()
            case Cons(h, t):
                return Cons(h, t.init())

    def length(self) -> int:
        return self.fold(0, (lambda acc, h: acc + 1))

    def fold(self, z: B, f: Callable[[B, A], B]) -> B:
        def go(xs: List[A], b: B, g: Callable[[B, A], B]) -> TailCall[B]:
            match xs:
                case Nil():
                    return Return(b)
                case Cons(h, t):
                    return Suspend(lambda: go(t, g(b, h), g))

        return go(self, z, f).eval()

    def reverse(self) -> List[A]:
        return self.fold(empty_list(), (lambda acc, h: Cons(h, acc)))

    @staticmethod
    def concat(xs: List[List[A]]) -> List[A]:
        return xs.fold_right(empty_list(), List.append)

    def map(self, f: Callable[[A], B]) -> List[B]:
        return self.fold_right(empty_list(), (lambda h, t: Cons(f(h), t)))

    def filter(self, f: Callable[[A], bool]) -> List[A]:
        def go(h: A, t: List[A]) -> List[A]:
            if f(h):
                return Cons(h, t)
            else:
                return t

        return self.fold_right(empty_list(), go)

    def flat_map(self, f: Callable[[A], List[B]]) -> List[B]:
        return List.concat(self.map(f))

    def zip_with(self, b: List[B], f: Callable[[A, B], C]) -> List[C]:
        match (self, b):
            case (Nil(), _):
                return Nil()
            case (_, Nil()):
                return Nil()
            case (Cons(h1, t1), Cons(h2, t2)):
                return Cons(f(h1, h2), t1.zip_with(t2, f))

    def starts_with(self, prefix: List[A]) -> bool:
        def go(xs: List[A], pre: List[A]) -> TailCall[bool]:
            match (xs, pre):
                case (_, Nil()):
                    return Return(True)
                case (Cons(h, t), Cons(h2, t2)) if h == h2:
                    return Suspend(lambda: go(t, t2))
                case _:
                    return Return(False)

        return go(self, prefix).eval()

    def has_subsequence(self, subsequence: List[A]) -> bool:
        def go(sup: List[A], sub: List[A]) -> TailCall[bool]:
            match sup:
                case Nil():
                    return Return(sub == Nil)
                case _ if sup.starts_with(sub):
                    return Return(True)
                case Cons(_, t):
                    return Suspend(lambda: go(t, sub))

        return go(self, subsequence).eval()

    def group_by(self, key_selector: Callable[[A], B]) -> dict[B, List[A]]:
        xs: list[A] = self.to_python()
        xs.reverse()
        dictionary: dict[A, List[A]] = {}
        for x in xs:
            key = key_selector(x)
            list_in_dict = dictionary.get(key)
            if list_in_dict:
                dictionary[key] = Cons(x, list_in_dict)
            else:
                dictionary[key] = Cons(x, Nil())

        return dictionary

    def __str__(self) -> str:
        if isinstance(self, Nil):
            return '[]'
        else:
            first = f'[{self.head()}'
            remaining = self.tail().fold('', (lambda b, a: f"{b}, {str(a)}"))

            return first + remaining + ']'

    def to_python(self) -> list[A]:
        def go(b: list[A], a: A) -> list[A]:
            b.append(a)
            return b

        return self.fold(list(), go)


def list_of(*elements: A) -> List[A]:
    if len(elements) == 0:
        return Nil()
    else:
        return Cons(elements[0], list_of(*elements[1:]))


def empty_list() -> List[Nothing]:
    return Nil()


@dataclass(frozen=True)
class Nil(List[Nothing]):
    pass


@dataclass(frozen=True)
class Cons(List[A]):
    _head: A
    _tail: List[A]


def curry(f: Callable[[A, B], C]) -> Callable[[A], Callable[[B], C]]:
    return lambda a: lambda b: f(a, b)
