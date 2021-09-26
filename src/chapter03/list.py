from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

from common.tail_call import TailCall, Return, Suspend

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
Nothing = TypeVar('Nothing')

class List(Generic[A]):  # `List` data type, parameterized on a type, `A`
    pass


@dataclass(frozen=True)
class Nil(List[Nothing]):  # A `List` data constructor representing the empty list
    pass


# Another data constructor, representing nonempty lists. Note that `tail` is another `List[A]`,
# which may be `Nil` or another `Cons`.
@dataclass(frozen=True)
class Cons(List[A]):
    head: A
    tail: List[A]


# `list` module. Contains functions for creating and working with lists.

def sum(ints: List[int]) -> int:  # A function that uses pattern matching to add up a list of integers
    match ints:
        case Nil():
            return 0  # The sum of the empty list is 0.
        case Cons(x, xs):
            return x + sum(xs)  # The sum of a list starting with `x` is `x` plus the sum of the rest of the list.


def product(ds: List[float]) -> float:
    match ds:
        case Nil():
            return 1.0
        case Cons(0.0, _):
            return 0.0
        case Cons(x, xs):
            return x * product(xs)


def listOf(*xs: A) -> List[A]:  # Variadic function syntax
    if len(xs) == 0:
        return Nil()
    else:
        return Cons(xs[0], listOf(*xs[1:]))


def x() -> int:
    match listOf(1, 2, 3, 4, 5):
        case Cons(x, Cons(2, Cons(4, _))):
            return x
        case Nil():
            return 42
        case Cons(x, Cons(y, Cons(3, Cons(4, _)))):
            return x + y
        case Cons(h, t):
            return h + sum(t)
        case _:
            return 101


def append(a1: List[A], a2: List[A]) -> List[A]:
    match a1:
        case Nil():
            return a2
        case Cons(h, t):
            return Cons(h, append(t, a2))


def foldRight(xs: List[A], z: B, f: Callable[[A, B], B]) -> B:  # Utility functions
    match xs:
        case Nil():
            return z
        case Cons(h, t):
            return f(h, foldRight(t, z, f))


def sum2(ns: List[int]) -> int:
    return foldRight(ns, 0, (lambda x, y: x + y))


def product2(ns: List[float]) -> float:
    return foldRight(ns, 1.0, (lambda x, y: x * y))


# 3. The third case is the first that matches, with `x` bound to 1 and `y` bound to 2.

# Although we could return `Nil` when the input list is empty, we choose to throw an exception instead. This is
# a somewhat subjective choice. In our experience, taking the tail of an empty list is often a bug, and silently
# returning a value just means this bug will be discovered later, further from the place where it was introduced.
#
# It's generally good practice when pattern matching to use `_` for any variables you don't intend to use on the
# right hand side of a pattern. This makes it clear the value isn't relevant.
def tail(l: List[A]) -> List[A]:
    match l:
        case Nil():
            raise RuntimeError('tail of empty list')
        case Cons(_, t):
            return t


# If a function body consists solely of a match expression, we'll often put the match on the same line as the
# function signature, rather than introducing another level of nesting.
def setHead(l: List[A], h: A) -> List[A]:
    match l:
        case Nil():
            raise RuntimeError('setHead on empty list')
        case Cons(_, t):
            return Cons(h, t)


# Again, it's somewhat subjective whether to throw an exception when asked to drop more elements than the list
# contains. The usual default for `drop` is not to throw an exception, since it's typically used in cases where this
# is not indicative of a programming error. If you pay attention to how you use `drop`, it's often in cases where the
# length of the input list is unknown, and the number of elements to be dropped is being computed from something else.
# If `drop` threw an exception, we'd have to first compute or check the length and only drop up to that many elements.
def drop(l: List[A], n: int) -> List[A]:
    if n <= 0:
        return l
    else:
        match l:
            case Nil():
                return Nil()
            case Cons(_, t):
                return drop(t, n - 1)


