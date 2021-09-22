from unittest import TestCase

from chapter03.List import list_of, List, empty_list


class TestList(TestCase):
    def test_emptyList(self) -> None:
        assert 0 == empty_list().length()

    def test_append(self) -> None:
        x = list_of(1, 2, 3)
        y = list_of(4, 5, 6)
        assert list_of(1, 2, 3, 4, 5, 6) == x.append(y)

    def test_fold_right(self) -> None:
        total = list_of(1, 2, 3).fold_right(0, (lambda x, y: x + y))
        assert 6 == total

    def test_tail(self) -> None:
        expected = list_of(2, 3)
        actual = list_of(1, 2, 3).tail()
        assert expected == actual

    def test_head(self) -> None:
        assert 1 == list_of(1, 2, 3).head()

    def test_set_head(self) -> None:
        xs = list_of(1, 2, 3).set_head(5)
        assert list_of(5, 2, 3) == xs

    def test_drop(self) -> None:
        assert list_of(3, 4) == list_of(1, 2, 3, 4).drop(2)

    def test_drop_while(self) -> None:
        xs = list_of(1, 2, 3, 4, 5, 6)
        assert list_of(4, 5, 6) == xs.drop_while(lambda x: x < 4)

    def test_init(self) -> None:
        self.assertEqual(list_of(1, 2, 3), list_of(1, 2, 3, 4).init())

    def test_fold_left(self) -> None:
        self.assertEqual("4321", list_of(1, 2, 3, 4).fold("", (lambda b, a: f'{a}{b}')))

    def test_length(self) -> None:
        self.assertEqual(4, list_of(1, 2, 3, 4).length())

    def test_reverse(self) -> None:
        self.assertEqual(list_of(4, 3, 2, 1), list_of(1, 2, 3, 4).reverse())

    def test_map(self) -> None:
        self.assertEqual(list_of(2, 4, 6, 8), list_of(1, 2, 3, 4).map(lambda x: x * 2))

    def test_filter(self) -> None:
        self.assertEqual(list_of(2, 4), list_of(1, 2, 3, 4).filter(lambda x: x % 2 == 0))

    def test_concat(self) -> None:
        self.assertEqual(list_of(1, 2), List.concat(list_of(list_of(1), list_of(2))))

    def test_flat_map(self) -> None:
        self.assertEqual(list_of(1, 1, 2, 2), list_of(1, 2).flat_map(lambda x: list_of(x, x)))

    def test_zip_with(self) -> None:
        self.assertEqual(list_of(5, 7, 9), list_of(1, 2, 3).zip_with(list_of(4, 5, 6), (lambda a, b: a + b)))

    def test_to_string(self) -> None:
        self.assertEqual("[1, 2, 3, 4]", str(list_of(1, 2, 3, 4)))

    def test_toPython(self) -> None:
        actual = list_of(1, 2, 3, 4).to_python()
        self.assertTrue(isinstance(actual, list))
        self.assertEqual([1, 2, 3, 4], actual)
        self.assertEqual([], empty_list().to_python())

    def test_startWith(self) -> None:
        self.assertTrue(list_of(1, 2, 3, 4).starts_with(list_of(1, 2)))
        self.assertFalse(list_of(1, 2).starts_with(list_of(0)))

    def test_hasSubsequence(self) -> None:
        assert list_of(1, 2, 3, 4, 5).has_subsequence(list_of(1))
        assert list_of(1, 2, 3, 4, 5).has_subsequence(list_of(1, 2))
        assert list_of(1, 2, 3, 4, 5).has_subsequence(list_of(1, 2, 3, 4, 5))
        assert list_of(1, 2, 3, 4, 5).has_subsequence(list_of(4, 5))
        assert list_of(1, 2, 3, 4, 5).has_subsequence(list_of(5))
        assert not list_of(1, 2, 3, 4, 5).has_subsequence(list_of(0))
        assert not list_of(1, 2, 3, 4, 5).has_subsequence(list_of(5, 6))

    def test_map_filter_flatMap(self) -> None:
        expected: List[int] = list_of(6, 6, 12, 12)
        actual: List[int] = list_of(1, 2, 3, 4, 5, 6, 7, 8) \
            .map(lambda it: it * 2) \
            .filter(lambda it: it % 3 == 0) \
            .flat_map(lambda it: list_of(it, it))
        assert expected == actual

    def test_group_by(self) -> None:
        actual = list_of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10).group_by(lambda it: it % 2)
        expected = {0: list_of(2, 4, 6, 8, 10), 1: list_of(1, 3, 5, 7, 9)}
        assert expected == actual
