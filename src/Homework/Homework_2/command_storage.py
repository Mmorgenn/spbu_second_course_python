from abc import ABC, ABCMeta, abstractmethod
from collections import deque
from collections.abc import MutableMapping as M
from collections.abc import MutableSequence as S
from typing import Any, Generic, TypeVar

from src.Homework.Homework_1.registry import Registry

T = TypeVar("T")

ACTIONS = Registry["Action"]()


class Action(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def apply(self, data: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def undo(self, data: T) -> None:
        raise NotImplementedError


@ACTIONS.register("first_insert <sequence>")
class FirstInsertAction(Action[S]):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def apply(self, data: S) -> None:
        data.insert(0, self.value)

    def undo(self, data: S) -> None:
        del data[0]


@ACTIONS.register("last_insert <sequence>")
class LastInsertAction(Action[S]):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def apply(self, data: S) -> None:
        data.append(self.value)

    def undo(self, data: S) -> None:
        data.pop()


@ACTIONS.register("first_del <sequence>")
class FirstDelAction(Action[S]):
    def __init__(self) -> None:
        self.value: int | None = None

    def apply(self, data: S) -> None:
        if len(data) == 0:
            raise IndexError("Data is empty")
        self.value = data[0]
        del data[0]

    def undo(self, data: S) -> None:
        data.insert(0, self.value)


@ACTIONS.register("last_del <sequence>")
class LastDelAction(Action[S]):
    def __init__(self) -> None:
        self.value: int | None = None

    def apply(self, data: S) -> None:
        if len(data) == 0:
            raise IndexError("Data is empty")
        self.value = data.pop()

    def undo(self, data: S) -> None:
        data.append(self.value)


@ACTIONS.register("add_value <sequence>")
class AddValueAction(Action[S]):
    def __init__(self, index: int, value: int) -> None:
        self.index: Any = index
        self.value: int = value

    def apply(self, data: S) -> None:
        if not (self.index == 0 or 0 <= self.index < len(data)):
            raise IndexError("Index out of range")
        data[self.index] += self.value

    def undo(self, data: S | M) -> None:
        data[self.index] -= self.value


@ACTIONS.register("subtract_value <sequence>")
class SubtractValueAction(Action[S]):
    def __init__(self, index: int, value: int) -> None:
        self.index: int = index
        self.value: int = value

    def apply(self, data: S) -> None:
        data[self.index] -= self.value

    def undo(self, data: S) -> None:
        data[self.index] += self.value


@ACTIONS.register("move <mapping>")
class MoveAction(Action[M]):
    def __init__(self, key_from: Any, key_to: Any) -> None:
        self.key_from: Any = key_from
        self.key_to: Any = key_to

    def apply(self, data: M) -> None:
        if self.key_from not in data.keys() or self.key_to not in data.keys():
            raise KeyError("There is no such key/s")
        data[self.key_from], data[self.key_to] = data[self.key_to], data[self.key_from]

    def undo(self, data: M) -> None:
        data[self.key_to], data[self.key_from] = data[self.key_from], data[self.key_to]


@ACTIONS.register("change_value <mapping>")
class ChangeValueAction(Action[M]):
    def __init__(self, key: Any, new_value: int) -> None:
        self.key: Any = key
        self.new_value: int = new_value
        self.old_value: int | None = None

    def apply(self, data: M) -> None:
        if self.key not in data.keys():
            raise KeyError("There is no such key")
        self.old_value = data[self.key]
        data[self.key] = self.new_value

    def undo(self, data: M) -> None:
        data[self.key] = self.old_value


@ACTIONS.register("insert <sequence>")
class InsertAction(Action[S]):
    def __init__(self, index: int, value: int) -> None:
        self.index = index
        self.value = value

    def apply(self, data: S) -> None:
        if not (self.index == 0 or 0 <= self.index < len(data)):
            raise IndexError("Index out of range")
        data.insert(self.index, self.value)

    def undo(self, data: S) -> None:
        del data[self.index]


@ACTIONS.register("set_value <mapping>")
class SetValueAction(Action[M]):
    def __init__(self, key: Any, value: int) -> None:
        self.key = key
        self.value = value

    def apply(self, data: M) -> None:
        if self.key in data.keys():
            raise KeyError("Such key is already exist")
        data[self.key] = self.value

    def undo(self, data: M) -> None:
        del data[self.key]


@ACTIONS.register("pop <sequence>")
class PopAction(Action[S]):
    def __init__(self, index: int) -> None:
        self.index: Any = index
        self.value: int | None = None

    def apply(self, data: S) -> None:
        if not (self.index == 0 or 0 <= self.index < len(data)):
            raise IndexError("Index out of range")
        self.value = data[self.index]
        del data[self.index]

    def undo(self, data: S) -> None:
        data.insert(self.index, self.value)


@ACTIONS.register("del <mapping>")
class DelAction(Action[M]):
    def __init__(self, key: Any) -> None:
        self.key: Any = key
        self.value: int | None = None

    def apply(self, data: M) -> None:
        if self.key not in data.keys():
            raise KeyError("There is no such key")
        self.value = data[self.key]
        del data[self.key]

    def undo(self, data: M) -> None:
        data[self.key] = self.value


@ACTIONS.register("change_key <mapping>")
class ChangeKeyAction(Action[M]):
    def __init__(self, key_from: Any, key_to: Any) -> None:
        self.key_from = key_from
        self.key_to = key_to
        self.value: int | None = None

    def apply(self, data: M) -> None:
        if self.key_from not in data.keys():
            raise KeyError(f"There is no such key as '{self.key_from}'")
        if self.key_to in data.keys():
            raise KeyError(f"There is such key as '{self.key_to}'")
        self.value = data.pop(self.key_from)
        data[self.key_to] = self.value

    def undo(self, data: M) -> None:
        del data[self.key_to]
        data[self.key_from] = self.value


class PerformedCommandStorage:
    def __init__(self, data: S | M) -> None:
        self.data = data
        self.storage_actions: list[Action] = []

    def apply_action(self, action: Action) -> None:
        action.apply(self.data)
        self.storage_actions.append(action)

    def undo_action(self) -> None:
        if not self.storage_actions:
            raise ValueError("There are no any actions for undo")
        action = self.storage_actions.pop()
        action.undo(self.data)


print(issubclass(PopAction, Action))
