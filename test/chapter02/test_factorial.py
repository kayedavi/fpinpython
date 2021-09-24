from chapter02.factorial import factorial


def test_factorial() -> None:
    assert 1 == factorial(1)
    assert 2 == factorial(2)
    assert 6 == factorial(3)
    assert 24 == factorial(4)
    assert 120 == factorial(5)
