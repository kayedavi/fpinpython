from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

T = TypeVar('T')


class TailCall(Generic[T], ABC):
    def eval(self) -> T:
        tail_rec = self
        while isinstance(tail_rec, Suspend):
            tail_rec = tail_rec.resume()
        return tail_rec.eval()


@dataclass
class Return(TailCall[T]):
    t: T

    def eval(self) -> T:
        return self.t


@dataclass
class Suspend(TailCall[T]):
    resume_function: Callable[[], T]

    def resume(self) -> TailCall[T]:
        return self.resume_function()
