import json
from dataclasses import asdict, dataclass
from typing import Any, Generic, Type, TypeVar

T = TypeVar("T", bound="ORM")


class JsonError(Exception):
    pass


class ORMDescriptor(Generic[T]):
    def __init__(self, key: str) -> None:
        self.key = key
        self.value = None

    def __get__(self, instance: T, owner: Type[T]) -> None:
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
    def __new__(cls, name: Any, bases: Any, dct: dict) -> type:
        branches = {}
        attrs = []
        for field_name, field_type in dct["__annotations__"].items():
            if issubclass(field_type, ORM):
                branches[field_name] = field_type
            else:
                attrs.append(field_name)
            dct[field_name] = None

        dct["__branches__"] = branches
        dct["__attrs__"] = attrs
        return super().__new__(cls, name, bases, dct)


@dataclass
class ORM:
    @classmethod
    def parse_json(cls: Type[T], data: dict) -> T:
        for name in getattr(cls, "__attrs__", []):
            setattr(cls, name, ORMDescriptor(name))
        setattr(cls, "__data__", data)
        new_cls = cls()
        for name, bcls in getattr(cls, "__branches__", {}).items():
            small_data = data.get(name, None)
            if small_data is None:
                raise JsonError(f"The {name} is missing in json data")
            setattr(new_cls, name, bcls.parse_json(small_data))

        return new_cls

    def dump(self) -> str:
        return json.dumps(asdict(self))
