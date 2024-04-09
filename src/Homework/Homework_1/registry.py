from collections import Counter, OrderedDict
from typing import Callable, Generic, Mapping, MutableMapping, Type, TypeVar

C = TypeVar("C")


class Registry(Generic[C]):
    def __init__(self, default: Type[C] | None = None) -> None:
        self.storage: dict[str, Type[C]] = {}
        self.default: Type[C] | None = default

    def register(self, class_name: str) -> Callable[[Type[C]], Type[C]]:
        """Method for registering the interface"""

        if self.storage.get(class_name, None) is not None:
            raise ValueError(f"{class_name} is already registered!")

        def decorator(cls: Type[C]) -> Type[C]:
            self.storage[class_name] = cls
            return cls

        return decorator

    def dispatch(self, class_name: str) -> Type[C]:
        """Method of dispatching the registered interface"""

        class_registered = self.storage.get(class_name, None)

        if class_registered is not None:
            return class_registered
        if self.default is not None:
            return self.default
        raise ValueError(f"{class_name} isn't registered!")


if __name__ == "__main__":
    logs_default = Registry[Mapping](default=dict)
    logs = Registry[Mapping]()
    logs_default.register("very_useful")(Counter)
    logs.register("very_useful")(Counter)
    logs_default.register("not_useful")(OrderedDict)
    logs.register("not_useful")(OrderedDict)
    user_input = str(input(f"Current logs: {logs_default.storage}\nInput name for dispatching: "))
    print(f"With default: {logs_default.dispatch(user_input)}")
    try:
        print(f"Without: {logs.dispatch(user_input)}")
    except ValueError as e:
        print(f"Without: (Error) - {e}")
