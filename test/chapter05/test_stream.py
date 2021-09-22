from unittest import TestCase

from chapter03.List import listOf
from chapter05.stream import stream


class TestStream(TestCase):
    def test_take(self) -> None:
        xs = stream(1, 2, 3, 4, 5).take(3).toList()
        self.assertEqual(listOf(1, 2, 3), xs)

    def test_drop(self) -> None:
        xs = stream(1, 2, 3, 4, 5).drop(2).toList()
        self.assertEqual(listOf(3, 4, 5), xs)

    def test_take_while(self) -> None:
        xs = stream(1, 2, 3, 4, 5, 6).takeWhile(lambda it: it < 5).toList()
        self.assertEqual(listOf(1, 2, 3, 4), xs)

    def test_fold_right(self) -> None:
        total = stream(1, 2, 3, 4).foldRight(lambda: 0, (lambda a, b: a + b()))
        self.assertEqual(10, total)

    def test_map(self) -> None:
        self.assertEqual(listOf(3, 4, 5), stream(1, 2, 3).map(lambda it: it + 2).toList())

    def test_exists(self) -> None:
        self.assertEqual(True, stream(1, 2, 3, 4).exists(lambda it: it == 4))
        self.assertEqual(False, stream(1, 2, 3, 4).exists(lambda it: it == 5))

    def test_forAll(self) -> None:
        self.assertEqual(True, stream(1, 2, 3, 4).forAll(lambda it: it < 5))
        self.assertEqual(False, stream(1, 2, 3, 4).forAll(lambda it: it < 4))

    def test_filter(self) -> None:
        self.assertEqual(listOf(1, 3), stream(1, 2, 3).filter(lambda it: it % 2 == 1).toList())

    def test_append(self) -> None:
        self.assertEqual(listOf(1, 2, 3, 4), stream(1, 2).append(lambda: stream(3, 4)).toList())

    def test_flatMap(self) -> None:
        self.assertEqual(listOf(1, 2, 3), stream("1", "2", "3").flatMap(lambda it: stream(int(it))).toList())
