from chapter03.list import apply, List


def test_list_create() -> None:
    assert apply(1, 2, 3, 4, 5) == {}
