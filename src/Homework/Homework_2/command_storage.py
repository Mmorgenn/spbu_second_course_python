from abc import ABC, ABCMeta, abstractmethod
from collections import deque
from collections.abc import MutableMapping as M
from collections.abc import MutableSequence as S
from typing import Any

from src.Homework.Homework_1.registry import Registry

ACTIONS = Registry["Action"]()


class Action(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, data: S | M) -> None:
        raise NotImplementedError

    @abstractmethod
    def undo(self, data: S | M) -> None:
        raise NotImplementedError


class ActionSequence(Action, ABC):
    @abstractmethod
    def _apply(self, data: S) -> None:
        raise NotImplementedError

    @abstractmethod
    def _undo(self, data: S) -> None:
        raise NotImplementedError

    def apply(self, data: S | M) -> None:
        if not isinstance(data, S):
            raise AttributeError("This collection is immutable or not sequence")
        self._apply(data)

    def undo(self, data: S | M) -> None:
        if not isinstance(data, S):
            raise AttributeError("This collection is immutable or not sequence")
        self._undo(data)


class ActionMapping(Action, ABC):
    @abstractmethod
    def _apply(self, data: M) -> None:
        raise NotImplementedError

    @abstractmethod
    def _undo(self, data: M) -> None:
        raise NotImplementedError

    def apply(self, data: S | M) -> None:
        if not isinstance(data, M):
            raise AttributeError("This collection is immutable or not mapping")
        self._apply(data)

    def undo(self, data: S | M) -> None:
        if not isinstance(data, M):
            raise AttributeError("This collection is immutable or not mapping")
        self._undo(data)


class ActionUniversal(Action, ABC):
    @abstractmethod
    def _apply(self, data: S | M) -> None:
        raise NotImplementedError

    def apply(self, data: S | M) -> None:
        if isinstance(data, S) and hasattr(self, "validation_keys"):
            for key in self.validation_keys:
                self.has_index(data, key)
        elif isinstance(data, M) and hasattr(self, "validation_keys"):
            for key in self.validation_keys:
                self.has_key(data, key)
        self._apply(data)

    @staticmethod
    def has_index(data: S | M, key: Any) -> None:
        if type(key) is not int:
            raise KeyError(f"Index must be integer")
        if not (key == 0 or 0 <= key < len(data)):
            raise IndexError("Index out of range")

    @staticmethod
    def has_key(data: M, key: Any) -> None:
        if key not in data.keys():
            raise KeyError("There is no such key")


@ACTIONS.register("first_insert")
class FirstInsertAction(ActionSequence):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def _apply(self, data: S) -> None:
        data.insert(0, self.value)

    def _undo(self, data: S) -> None:
        del data[0]


@ACTIONS.register("last_insert")
class LastInsertAction(ActionSequence):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def _apply(self, data: S) -> None:
        data.append(self.value)

    def _undo(self, data: S) -> None:
        data.pop()


@ACTIONS.register("first_del")
class FirstDelAction(ActionSequence):
    def __init__(self) -> None:
        self.value: int | None = None

    def _apply(self, data: S) -> None:
        if len(data) == 0:
            raise IndexError("Data is empty")
        self.value = data[0]
        del data[0]

    def _undo(self, data: S) -> None:
        data.insert(0, self.value)


@ACTIONS.register("last_del")
class LastDelAction(ActionSequence):
    def __init__(self) -> None:
        self.value: int | None = None

    def _apply(self, data: S) -> None:
        if len(data) == 0:
            raise IndexError("Data is empty")
        self.value = data.pop()

    def _undo(self, data: S) -> None:
        data.append(self.value)


@ACTIONS.register("add_value")
class AddValueAction(ActionUniversal):
    def __init__(self, key: Any, value: int) -> None:
        self.key: Any = key
        self.value: int = value
        self.validation_keys: list[Any] = [key]

    def _apply(self, data: S | M) -> None:
        data[self.key] += self.value

    def undo(self, data: S | M) -> None:
        data[self.key] -= self.value


@ACTIONS.register("subtract_value")
class SubtractValueAction(ActionUniversal):
    def __init__(self, key: Any, value: int) -> None:
        self.key: Any = key
        self.value: int = value
        self.validation_keys: list[Any] = [key]

    def _apply(self, data: S | M) -> None:
        data[self.key] -= self.value

    def undo(self, data: S | M) -> None:
        data[self.key] += self.value


@ACTIONS.register("move")
class MoveAction(ActionUniversal):
    def __init__(self, key_from: Any, key_to: Any) -> None:
        self.key_from: Any = key_from
        self.key_to: Any = key_to
        self.validation_keys: list[Any] = [key_from, key_to]

    def _apply(self, data: S | M) -> None:
        data[self.key_from], data[self.key_to] = data[self.key_to], data[self.key_from]

    def undo(self, data: S | M) -> None:
        data[self.key_to], data[self.key_from] = data[self.key_from], data[self.key_to]


@ACTIONS.register("change_value")
class ChangeValueAction(ActionUniversal):
    def __init__(self, key: Any, new_value: int) -> None:
        self.key: Any = key
        self.new_value: int = new_value
        self.old_value: int | None = None
        self.validation_keys: list[Any] = [key]

    def _apply(self, data: S | M) -> None:
        self.old_value = data[self.key]
        data[self.key] = self.new_value

    def undo(self, data: S | M) -> None:
        data[self.key] = self.old_value


@ACTIONS.register("insert")
class InsertAction(ActionUniversal):
    def __init__(self, key: Any, value: int) -> None:
        self.key = key
        self.value = value

    def _apply(self, data: S | M) -> None:
        if isinstance(data, S):
            self.has_index(data, self.key)
            data.insert(self.key, self.value)
            return
        data[self.key] = self.value

    def undo(self, data: S | M) -> None:
        del data[self.key]


@ACTIONS.register("del")
class DelAction(ActionUniversal):
    def __init__(self, key: Any) -> None:
        self.key: Any = key
        self.value: int | None = None
        self.validation_keys: list[Any] = [key]

    def _apply(self, data: S | M) -> None:
        self.value = data[self.key]
        del data[self.key]

    def undo(self, data: S | M) -> None:
        if isinstance(data, S):
            data.insert(self.key, self.value)
            return
        data[self.key] = self.value


@ACTIONS.register("change_key")
class ChangeKeyAction(ActionMapping):
    def __init__(self, key_from: Any, key_to: Any) -> None:
        self.key_from = key_from
        self.key_to = key_to
        self.value: int | None = None

    def _apply(self, data: M) -> None:
        if self.key_from not in data.keys():
            raise KeyError(f"There is no such key as '{self.key_from}'")
        if self.key_to in data.keys():
            raise KeyError(f"There is such key as '{self.key_to}'")
        self.value = data.pop(self.key_from)
        data[self.key_to] = self.value

    def _undo(self, data: M) -> None:
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
