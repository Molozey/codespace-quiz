import timeit

_GLOBAL_IDX = 256


class Element:
    def __init__(self, idx: int, ydx: int):
        self._idx = idx
        self._ydx = ydx

    def __hash__(self):
        return id(self)

    def __eq__(self, other: "Element"):
        return (self._idx == other._idx) and (self._ydx == other._ydx)


def main():
    storage = {}
    for _ in range(50_000):
        storage[Element(_GLOBAL_IDX, _)] = _


if __name__ == "__main__":
    result = timeit.timeit(lambda: main(), number=1)
    print(result)