# Somewhat overkill, but to illustrate the feature we're using a _pattern guard_, to only match a `Cons` whose head
# satisfies our predicate, `f`. The syntax is to add `if <cond>` after the pattern, before the `=>`, where `<cond>` can
# use any of the variables introduced by the pattern.
def dropWhile(l: List[A], f: Callable[[A], bool]) -> List[A]:
    match l:
        case Cons(h, t) if f(h):
            return dropWhile(t, f)
        case _:
            return l


# Note that we're copying the entire list up until the last element. Besides being inefficient, the natural recursive
# solution will use a stack frame for each element of the list, which can lead to stack overflows for
# large lists (can you see why?). With lists, it's common to use a temporary, mutable buffer internal to the
# function (with lazy lists or streams, which we discuss in chapter 5, we don't normally do this). So long as the
# buffer is allocated internal to the function, the mutation is not observable and RT is preserved.
#
# Another common convention is to accumulate the output list in reverse order, then reverse it at the end, which
# doesn't require even local mutation. We'll write a reverse function later in this chapter.
def init(l: List[A]) -> List[A]:
    match l:
        case Nil():
            raise RuntimeError('init of empty list')
        case Cons(_, Nil()):
            return Nil()
        case Cons(h, t):
            return Cons(h, init(t))


def init2(l: List[A]) -> List[A]:
    buf: list[A] = []

    def go(cur: List[A]) -> TailCall[List[A]]:
        match cur:
            case Nil():
                raise RuntimeError('init of empty list')
            case Cons(_, Nil()):
                return Return(listOf(*buf))
            case Cons(h, t):
                buf.append(h)
                return Suspend(lambda: go(t))

    return go(l).eval()


# No, this is not possible! The reason is because _before_ we ever call our function, `f`, we evaluate its argument,
# which in the case of `foldRight` means traversing the list all the way to the end. We need _non-strict_ evaluation
# to support early termination---we discuss this in chapter 5.

# We get back the original list! Why is that? As we mentioned earlier, one way of thinking about what `foldRight` "does"
# is it replaces the `Nil` constructor of the list with the `z` argument, and it replaces the `Cons` constructor with
# the given function, `f`. If we just supply `Nil` for `z` and `Cons` for `f`, then we get back the input list.
#
# foldRight(Cons(1, Cons(2, Cons(3, Nil))), Nil:List[Int])(Cons(_,_))
# Cons(1, foldRight(Cons(2, Cons(3, Nil)), Nil:List[Int])(Cons(_,_)))
# Cons(1, Cons(2, foldRight(Cons(3, Nil), Nil:List[Int])(Cons(_,_))))
# Cons(1, Cons(2, Cons(3, foldRight(Nil, Nil:List[Int])(Cons(_,_)))))
# Cons(1, Cons(2, Cons(3, Nil)))
def length(l: List[A]) -> int:
    return foldRight(l, 0, (lambda _, acc: acc + 1))


# It's common practice to annotate functions you expect to be tail-recursive with the `tailrec` annotation. If the
# function is not tail-recursive, it will yield a compile error, rather than silently compiling the code and resulting
# in greater stack space usage at runtime.
def foldLeft(l: List[A], z: B, f: Callable[[B, A], B]) -> B:
    def go(l: List[A], z: B, f: Callable[[B, A], B]) -> TailCall[B]:
        match l:
            case Nil():
                return Return(z)
            case Cons(h, t):
                return Suspend(lambda: go(t, f(z, h), f))

    return go(l, z, f).eval()


def sum3(l: List[int]) -> int:
    return foldLeft(l, 0, (lambda x, y: x + y))


def product3(l: List[float]) -> float:
    return foldLeft(l, 1.0, (lambda x, y: x * y))


def length2(l: List[A]) -> int:
    return foldLeft(l, 0, (lambda acc, _: acc + 1))


def reverse(l: List[A]) -> List[A]:
    return foldLeft(l, listOf(), (lambda acc, h: Cons(h, acc)))


