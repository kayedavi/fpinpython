from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


class Tree(Generic[A]):  # `List` data type, parameterized on a type, `A`
    pass


@dataclass(frozen=True)
class Leaf(Tree[A]):  # A `List` data constructor representing the empty list
    value: A


@dataclass(frozen=True)
class Branch(Tree[A]):
    left: Tree[A]
    right: Tree[A]


def size(t: Tree[A]) -> int:
    match t:
        case Leaf(_):
            return 1
        case Branch(l, r):
            return 1 + size(l) + size(r)


# We're using the method `max` that exists on all `Int` values rather than an explicit `if` expression.
#
# Note how similar the implementation is to `size`. We'll abstract out the common pattern in a later exercise.
def maximum(t: Tree[int]) -> int:
    match t:
        case Leaf(n):
            return n
        case Branch(l, r):
            return max(maximum(l), maximum(r))


# Again, note how similar the implementation is to `size` and `maximum`.
def depth(t: Tree[A]) -> int:
    match t:
        case Leaf(_):
            return 0
        case Branch(l, r):
            return 1 + max(depth(l), depth(r))


def map(t: Tree[A], f: Callable[[A], B]) -> Tree[B]:
    match t:
        case Leaf(a):
            return Leaf(f(a))
        case Branch(l, r):
            return Branch(map(l, f), map(r, f))


# Like `foldRight` for lists, `fold` receives a "handler" for each of the data constructors of the type, and recursively
# accumulates some value using these handlers. As with `foldRight`, `fold(t)(Leaf(_))(Branch(_,_)) == t`, and we can use
# this function to implement just about any recursive function that would otherwise be defined by pattern matching.
def fold(t: Tree[A], f: Callable[[A], B], g: Callable[[B, B], B]) -> B:
    match t:
        case Leaf(a):
            return f(a)
        case Branch(l, r):
            return g(fold(l, f, g), fold(r, f, g))


def sizeViaFold(t: Tree[A]) -> int:
    return fold(t, lambda _: 1, lambda x, y: 1 + x + y)


def maximumViaFold(t: Tree[int]) -> int:
    return fold(t, lambda a: a, (lambda x, y: max(x, y)))


def depthViaFold(t: Tree[A]) -> int:
    return fold(t, lambda _: 0, (lambda d1, d2: 1 + max(d1, d2)))


# Note the type annotation required on the expression `Leaf(f(a))`. Without this annotation, we get an error like this:
#
# type mismatch;
#   found   : fpinscala.datastructures.Branch[B]
#   required: fpinscala.datastructures.Leaf[B]
#      fold(t)(a => Leaf(f(a)))(Branch(_,_))
#                                     ^
#
# This error is an unfortunate consequence of Scala using subtyping to encode algebraic data types. Without the
# annotation, the result type of the fold gets inferred as `Leaf[B]` and it is then expected that the second argument
# to `fold` will return `Leaf[B]`, which it doesn't (it returns `Branch[B]`). Really, we'd prefer Scala to
# infer `Tree[B]` as the result type in both cases. When working with algebraic data types in Scala, it's somewhat
# common to define helper functions that simply call the corresponding data constructors but give the less specific
# result type:
#
#   def leaf[A](a: A): Tree[A] = Leaf(a)
#   def branch[A](l: Tree[A], r: Tree[A]): Tree[A] = Branch(l, r)
def mapViaFold(t: Tree[A], f: Callable[[A], B]) -> Tree[B]:
    return fold(t, lambda a: leaf(f(a)), branch)


def leaf(a: A) -> Tree[A]:
    return Leaf(a)


def branch(l: Tree[B], r: Tree[B]) -> Tree[B]:
    return Branch(l, r)
