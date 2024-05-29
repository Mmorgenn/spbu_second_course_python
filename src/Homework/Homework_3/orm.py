import json
from dataclasses import asdict, dataclass
from typing import Any, Generic, List, Type, TypeVar, get_args, get_origin, get_type_hints

T = TypeVar("T")


class JsonError(Exception):
    pass


class ORMMeta(type):
    def __init__(cls, name: str, bases: Any, dct: dict) -> None:
        for field_name, field_type in cls.__annotations__.items():
            if hasattr(field_type, "__args__") and isinstance(field_type.__args__[0], ORMMeta):
                setattr(cls, field_name, BranchDescriptor(field_name, field_type.__args__[0]))
            elif isinstance(field_type, ORMMeta):
                setattr(cls, field_name, BranchDescriptor(field_name, field_type))
            else:
                setattr(cls, field_name, ORMDescriptor(field_name))
        super(ORMMeta, cls).__init__(name, bases, dct)

    def parse_json(cls: Type[T], data: dict) -> T:
        setattr(cls, "__data__", data)
        return cls()


class ORMDescriptor(Generic[T]):
    def __init__(self, key: str) -> None:
        self.key = key

    def __get__(self, instance: T, owner: Type[T]) -> Any:
        if instance is None:
            return None
        if not hasattr(instance, "__data__"):
            raise JsonError("Json data is missing")

        if not hasattr(instance, f"_{self.key}"):
            if self.key not in instance.__data__.keys():
                raise JsonError(f"The {self.key} is missing in json data")
            value = instance.__data__.get(self.key)
            setattr(instance, f"_{self.key}", value)
            return value
        return getattr(instance, f"_{self.key}")

    def __set__(self, instance: T, value: Any) -> None:
        if value is not None:
            setattr(instance, f"_{self.key}", value)


class BranchDescriptor(Generic[T]):
    def __init__(self, name: str, orm_cls: ORMMeta) -> None:
        self.name = name
        self.orm_cls = orm_cls

    def __get__(self, instance: T, owner: Type[T]) -> Any:
        if instance is None:
            return None
        if not hasattr(instance, "__data__"):
            raise JsonError("Json data is missing")
        if not hasattr(instance, f"_{self.name}"):
            if self.name not in instance.__data__.keys():
                raise JsonError(f"The {self.name} is missing in json data")
            data = instance.__data__.get(self.name)

            if type(data) is list:
                result: list[Any] = []
                for i in range(len(data)):
                    result.append(self.orm_cls.parse_json(data[i]))
                setattr(instance, f"_{self.name}", result)
                return result

            orm: Any = self.orm_cls.parse_json(data)
            setattr(instance, f"_{self.name}", orm)
            return orm

        return getattr(instance, f"_{self.name}")

    def __set__(self, instance: T, value: Any) -> None:
        if value is not None:
            setattr(instance, f"_{self.name}", value)


def dump_dataclass(obj: Any) -> str:
    return json.dumps(asdict(obj))
