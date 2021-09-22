from unittest import TestCase

from chapter03.List import listOf, List, emptyList


class TestList(TestCase):
    def test_emptyList(self) -> None:
        assert 0 == emptyList().length()

    def test_append(self) -> None:
        x = listOf(1, 2, 3)
        y = listOf(4, 5, 6)
        assert listOf(1, 2, 3, 4, 5, 6) == x.append(y)

    def test_fold_right(self) -> None:
        total = listOf(1, 2, 3).foldRight(0, (lambda x, y: x + y))
        assert 6 == total

    def test_tail(self) -> None:
        expected = listOf(2, 3)
        actual = listOf(1, 2, 3).tail()
        assert expected == actual

    def test_head(self) -> None:
        assert 1 == listOf(1, 2, 3).head()

    def test_set_head(self) -> None:
        xs = listOf(1, 2, 3).setHead(5)
        assert listOf(5, 2, 3) == xs

    def test_drop(self) -> None:
        assert listOf(3, 4) == listOf(1, 2, 3, 4).drop(2)

    def test_drop_while(self) -> None:
        xs = listOf(1, 2, 3, 4, 5, 6)
        assert listOf(4, 5, 6) == xs.dropWhile(lambda x: x < 4)

    def test_init(self) -> None:
        self.assertEqual(listOf(1, 2, 3), listOf(1, 2, 3, 4).init())

    def test_fold_left(self) -> None:
        self.assertEqual("4321", listOf(1, 2, 3, 4).fold("", (lambda b, a: f'{a}{b}')))

    def test_length(self) -> None:
        self.assertEqual(4, listOf(1, 2, 3, 4).length())

    def test_reverse(self) -> None:
        self.assertEqual(listOf(4, 3, 2, 1), listOf(1, 2, 3, 4).reverse())

    def test_map(self) -> None:
        self.assertEqual(listOf(2, 4, 6, 8), listOf(1, 2, 3, 4).map(lambda x: x * 2))

    def test_filter(self) -> None:
        self.assertEqual(listOf(2, 4), listOf(1, 2, 3, 4).filter(lambda x: x % 2 == 0))

    def test_concat(self) -> None:
        self.assertEqual(listOf(1, 2), List.concat(listOf(listOf(1), listOf(2))))

    def test_flat_map(self) -> None:
        self.assertEqual(listOf(1, 1, 2, 2), listOf(1, 2).flatMap(lambda x: listOf(x, x)))

    def test_zip_with(self) -> None:
        self.assertEqual(listOf(5, 7, 9), listOf(1, 2, 3).zipWith(listOf(4, 5, 6), (lambda a, b: a + b)))

    def test_to_string(self) -> None:
        self.assertEqual("[1, 2, 3, 4]", str(listOf(1, 2, 3, 4)))

    def test_toPython(self) -> None:
        actual = listOf(1, 2, 3, 4).toPython()
        self.assertTrue(isinstance(actual, list))
        self.assertEqual([1, 2, 3, 4], actual)
        self.assertEqual([], emptyList().toPython())

    def test_startWith(self) -> None:
        self.assertTrue(listOf(1, 2, 3, 4).startsWith(listOf(1, 2)))
        self.assertFalse(listOf(1, 2).startsWith(listOf(0)))

    def test_hasSubsequence(self) -> None:
        assert listOf(1, 2, 3, 4, 5).hasSubsequence(listOf(1))
        assert listOf(1, 2, 3, 4, 5).hasSubsequence(listOf(1, 2))
        assert listOf(1, 2, 3, 4, 5).hasSubsequence(listOf(1, 2, 3, 4, 5))
        assert listOf(1, 2, 3, 4, 5).hasSubsequence(listOf(4, 5))
        assert listOf(1, 2, 3, 4, 5).hasSubsequence(listOf(5))
        assert not listOf(1, 2, 3, 4, 5).hasSubsequence(listOf(0))
        assert not listOf(1, 2, 3, 4, 5).hasSubsequence(listOf(5, 6))

    def test_map_filter_flatMap(self) -> None:
        expected: List[int] = listOf(6, 6, 12, 12)
        actual: List[int] = listOf(1, 2, 3, 4, 5, 6, 7, 8) \
            .map(lambda it: it * 2) \
            .filter(lambda it: it % 3 == 0) \
            .flatMap(lambda it: listOf(it, it))
        assert expected == actual

    def test_group_by(self) -> None:
        actual = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10).groupBy(lambda it: it % 2)
        expected = {0: listOf(2, 4, 6, 8, 10), 1: listOf(1, 3, 5, 7, 9)}
        assert expected == actual
