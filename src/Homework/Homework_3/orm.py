from dataclasses import asdict, dataclass
from json import dumps
from typing import Any, Generic, Type, TypeVar

T = TypeVar("T", bound="ORM")


class JsonError(Exception):
    pass


class CustomDescriptor(Generic[T]):
    def __init__(self, default: str) -> None:
        self.default = default

    def __get__(self, instance: T, owner: Type[T]) -> Any:
        if not hasattr(instance, "data"):
            raise JsonError("Json data is missing")
        value = getattr(instance, f"_{self.default}", self.default)
        if value is None:
            new_value = instance.data.get(self.default, None)
            if new_value:
                setattr(instance, self.default, new_value)
                return new_value
            raise JsonError(f"The {self.default} is missing in json data")
        return value

    def __set__(self, instance: T, value: Any) -> None:
        setattr(instance, f"_{self.default}", value)


@dataclass
class ORM(Generic[T]):
    @classmethod
    def apply_descriptor(cls: Type[T]) -> Type[T]:
        for name, field in cls.__annotations__.items():
            setattr(cls, name, CustomDescriptor(name))
        return cls

    @classmethod
    def upload_dict(cls: Type[T], data: dict) -> T:
        new_cls = cls.apply_descriptor()
        result = new_cls()
        setattr(result, "data", data)
        return result

    def dump(self) -> str | None:
        try:
            json = asdict(self)
        except TypeError:
            raise TypeError("This is not dataclass")
        return dumps(json)
