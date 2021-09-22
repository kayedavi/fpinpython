from chapter02.monomorphic_binary_search import find_first, binary_search


def test_binary_search() -> None:
    assert binary_search([1.3, 2.8, 3.1, 4.1, 5.2], 4.1) == 3


def test_find_first() -> None:
    assert find_first(['a', 'b', 'c', 'd', 'e'], 'e') == 4
    assert find_first(['a', 'b', 'c', 'd', 'e'], 'f') == -1
    assert find_first([], 'f') == -1
