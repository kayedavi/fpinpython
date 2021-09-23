from typing import TypeVar, Generic
from unittest import TestCase

from chapter04.either import Right, Left, Try, Either

A = TypeVar('A')
E = TypeVar('E')


class TestEither(TestCase, Generic[E, A]):
    def test_map(self) -> None:
        exception = Exception('Error')
        self.assertEqual(Left(exception), Left(exception).map(lambda it: it + 1))
        self.assertEqual(Right(5), Right(4).map(lambda it: it + 1))

    def test_Try(self) -> None:
        # self.assertEqual(Right(3), Try(lambda: 4 / 2).map(lambda it: it + 1))
        Try(lambda: 2 / 1).map(lambda x: x + 6).map(lambda x: print(f'Success: {x}'))
        Try(lambda: 2 / 0) \
            .map(lambda x: x + 6) \
            .map(lambda x: print(f'Success: {x}')) \
            .or_else(lambda: Right(6)) \
            .map(lambda x: print(f'Failure: {x}'))
        # left = Try(lambda: 4 / 0).map(lambda it: it + 1)
        # self.assertLeft(left, ZeroDivisionError, 'division by zero')

    def test_flatMap(self) -> None:
        self.assertEqual(Right(4), Right(2).flat_map(lambda it: Right(it + 2)))
        left1 = Left(Exception('Blah')).flat_map(lambda it: Right(it + 2))
        self.assertLeft(left1, Exception, 'Blah')
        left2 = Right(2).flat_map(lambda _: Left(Exception('Blah')))
        self.assertLeft(left2, Exception, 'Blah')

    def test_orElse(self) -> None:
        self.assertEqual(Right(3), Right(3).or_else(lambda _: Right(7)))
        self.assertEqual(Right(7), Left(Exception('Blah')).or_else(lambda: Right(7)))

    def test_map2(self) -> None:
        self.assertEqual(Right(3), Right(1).map2(Right(2), (lambda x, y: x + y)))
        left1 = Right(1).map2(Left(Exception('Blah')), (lambda x, y: x + y))
        self.assertLeft(left1, Exception, 'Blah')
        left2 = Left(Exception('Blah')).map2(Right(1), (lambda x, y: x + y))
        self.assertLeft(left2, Exception, 'Blah')
        left3 = Left(Exception('Blah')).map2(Left(Exception('Newp')), (lambda x, y: x + y))
        self.assertLeft(left3, Exception, 'Blah')

    def assertLeft(self, left: Either[Exception, A], error_type, msg: str) -> None:
        match left:
            case Left(e):
                self.assertEqual(error_type, type(e))
                self.assertEqual(msg, e.args[0])
            case Right(_):
                self.fail()
