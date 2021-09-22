from unittest import TestCase

from chapter03.List import list_of
from chapter04.option import Some, Nonentity, map2, sequence, traverse


class TestOption(TestCase):
    def test_Some(self) -> None:
        self.assertEqual(5, Some(5).get)

    def test_map(self) -> None:
        self.assertEqual(Some(6), Some(2).map(lambda it: it * 3))

    def test_getOrElse(self) -> None:
        self.assertEqual(3, Some(3).get_or_else(lambda: 4))
        self.assertEqual(4, Nonentity().get_or_else(lambda: 4))

    def test_flatMap(self) -> None:
        self.assertEqual(Some(5), Some(2).flat_map(lambda it: Some(it + 3)))
        self.assertEqual(Nonentity(), Nonentity().flat_map(lambda it: Some(it + 3)))

    def test_orElse(self) -> None:
        self.assertEqual(Some(5), Some(5).or_else(lambda: Some(4)))
        self.assertEqual(Some(4), Nonentity().or_else(lambda: Some(4)))

    def test_filter(self) -> None:
        self.assertEqual(Some(5), Some(5).filter(lambda it: it % 2 == 1))
        self.assertEqual(Nonentity(), Some(4).filter(lambda it: it % 2 == 1))

    def test_map2(self) -> None:
        self.assertEqual(Some(3), map2(Some(1), Some(2), (lambda a, b: a + b)))
        self.assertEqual(Nonentity(), map2(Some(1), Nonentity(), (lambda a, b: a + b)))

    def test_sequence(self) -> None:
        self.assertEqual(Some(list_of(1, 2, 3)), sequence(list_of(Some(1), Some(2), Some(3))))

    def test_traverse(self) -> None:
        xs = traverse(list_of(1, 2, 3, 4), lambda it: Some(it / 2.0))
        self.assertEqual(Some(list_of(0.5, 1.0, 1.5, 2.0)), xs)
