from unittest import TestCase

from chapter03.List import list_of
from chapter05.stream import stream


class TestStream(TestCase):
    def test_take(self) -> None:
        xs = stream(1, 2, 3, 4, 5).take(3).to_list()
        self.assertEqual(list_of(1, 2, 3), xs)

    def test_drop(self) -> None:
        xs = stream(1, 2, 3, 4, 5).drop(2).to_list()
        self.assertEqual(list_of(3, 4, 5), xs)

    def test_take_while(self) -> None:
        xs = stream(1, 2, 3, 4, 5, 6).take_while(lambda it: it < 5).to_list()
        self.assertEqual(list_of(1, 2, 3, 4), xs)

    def test_fold_right(self) -> None:
        total = stream(1, 2, 3, 4).fold_right(lambda: 0, (lambda a, b: a + b()))
        self.assertEqual(10, total)

    def test_map(self) -> None:
        self.assertEqual(list_of(3, 4, 5), stream(1, 2, 3).map(lambda it: it + 2).to_list())

    def test_exists(self) -> None:
        self.assertEqual(True, stream(1, 2, 3, 4).exists(lambda it: it == 4))
        self.assertEqual(False, stream(1, 2, 3, 4).exists(lambda it: it == 5))

    def test_forAll(self) -> None:
        self.assertEqual(True, stream(1, 2, 3, 4).for_all(lambda it: it < 5))
        self.assertEqual(False, stream(1, 2, 3, 4).for_all(lambda it: it < 4))

    def test_filter(self) -> None:
        self.assertEqual(list_of(1, 3), stream(1, 2, 3).filter(lambda it: it % 2 == 1).to_list())

    def test_append(self) -> None:
        self.assertEqual(list_of(1, 2, 3, 4), stream(1, 2).append(lambda: stream(3, 4)).to_list())

    def test_flatMap(self) -> None:
        self.assertEqual(list_of(1, 2, 3), stream("1", "2", "3").flat_map(lambda it: stream(int(it))).to_list())
