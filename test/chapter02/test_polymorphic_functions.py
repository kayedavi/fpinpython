from chapter02.polymorphic_functions import find_first, is_sorted, partial1, curry, uncurry, compose, binary_search


def test_binary_search() -> None:
    assert binary_search([1, 2, 3, 4, 5], 4, (lambda a, b: a > b)) == 3


def test_find_first() -> None:
    assert find_first([6, 5, 4, 3, 2, 1], lambda x: x < 4) == 3
    assert find_first([], lambda x: x < 4) == -1
    assert find_first([], lambda x: x > 10) == -1
    assert find_first([6, 5, 4, 3, 2, 1], lambda x: x < 10) == 0


def test_is_sorted() -> None:
    assert is_sorted([1, 3, 5, 7, 9], (lambda a, b: a > b))
    assert not is_sorted([9, 8, 7, 6, 5, 4, 3, 2, 1], (lambda a, b: a > b))
    assert is_sorted([], (lambda a, b: a > b))


def test_partial1() -> None:
    def add(a: int, b: int) -> int:
        return a + b

    partial = partial1(5, add)
    assert partial(2) == 7


def test_curry() -> None:
    def add(a: int, b: int) -> int:
        return a + b

    curried = curry(add)
    assert curried(5)(2) == 7


def test_uncurry() -> None:
    def add(a: int, b: int) -> int:
        return a + b

    uncurried = uncurry(curry(add))
    assert uncurried(5, 2) == 7


def test_compose() -> None:
    c = compose(str, int)
    assert c(7.2) == "7"
