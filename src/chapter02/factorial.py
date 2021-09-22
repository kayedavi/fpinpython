from TailCall import Return, Suspend, TailCall


def factorial(n: int) -> int:
    def go(x: int, acc: int) -> TailCall[int]:
        if x <= 0:
            return Return(acc)
        else:
            return Suspend(lambda: go(x - 1, x * acc))

    return go(n, 1).eval()
