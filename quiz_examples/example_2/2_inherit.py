from abc import ABC


class Basic(ABC):
    def __init__(self, value):
        self._value = value

    def __hash__(self):
        return hash(self._value)


class ClassA(Basic):
    def __init__(self, value):
        super().__init__(value)

    def __hash__(self):
        return super().__hash__()


class ClassB(Basic):
    def __init__(self, value):
        super().__init__(value)


a = ClassA("A")
a2 = ClassA("A")
b = ClassB("A")
print(hash(a), hash(a2), hash(b))

storage = {}

storage[a] = 10
storage[a2] = 20
storage[b] = 30

print(storage)
