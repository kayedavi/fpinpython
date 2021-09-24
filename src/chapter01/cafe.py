from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from itertools import groupby


@dataclass(frozen=True)
class CreditCard:
    def charge(self, price: float) -> None:
        pass


@dataclass()
class Coffee:
    price: float = 5.0


@dataclass
class Payments:
    def charge(self, cc: CreditCard, price: float) -> None:
        pass


@dataclass
class Charge:
    cc: CreditCard
    amount: float

    def combine(self, other: Charge) -> Charge:
        if self.cc == other.cc:
            return Charge(self.cc, self.amount + other.amount)
        else:
            raise Exception("Can't combine charges to different cards")


def buy_coffee(cc: CreditCard) -> (Coffee, Charge):
    cup = Coffee()
    return cup, Charge(cc, cup.price)


def buy_coffees(cc: CreditCard, n: int) -> ([Coffee], Charge):
    purchases = [buy_coffee(cc)] * n
    coffees, charges = zip(*purchases)
    return list(coffees), reduce((lambda c1, c2: c1.combine(c2)), charges)


def coalesce(charges: list[Charge]) -> list[Charge]:
    return list(map(lambda x: reduce((lambda c1, c2: c1.combine(c2)), x),
                    [list(chgs) for credit_card, chgs in groupby(charges, lambda charge: charge.cc)]))
