from chapter04.option import Some, Nothing, map2, sequenceViaTraverse, traverse
from common.list import list_of


def test_Some() -> None:
    assert 5 == Some(5).get


def test_map() -> None:
    assert Some(2).map(lambda it: it * 3) == Some(6)


def test_getOrElse() -> None:
    assert Some(3).getOrElse(lambda: 4) == 3
    assert Nothing().getOrElse(lambda: 4) == 4


def test_flatMap() -> None:
    assert Some(2).flatMap(lambda it: Some(it + 3)) == Some(5)
    assert Nothing().flatMap(lambda it: Some(it + 3)) == Nothing()


def test_flatMap_1() -> None:
    assert Some(2).flatMap_1(lambda it: Some(it + 3)) == Some(5)
    assert Nothing().flatMap_1(lambda it: Some(it + 3)) == Nothing()


def test_orElse() -> None:
    assert Some(5).orElse(lambda: Some(4)) == Some(5)
    assert Nothing().orElse(lambda: Some(4)) == Some(4)

def test_orElse_1() -> None:
    assert Some(5).orElse_1(lambda: Some(4)) == Some(5)
    assert Nothing().orElse_1(lambda: Some(4)) == Some(4)


def test_filter() -> None:
    assert Some(5).filter(lambda it: it % 2 == 1) == Some(5)
    assert Some(4).filter(lambda it: it % 2 == 1) == Nothing()

def test_filter_1() -> None:
    assert Some(5).filter_1(lambda it: it % 2 == 1) == Some(5)
    assert Some(4).filter_1(lambda it: it % 2 == 1) == Nothing()


def test_map2() -> None:
    assert map2(Some(1), Some(2), (lambda a, b: a + b)) == Some(3)
    assert map2(Some(1), Nothing(), (lambda a, b: a + b)) == Nothing()


def test_sequenceViaTraverse() -> None:
    assert sequenceViaTraverse(list_of(Some(1), Some(2), Some(3))) == Some(list_of(1, 2, 3))


def test_traverse() -> None:
    xs = traverse(list_of(1, 2, 3, 4), lambda it: Some(it / 2.0))
    assert xs == Some(list_of(0.5, 1.0, 1.5, 2.0))
