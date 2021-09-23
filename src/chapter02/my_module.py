from typing import Callable

from common.tail_call import TailCall, Return, Suspend

# A comment!
# Another comment
""" A documentation comment """


def absolute_value(n: int) -> int:
    return -n if n < 0 else n


def __format_abs(x: int) -> str:
    msg = 'The absolute value of %d is %d'
    return msg % (x, absolute_value(x))


if __name__ == '__main__':
    print(__format_abs(-42))


# A definition of factorial, using a local, tail recursive function
def factorial(n: int) -> int:
    def go(x: int, acc: int) -> TailCall[int]:
        if x <= 0:
            return Return(acc)
        else:
            return Suspend(lambda: go(x - 1, x * acc))

    return go(n, 1).eval()


# Another implementation of `factorial`, this time with a `while` loop
def factorial2(n: int) -> int:
    acc = 1
    i = n
    while i > 0:
        acc *= i
        i -= 1
    return acc


# Exercise 1: Write a function to compute the nth fibonacci number

# 0 and 1 are the first two numbers in the sequence,
# so we start the accumulators with those.
# At every iteration, we add the two numbers to get the next one.
def fib(n: int) -> int:
    def loop(x: int, prev: int, cur: int) -> TailCall[int]:
        return Return(prev) if x == 0 else Suspend(lambda: loop(x - 1, cur, prev + cur))

    return loop(n, 0, 1).eval()


# This definition and `formatAbs` are very similar..
def __format_factorial(n: int) -> str:
    msg = 'The factorial of %d is %d.'
    return msg % (n, factorial(n))


# We can generalize `formatAbs` and `formatFactorial` to
# accept a _function_ as a parameter
def format_result(name: str, n: int, f: Callable[[int], int]) -> str:
    msg = 'The %s of %d is %d.'
    return msg % (name, n, f(n))
