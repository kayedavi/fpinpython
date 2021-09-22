from __future__ import annotations

from typing import TypeVar, Callable, Optional, Any, Iterator, Iterable, Sequence, ParamSpec

T = ParamSpec('T')
R = TypeVar('R')
K = TypeVar('K')
V = TypeVar('V')


class KList(list[T]):
    def __init__(self, *elements: T.args) -> None:
        super().__init__(list(elements))

    def map(self, transform: Callable[[T], R]) -> KList[R]:
        ret_list = KList()
        for x in self:
            y = transform(x)
            ret_list.append(y)
        return ret_list

    def flat_map(self, transform: Callable[[T], KList[R]]) -> KList[R]:
        ret_list = KList()
        for x in self:
            xs = transform(x)
            ret_list += xs
        return ret_list

    def filter(self, predicate: Callable[[T], bool]) -> KList[T]:
        ret_list = KList()
        for x in self:
            if predicate(x):
                ret_list.append(x)
        return ret_list

    def group_by(self, key_selector: Callable[[T], R]) -> dict[R, KList[T]]:
        ret_dict: dict[R, KList[T]] = {}
        for x in self:
            key = key_selector(x)
            existing_list = ret_dict.get(key)
            if existing_list:
                existing_list.append(x)
            else:
                ret_dict[key] = KList(x)
        return ret_dict

    def size(self) -> int:
        return len(self)

    def contains_all(self, elements: [T]) -> bool:
        return all(elem in self for elem in elements)

    def is_empty(self) -> bool:
        return not self

    def reversed(self) -> KList[T]:
        reversed_list = self.copy()
        reversed_list.reverse()
        return KList(*reversed_list)

    def get_or_none(self, index: int) -> Optional[T]:
        if 0 <= index < len(self):
            return self[index]
        else:
            return None

    def get_or_else(self, index: int, default_value: Callable[[], T]) -> T:
        if 0 <= index < len(self):
            return self[index]
        else:
            return default_value()

    def for_each(self, action: Callable[[T], None]) -> None:
        for x in self:
            action(x)

    def fold(self, initial: R, operation: Callable[[R, T], R]) -> R:
        acc = initial
        for x in self:
            acc = operation(acc, x)
        return acc

    def fold_right(self, initial: R, operation: Callable[[T, R], R]) -> R:
        acc = initial
        for x in self.reversed():
            acc = operation(x, acc)
        return acc

    def __add__(self, other: [T]) -> KList:
        return KList(*super().__add__(other))

    def contains(self, element: T) -> bool:
        return element in self

    def index_of(self, element: T) -> int:
        try:
            return self.index(element)
        except ValueError:
            return -1

    def iterator(self) -> Iterator[T]:
        return iter(self)

    def last_index_of(self, element: T) -> int:
        for n in range(self.size() - 1, -1, -1):
            if self[n] == element:
                return n
        return -1

    def sub_list(self, from_index: int, to_index: int) -> KList[T]:
        return self[from_index:to_index]

    def indices(self) -> range:
        return range(0, len(self))

    def last_index(self) -> int:
        return len(self) - 1

    def all(self, predicate: Callable[[T], bool]) -> bool:
        for x in self:
            if not predicate(x):
                return False
        return True

    def any(self, predicate: Callable[[T], bool]) -> bool:
        for x in self:
            if predicate(x):
                return True
        return False

    def as_iterable(self) -> Iterable[T]:
        return self

    def as_reversed(self) -> KList[T]:
        return self.reversed()

    def as_sequence(self) -> Sequence[T]:
        return self

    def associate(self, transform: Callable[[T], (K, V)]) -> dict[K, V]:
        associates = {}
        for x in self:
            key, value = transform(x)
            associates[key] = value
        return associates


def also(a: T, f: Callable[[T], None]) -> T:
    f(a)
    return a


def also_optional(a: Optional[T], f: Callable[[T], None]) -> T:
    if a is not None:
        f(a)
    return a


def let(a: T, f: Callable[[T], R]) -> R:
    return f(a)


def take_if(a: T, predicate: Callable[[T], bool]) -> Optional[T]:
    if predicate(a):
        return a
    else:
        return None


def take_unless(a: T, predicate: Callable[[T], bool]) -> Optional[T]:
    if predicate(a):
        return None
    else:
        return a


def TODO() -> Any:
    raise NotImplementedError()
