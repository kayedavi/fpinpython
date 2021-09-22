# First, a findFirst, specialized to `String`.
# Ideally, we could generalize this to work for any `list` type.

from TailCall import TailCall, Return, Suspend


# First, a binary search implementation, specialized to `float`,
# another primitive type in Python, representing 64-bit floating
# point numbers
# Ideally, we could generalize this to work for any `list` type,
# so long as we have some way of comparing elements of the `list`
def binary_search(ds: list[float], key: float) -> int:
    def go(low: int, mid: int, high: int) -> TailCall[int]:
        if low > high:
            return Return(-mid - 1)
        else:
            mid2 = (low + high) // 2
            d = ds[mid2]
            if d == key:
                return Return(mid2)
            elif d > key:
                return Suspend(lambda: go(low, mid2, mid2 - 1))
            else:
                return Suspend(lambda: go(mid2 + 1, mid2, high))

    return go(0, 0, len(ds) - 1).eval()


def find_first(ss: list[str], key: str) -> int:
    def loop(n: int) -> TailCall[int]:
        # If `n` is past the end of the list, return `-1`
        # indicating the key doesn't exist in the list.
        if n >= len(ss):
            return Return(-1)
        # `ss[n]` extracts the n'th element of the list `ss`.
        # If the element at `n` is equal to the key, return `n`
        # indicating that the element appears in the list at that index.
        elif ss[n] == key:
            return Return(n)
        else:
            return Suspend(lambda: loop(n + 1))  # Otherwise increment `n` and keep looking.

    # Start the loop at the first element of the list.
    return loop(0).eval()