# The implementation of `foldRight` in terms of `reverse` and `foldLeft` is a common trick for avoiding stack overflows
# when implementing a strict `foldRight` function as we've done in this chapter. (We'll revisit this in a later chapter,
# when we discuss laziness).

# The other implementations build up a chain of functions which, when called, results in the operations being performed
# with the correct associativity. We are calling `foldRight` with the `B` type being instantiated to `B => B`, then
# calling the built up function with the `z` argument. Try expanding the definitions by substituting equals for equals
# using a simple example, like `foldLeft(List(1,2,3), 0)(_ + _)` if this isn't clear. Note these implementations are
# more of theoretical interest - they aren't stack-safe and won't work for large lists.
def foldRightViaFoldLeft(l: List[A], z: B, f: Callable[[A, B], B]) -> B:
    return foldLeft(reverse(l), z, (lambda b, a: f(a, b)))


def foldRightViaFoldLeft_1(l: List[A], z: B, f: Callable[[A, B], B]) -> B:
    return foldLeft(l, lambda b: b, (lambda g, a: lambda c: g(f(a, c))))(z)


def foldLeftViaFoldRight(l: List[A], z: B, f: Callable[[B, A], B]) -> B:
    return foldRight(l, lambda b: b, (lambda a, g: lambda b: g(f(b, a))))(z)


# `append` simply replaces the `Nil` constructor of the first list with the second list, which is exactly the operation
# performed by `foldRight`.
def appendViaFoldRight(l: List[A], r: List[A]) -> List[A]:
    return foldRight(l, r, Cons)


# Since `append` takes time proportional to its first argument, and this first argument never grows because of the
# right-associativity of `foldRight`, this function is linear in the total length of all lists. You may want to try
# tracing the execution of the implementation on paper to convince yourself that this works.

# Note that we're simply referencing the `append` function, without writing something like `(x,y) => append(x,y)`
# or `append(_,_)`. In Scala there is a rather arbitrary distinction between functions defined as _methods_, which are
# introduced with the `def` keyword, and function values, which are the first-class objects we can pass to other
# functions, put in collections, and so on. This is a case where Scala lets us pretend the distinction doesn't exist.
# In other cases, you'll be forced to write `append _` (to convert a `def` to a function value)
# or even `(x: List[A], y: List[A]) => append(x,y)` if the function is polymorphic and the type arguments aren't known.
def concat(l: List[List[A]]) -> List[A]:
    return foldRight(l, listOf(), append)


def add1(l: List[int]) -> List[int]:
    return foldRight(l, listOf(), (lambda h, t: Cons(h + 1, t)))


def doubleToString(l: List[float]) -> List[str]:
    return foldRight(l, listOf(), (lambda h, t: Cons(str(h), t)))


# A natural solution is using `foldRight`, but our implementation of `foldRight` is not stack-safe. We can
# use `foldRightViaFoldLeft` to avoid the stack overflow (variation 1), but more commonly, with our current
# implementation of `List`, `map` will just be implemented using local mutation (variation 2). Again, note that the
# mutation isn't observable outside the function, since we're only mutating a buffer that we've allocated.
def map(l: List[A], f: Callable[[A], B]) -> List[B]:
    return foldRight(l, listOf(), (lambda h, t: Cons(f(h), t)))


def map_1(l: List[A], f: Callable[[A], B]) -> List[B]:
    return foldRightViaFoldLeft(l, listOf(), (lambda h, t: Cons(f(h), t)))


def map_2(l: List[A], f: Callable[[A], B]) -> List[B]:
    buf: list[B] = []

    def go(l: List[A]) -> TailCall[None]:
        match l:
            case Nil():
                return Return(None)
            case Cons(h, t):
                buf.append(f(h))
                return Suspend(lambda: go(t))

    go(l).eval()
    return listOf(*buf)  # converting from the standard Scala list to the list we've defined here


