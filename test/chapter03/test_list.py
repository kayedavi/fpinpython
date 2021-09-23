from chapter03.list import listOf, sum, product, x, append, foldRight, sum2, product2, tail, setHead, drop, dropWhile, \
    init, init2, length, foldLeft, sum3, product3, reverse, foldRightViaFoldLeft, foldRightViaFoldLeft_1, \
    foldLeftViaFoldRight, appendViaFoldRight, concat, add1, map, map_1, map_2, filter, filter_1, filter_2, flatMap, \
    filterViaFlatMap, addPairwise, zipWith, startsWith, hasSubsequence


def test_sum() -> None:
    assert sum(listOf(1, 2, 3, 4)) == 10


def test_product() -> None:
    assert product(listOf(1, 2, 3, 4)) == 24.0


def test_pattern_matching() -> None:
    assert x() == 3


def test_append() -> None:
    assert append(listOf(1, 2, 3), listOf(4, 5, 6)) == listOf(1, 2, 3, 4, 5, 6)


def test_fold_right() -> None:
    assert foldRight(listOf(1, 2, 3, 4, 5), 3, (lambda x, y: x + y)) == 18


def test_sum2() -> None:
    assert sum2(listOf(1, 2, 3, 4)) == 10


def test_product2() -> None:
    assert product2(listOf(1, 2, 3, 4)) == 24.0


def test_tail() -> None:
    assert tail(listOf(1, 2, 3, 4)) == listOf(2, 3, 4)


def test_set_head() -> None:
    assert setHead(listOf(1, 2, 3, 4), 7) == listOf(7, 2, 3, 4)


def test_drop() -> None:
    assert drop(listOf(1, 2, 3, 4), 2) == listOf(3, 4)


def test_drop_while() -> None:
    assert dropWhile(listOf(1, 2, 3, 4), lambda x: x < 3) == listOf(3, 4)


def test_init() -> None:
    assert init(listOf(1, 2, 3, 4)) == listOf(1, 2, 3)


def test_init2() -> None:
    assert init2(listOf(1, 2, 3, 4)) == listOf(1, 2, 3)


def test_length() -> None:
    assert length(listOf(1, 2, 3, 4)) == 4


def test_fold_left() -> None:
    assert foldLeft(listOf(1, 2, 3, 4, 5), 3, (lambda y, x: x + y)) == 18


def test_sum3() -> None:
    assert sum3(listOf(1, 2, 3, 4)) == 10


def test_product3() -> None:
    assert product3(listOf(1, 2, 3, 4)) == 24.0


def test_reverse() -> None:
    assert reverse(listOf(1, 2, 3, 4)) == listOf(4, 3, 2, 1)


def test_fold_right_via_fold_left() -> None:
    assert foldRightViaFoldLeft(listOf(1, 2, 3, 4, 5), 3, (lambda x, y: x + y)) == 18


def test_fold_right_via_fold_left_1() -> None:
    assert foldRightViaFoldLeft_1(listOf(1, 2, 3, 4, 5), 3, (lambda x, y: x + y)) == 18


def test_fold_left_via_fold_right() -> None:
    assert foldLeftViaFoldRight(listOf(1, 2, 3, 4, 5), 3, (lambda y, x: x + y)) == 18


def test_append_via_fold_right() -> None:
    assert appendViaFoldRight(listOf(1, 2, 3), listOf(4, 5, 6)) == listOf(1, 2, 3, 4, 5, 6)


def test_concat() -> None:
    assert concat(listOf(listOf(1, 2), listOf(3, 4))) == listOf(1, 2, 3, 4)


def test_add1() -> None:
    assert add1(listOf(1, 2, 3, 4, 5)) == listOf(2, 3, 4, 5, 6)


def test_map() -> None:
    assert map(listOf('1', '2', '3'), int) == listOf(1, 2, 3)


def test_map_1() -> None:
    assert map_1(listOf('1', '2', '3'), int) == listOf(1, 2, 3)


def test_map_2() -> None:
    assert map_2(listOf('1', '2', '3'), int) == listOf(1, 2, 3)


def test_filter() -> None:
    assert filter(listOf(1, 2, 3, 4, 5, 6), lambda x: x % 2 == 0) == listOf(2, 4, 6)


def test_filter_1() -> None:
    assert filter_1(listOf(1, 2, 3, 4, 5, 6), lambda x: x % 2 == 0) == listOf(2, 4, 6)


def test_filter_2() -> None:
    assert filter_2(listOf(1, 2, 3, 4, 5, 6), lambda x: x % 2 == 0) == listOf(2, 4, 6)


def test_flat_map() -> None:
    assert flatMap(listOf(1, 2, 3), lambda x: listOf(str(x), str(x + 1))) == listOf('1', '2', '2', '3', '3', '4')


def test_filter_via_flat_map() -> None:
    assert filterViaFlatMap(listOf(1, 2, 3, 4, 5, 6), lambda x: x % 2 == 0) == listOf(2, 4, 6)


def test_add_pairwise() -> None:
    assert addPairwise(listOf(1, 2, 3, 4), listOf(3, 6, 8)) == listOf(4, 8, 11)


def test_zip_with() -> None:
    assert zipWith(listOf(1, 2, 3, 4), listOf(3, 6, 8), (lambda a, b: a + 2 * b)) == listOf(7, 14, 19)


def test_starts_with() -> None:
    assert startsWith(listOf(1, 2, 3, 4, 5, 6), listOf(1, 2, 3))
    assert not startsWith(listOf(1, 2, 3, 4, 5, 6), listOf(1, 3, 2))


def test_has_subsequence() -> None:
    assert hasSubsequence(listOf(1, 2, 3, 4, 5, 6), listOf(5, 6))
    assert hasSubsequence(listOf(), listOf())
    assert not hasSubsequence(listOf(1, 2, 3, 4, 5, 6), listOf(6, 7))
    assert not hasSubsequence(listOf(), listOf(6, 7))
