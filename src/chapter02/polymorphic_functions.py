from typing import TypeVar, Callable

from common.tail_call import TailCall, Return, Suspend

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


# Here's a polymorphic version of `binarySearch`, parameterized on
# a function for testing whether an `A` is greater than another `A`.
def binary_search(xs: list[A], key: A, gt: Callable[[A, A], bool]) -> int:
    def go(low: int, mid: int, high: int) -> TailCall[int]:
        if low > high:
            return Return(-mid - 1)
        else:
            mid2 = (low + high) // 2
            x = xs[mid2]
            greater = gt(x, key)
            if not greater and not gt(key, x):
                return Return(mid2)
            elif greater:
                return Suspend(lambda: go(low, mid2, mid2 - 1))
            else:
                return Suspend(lambda: go(mid2 + 1, mid2, high))

    return go(0, 0, len(xs) - 1).eval()


# Here's a polymorphic version of `find_first`, parameterized on
# a function for testing whether an `A` is the element we want to find.
# Instead of hard-coding `str`, we take a type `A` as a parameter.
# And instead of hard-coding an equality check for a given key,
# we take a function with which to test each element of the list.
def find_first(xs: list[A], p: Callable[[A], bool]) -> int:
    def loop(n: int) -> TailCall[int]:
        if n >= len(xs):
            return Return(-1)
        # If the function `p` matches the current element,
        # we've found a match and we return its index in the list.
        elif p(xs[n]):
            return Return(n)
        else:
            return Suspend(lambda: loop(n + 1))

    return loop(0).eval()


# Exercise 2: Implement a polymorphic function to check whether
# a `list[A]` is sorted
def is_sorted(xs: list[A], gt: Callable[[A, A], bool]) -> bool:
    def go(n: int) -> TailCall[bool]:
        if n >= len(xs) - 1:
            return Return(True)
        elif gt(xs[n], xs[n + 1]):
            return Return(False)
        else:
            return Suspend(lambda: go(n + 1))

    return go(0).eval()


# Polymorphic functions are often so constrained by their type
# that they only have one implementation! Here's an example:

def partial1(a: A, f: Callable[[A, B], C]) -> Callable[[B], C]:
    return lambda b: f(a, b)


# Exercise 3: Implement `curry`.

# Note that `=>` associates to the right, so we could
# write the return type as `A => B => C`
def curry(f: Callable[[A, B], C]) -> Callable[[A], Callable[[B], C]]:
    return lambda a: lambda b: f(a, b)


# NB: The `Function2` trait has a `curried` method already

# Exercise 4: Implement `uncurry`
def uncurry(f: Callable[[A], Callable[[B], C]]) -> Callable[[A, B], C]:
    return lambda a, b: f(a)(b)


# NB: There is a method on the `Function` object in the standard library,
# `Function.uncurried` that you can use for uncurrying.
# Note that we can go back and forth between the two forms. We can curry
# and uncurry and the two forms are in some sense "the same". In FP jargon,
# we say that they are _isomorphic_ ("iso" = same; "morphe" = shape, form),
# a term we inherit from category theory.

# Exercise 5: Implement `compose`

def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    return lambda a: f(g(a))