# The discussion about `map` also applies here.
def filter(l: List[A], f: Callable[[A], bool]) -> List[A]:
    return foldRight(l, listOf(), (lambda h, t: Cons(h, t) if f(h) else t))


def filter_1(l: List[A], f: Callable[[A], bool]) -> List[A]:
    return foldRightViaFoldLeft(l, listOf(), (lambda h, t: Cons(h, t) if f(h) else t))


def filter_2(l: List[A], f: Callable[[A], bool]) -> List[A]:
    buf: list[A] = []

    def go(l: List[A]) -> TailCall[None]:
        match l:
            case Nil():
                return Return(None)
            case Cons(h, t):
                if f(h): buf.append(h)
                return Suspend(lambda: go(t))

    go(l).eval()
    return listOf(*buf)  # converting from the standard Scala list to the list we've defined here


# This could also be implemented directly using `foldRight`.
def flatMap(l: List[A], f: Callable[[A], List[B]]) -> List[B]:
    return concat(map(l, f))


def filterViaFlatMap(l: List[A], f: Callable[[A], List[B]]) -> List[B]:
    return flatMap(l, lambda a: listOf(a) if f(a) else Nil())


# To match on multiple values, we can put the values into a pair and match on the pair, as shown next, and the same
# syntax extends to matching on N values (see sidebar "Pairs and tuples in Scala" for more about pair and tuple
# objects). You can also (somewhat less conveniently, but a bit more efficiently) nest pattern matches: on the
# right hand side of the `=>`, simply begin another `match` expression. The inner `match` will have access to all the
# variables introduced in the outer `match`.
#
# The discussion about stack usage from the explanation of `map` also applies here.
def addPairwise(a: List[int], b: List[int]) -> List[int]:
    match (a, b):
        case (Nil(), _):
            return Nil()
        case (_, Nil()):
            return Nil()
        case (Cons(h1, t1), Cons(h2, t2)):
            return Cons(h1 + h2, addPairwise(t1, t2))


# This function is usually called `zipWith`. The discussion about stack usage from the explanation of `map` also
# applies here. By putting the `f` in the second argument list, Scala can infer its type from the previous argument list.
def zipWith(a: List[A], b: List[B], f: Callable[[A, B], C]) -> List[C]:
    match (a, b):
        case (Nil(), _):
            return Nil()
        case (_, Nil()):
            return Nil()
        case (Cons(h1, t1), Cons(h2, t2)):
            return Cons(f(h1, h2), zipWith(t1, t2, f))


# There's nothing particularly bad about this implementation,
# except that it's somewhat monolithic and easy to get wrong.
# Where possible, we prefer to assemble functions like this using
# combinations of other functions. It makes the code more obviously
# correct and easier to read and understand. Notice that in this
# implementation we need special purpose logic to break out of our
# loops early. In Chapter 5 we'll discuss ways of composing functions
# like this from simpler components, without giving up the efficiency
# of having the resulting functions work in one pass over the data.
#
# It's good to specify some properties about these functions.
# For example, do you expect these expressions to be true?
#
# (xs append ys) startsWith xs
# xs startsWith Nil
# (xs append ys append zs) hasSubsequence ys
# xs hasSubsequence Nil
def startsWith(l: List[A], prefix: List[A]) -> bool:
    def go(l: List[A], prefix: List[A]) -> TailCall[bool]:
        match (l, prefix):
            case (_, Nil()):
                return Return(True)
            case (Cons(h, t), Cons(h2, t2)) if h == h2:
                return Suspend(lambda: go(t, t2))
            case _:
                return Return(False)

    return go(l, prefix).eval()


def hasSubsequence(sup: List[A], sub: List[A]) -> bool:
    def go(sup: List[A], sub: List[A]) -> TailCall[bool]:
        match sup:
            case Nil():
                return Return(sub == Nil())
            case _ if startsWith(sup, sub):
                return Return(True)
            case Cons(_, t):
                return Suspend(lambda: go(t, sub))

    return go(sup, sub).eval()
