from typing import Iterable, Sequence

from Standard import KList, also, let, take_if, take_unless, also_optional


def test_klist() -> None:
    xs = KList(1, 2, 3)
    assert xs[0] == 1
    assert xs[1] == 2
    assert xs[2] == 3
    assert isinstance(xs, list)


def test_map() -> None:
    xs = KList(1, 2, 3).map(lambda it: it * 2)
    assert xs == KList(2, 4, 6)
    assert isinstance(xs, list)


def test_flat_map() -> None:
    xs = KList(1, 2, 3).flat_map(lambda it: KList(it, it))
    assert xs == KList(1, 1, 2, 2, 3, 3)


def test_filter() -> None:
    xs = KList(1, 2, 3, 4, 5).filter(lambda it: it % 2 == 0)
    assert xs == KList(2, 4)


def test_group_by() -> None:
    xs = KList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10).group_by(lambda it: it % 2)
    print(xs)
    assert xs == {0: KList(2, 4, 6, 8, 10), 1: KList(1, 3, 5, 7, 9)}


def test_size() -> None:
    xs = KList(1, 2, 3, 4, 5)
    assert 5 == xs.size()


def test_from_list() -> None:
    xs = [1, 2, 3, 4, 5]
    kxs = KList(*xs)
    assert kxs == KList(1, 2, 3, 4, 5)


def test_in() -> None:
    assert 2 in KList(1, 2, 3, 4, 5)


def test_contains_all() -> None:
    assert KList(1, 2, 3, 4, 5).contains_all(KList(2, 4))


def test_isempty() -> None:
    assert KList().is_empty()


def test_reversed() -> None:
    assert KList(1, 2, 3, 4, 5).reversed() == KList(5, 4, 3, 2, 1)


def test_also() -> None:
    assert also([4], lambda it: it.append(5)) == [4, 5]


def test_also_optional() -> None:
    assert also_optional([4], lambda it: it.append(5)) == [4, 5]
    assert also_optional(None, lambda it: it.append(5)) is None


def test_let() -> None:
    assert let(KList(1, 2, 3), lambda it: it.map(lambda x: str(x))) == KList('1', '2', '3')


def test_take_if() -> None:
    assert take_if(3, lambda x: x % 3 == 0) == 3
    assert take_if(3, lambda x: x % 3 == 1) is None


def test_take_unless() -> None:
    assert take_unless(4, lambda x: x % 2 == 0) is None
    assert take_unless(3, lambda x: x % 2 == 0) is 3


def test_add() -> None:
    assert KList(1, 2) + KList(3, 4) == KList(1, 2, 3, 4)


def test_get_or_none() -> None:
    assert KList(1, 2).get_or_none(3) is None
    assert KList(1, 2).get_or_none(1) == 2


def test_get_or_else() -> None:
    assert KList(1, 2).get_or_else(3, lambda: 5) == 5
    assert KList(1, 2).get_or_else(1, lambda: 5) == 2


def test_fold() -> None:
    assert KList(1, 2, 3, 4).fold('', (lambda b, a: f'{a}{b}')) == '4321'


def test_fold_right() -> None:
    total = KList(1, 2, 3).fold_right(0, (lambda x, y: x + y))
    assert 6 == total


def test_contains() -> None:
    assert KList(1, 2, 3, 4, 5).contains(2)
    assert not KList(1, 2, 3, 4, 5).contains(0)


def test_index_of() -> None:
    assert KList(1, 2, 3, 4, 5).index_of(3) == 2
    assert KList(1, 2, 3, 4, 5).index_of(6) == -1


def test_iterator() -> None:
    xs = KList(1, 2, 3, 4, 5)
    total = 0
    for x in xs.iterator():
        total += x
    assert total == 15


def test_last_index_of() -> None:
    xs = KList(1, 2, 3, 4, 3, 2, 1)
    assert xs.last_index_of(2) == 5
    assert xs.last_index_of(5) == -1


def test_sub_list() -> None:
    assert KList(1, 2, 3, 4, 5, 6).sub_list(2, 4) == KList(3, 4)


def test_indices() -> None:
    assert KList(1, 2, 3, 4, 5, 6).indices() == range(6)


def test_last_index() -> None:
    assert KList(1, 2, 3, 4, 5).last_index() == 4
    assert KList().last_index() == -1


def test_all() -> None:
    assert KList(1, 2, 3, 4, 5).all(lambda it: it < 10)
    assert not KList(1, 2, 3, 4, 5).all(lambda it: it < 4)


def test_any() -> None:
    assert KList(1, 2, 3, 4, 5).any(lambda it: it < 10)
    assert not KList(1, 2, 3, 4, 5).any(lambda it: it < 1)


def test_as_iterable() -> None:
    assert isinstance(KList(1, 2, 3, 4, 5).as_iterable(), Iterable)


def test_as_sequence() -> None:
    assert isinstance(KList(1, 2, 3, 4, 5).as_sequence(), Sequence)


def test_associate() -> None:
    expected = {'1': 'David has 1 dollars', '2': 'David has 2 dollars', '3': 'David has 3 dollars',
                '4': 'David has 4 dollars', '5': 'David has 5 dollars'}
    actual = KList(1, 2, 3, 4, 5).associate(lambda it: (str(it), f'David has {it} dollars'))
    assert actual == expected


def test_map_filter_flat_map() -> None:
    expected = KList(6, 6, 12, 12)
    actual = KList(1, 2, 3, 4, 5, 6, 7, 8) \
        .map(lambda it: it * 2) \
        .filter(lambda it: it % 3 == 0) \
        .flat_map(lambda it: KList(it, it))
    assert expected == actual
