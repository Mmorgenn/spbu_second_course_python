import json
from dataclasses import asdict, dataclass
from typing import Any, Generic, Type, TypeVar

T = TypeVar("T")


class JsonError(Exception):
    pass


class ORMDescriptor(Generic[T]):
    def __init__(self, key: str) -> None:
        self.key = key
        self.value = None

    def __get__(self, instance: T, owner: Type[T]) -> None:
        if instance is None:
            return self
        if not hasattr(instance, "__data__"):
            raise JsonError("Json data is missing")

        if self.value is None:
            new_value = instance.__data__.get(self.key, None)
            if new_value is None:
                raise JsonError(f"The {self.key} is missing in json data")
            self.value = new_value
        return self.value

    def __set__(self, instance: T, value: Any) -> None:
        self.value = value


class ORMMeta(type):
    def __init__(cls, name: str, bases: Any, dct: dict) -> None:
        branches = dict()
        for field_name, field_type in cls.__annotations__.items():
            if type(field_type) is ORMMeta:
                branches[field_name] = field_type
                setattr(cls, field_name, None)
            else:
                setattr(cls, field_name, ORMDescriptor(field_name))
        setattr(cls, "__branches__", branches)
        super(ORMMeta, cls).__init__(name, bases, dct)

    def parse_json(cls: Type[T], data: dict) -> T:
        setattr(cls, "__data__", data)
        obj = cls(*[None for _ in range(len(cls.__annotations__.keys()))])
        for branch_name, branch_class in getattr(cls, "__branches__", {}).items():
            small_data = data.get(branch_name, None)
            if small_data is None:
                raise JsonError(f"The {branch_name} is missing in json data")
            setattr(obj, branch_name, branch_class.parse_json(small_data))
        return obj


def dump_dataclass(obj: Any) -> str:
    return json.dumps(asdict(obj))
