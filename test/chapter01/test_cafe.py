from chapter01.cafe import buy_coffees, CreditCard, Charge, coalesce, Coffee


def test_buy_coffees() -> None:
    coffees, charge = buy_coffees(CreditCard(), 2)
    assert coffees == [Coffee(price=5.0), Coffee(price=5.0)]
    assert charge == Charge(CreditCard(), 10.0)


def test_coalesce() -> None:
    charges = [Charge(CreditCard(), 5.0), Charge(CreditCard(), 2.0)]
    assert coalesce(charges) == [Charge(CreditCard(), 7.0)]
