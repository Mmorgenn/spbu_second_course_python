from typing import Any, Generic, Protocol, TypeVar


class ArithmeticAvailable(Protocol):
    def __eq__(self, other: Any) -> bool:
        pass

    def __add__(self, other: Any) -> Any:
        pass

    def __sub__(self, other: Any) -> Any:
        pass

    def __mul__(self, other: Any) -> Any:
        pass


T = TypeVar("T", bound=ArithmeticAvailable)


class ArityError(Exception):
    pass


class Vector(Generic[T]):
    def __init__(self, vector: list[T]) -> None:
        self.elements: list[T] = vector

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vector) and len(self) == len(other) and self.elements == other.elements

    def __str__(self) -> str:
        return f"Vector({self.elements})"

    def __len__(self) -> int:
        return len(self.elements)

    def is_null(self) -> bool:
        return all(not i for i in self.elements)

    def get_arity_op(self, other: object) -> int:
        if not isinstance(other, Vector):
            raise TypeError(f"Unsupported operand type(s): 'Vector' and {type(other)}")
        arity = len(self)
        if not arity == len(other):
            raise ArityError("Wrong arity of vectors!")
        return arity

    def mul_vectors(self, other: object) -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError(f"Unsupported operand type(s): 'Vector' and {type(other)}")
        if len(self) != 3 or len(other) != 3:
            raise ArityError("Wrong arity of vectors! Only 3 arity is supported!")
        return Vector(
            [
                self.elements[1] * other.elements[2] - self.elements[2] * other.elements[1],
                self.elements[2] * other.elements[0] - self.elements[0] * other.elements[2],
                self.elements[0] * other.elements[1] - self.elements[1] * other.elements[0],
            ]
        )

    def __add__(self, other: "Vector") -> "Vector":
        arity = self.get_arity_op(other)
        return Vector([self.elements[i] + other.elements[i] for i in range(arity)])

    def __sub__(self, other: "Vector") -> "Vector":
        arity = self.get_arity_op(other)
        return Vector([self.elements[i] - other.elements[i] for i in range(arity)])

    def __mul__(self, other: "Vector") -> int:
        arity = self.get_arity_op(other)
        return sum([self.elements[i] * other.elements[i] for i in range(arity)])
