from unittest import TestCase

from chapter02.factorial import factorial


class Test(TestCase):
    def test_factorial(self) -> None:
        assert 1 == factorial(1)
        assert 2 == factorial(2)
        assert 6 == factorial(3)
        assert 24 == factorial(4)
        self.assertEqual(120, factorial(5))
