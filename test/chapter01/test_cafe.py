from chapter01.cafe import buy_coffees, CreditCard


def test_buy_coffees() -> None:
    coffees, charge = buy_coffees(CreditCard(), 2)
    # print(f'Coffees: {coffees}, type: {type(coffees)}')
    # print(f'Charges: {charge}, type: {type(charge)}')
    assert coffees is not None
