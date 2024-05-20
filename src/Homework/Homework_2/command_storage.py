from abc import ABC, ABCMeta, abstractmethod
from collections import abc, deque
from typing import Any, Generic, TypeVar

from src.Homework.Homework_1.registry import Registry

S = TypeVar("S", bound=abc.MutableSequence)
M = TypeVar("M", bound=abc.MutableMapping)
ACTIONS = Registry["Action"]()


class Action(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, data: S | M) -> None:
        pass

    @abstractmethod
    def undo(self, data: S | M) -> None:
        pass


class ActionS(Action, ABC):
    @staticmethod
    def check_index(data: S, index: int) -> bool:
        if type(index) is not int:
            raise KeyError(f"Index '{index}' must be integer")
        return index == 0 or 0 <= index < len(data)


class ActionM(Action, ABC):
    @staticmethod
    def check_has_key(data: M, key: Any) -> bool:
        return data.get(key, None) is not None


class ActionSM(Action, ABC):
    @staticmethod
    def check_index(data: S, index: int) -> bool:
        if type(index) is not int:
            raise KeyError(f"Index '{index}' must be integer")
        return index == 0 or 0 <= index < len(data)

    @staticmethod
    def check_has_key(data: M, key: Any) -> bool:
        return data.get(key, None) is not None

    @staticmethod
    def check_error(data: S | M, key: Any) -> None:
        if isinstance(data, abc.MutableSequence):
            if not ActionSM.check_index(data, key):
                raise IndexError("Index out of range")
            return
        if isinstance(data, abc.MutableMapping):
            if not ActionSM.check_has_key(data, key):
                raise KeyError(f"There is no such key as '{key}'")
            return
        raise AttributeError("This collection is immutable or not sequence/mapping")


@ACTIONS.register("first_insert")
class FirstInsertAction(ActionS):
    def __init__(self, value: int) -> None:
        self.value = value

    def apply(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableSequence):
            raise AttributeError("This collection is immutable or not sequence")
        data.insert(0, self.value)

    def undo(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableSequence):
            raise AttributeError("This collection is immutable or not sequence")
        del data[0]


@ACTIONS.register("last_insert")
class LastInsertAction(ActionS):
    def __init__(self, value: int) -> None:
        self.value = value

    def apply(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableSequence):
            raise AttributeError("This collection is immutable or not sequence")
        data.append(self.value)

    def undo(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableSequence):
            raise AttributeError("This collection is immutable or not sequence")
        data.pop()


@ACTIONS.register("first_del")
class FirstDelAction(ActionS):
    def __init__(self) -> None:
        self.value: int | None = None

    def apply(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableSequence):
            raise AttributeError("This collection is immutable or not sequence")
        if len(data) == 0:
            raise IndexError("Data is empty")
        self.value = data[0]
        del data[0]

    def undo(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableSequence):
            raise AttributeError("This collection is immutable or not sequence")
        data.insert(0, self.value)


@ACTIONS.register("last_del")
class LastDelAction(ActionS):
    def __init__(self) -> None:
        self.value: int | None = None

    def apply(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableSequence):
            raise AttributeError("This collection is immutable or not sequence")
        if len(data) == 0:
            raise IndexError("Data is empty")
        self.value = data.pop()

    def undo(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableSequence):
            raise AttributeError("This collection is immutable or not sequence")
        data.append(self.value)


@ACTIONS.register("add_value")
class AddValueAction(ActionSM):
    def __init__(self, key: Any, value: int) -> None:
        self.key = key
        self.value = value

    def apply(self, data: S | M) -> None:
        self.check_error(data, self.key)
        data[self.key] += self.value

    def undo(self, data: S | M) -> None:
        data[self.key] -= self.value


@ACTIONS.register("subtract_value")
class SubtractValueAction(ActionSM):
    def __init__(self, key: Any, value: int) -> None:
        self.key = key
        self.value = value

    def apply(self, data: S | M) -> None:
        self.check_error(data, self.key)
        data[self.key] -= self.value

    def undo(self, data: S | M) -> None:
        data[self.key] += self.value


@ACTIONS.register("move")
class MoveAction(ActionSM):
    def __init__(self, key_from: Any, key_to: Any) -> None:
        self.key_from = key_from
        self.key_to = key_to

    def apply(self, data: S | M) -> None:
        self.check_error(data, self.key_from)
        self.check_error(data, self.key_to)
        # Swap two numbers
        data[self.key_from], data[self.key_to] = data[self.key_to], data[self.key_from]

    def undo(self, data: S | M) -> None:
        # Swap two numbers
        data[self.key_to], data[self.key_from] = data[self.key_from], data[self.key_to]


@ACTIONS.register("change_value")
class ChangeValueAction(ActionSM):
    def __init__(self, key: Any, new_value: int) -> None:
        self.key = key
        self.new_value = new_value
        self.old_value: int | None = None

    def apply(self, data: S | M) -> None:
        self.check_error(data, self.key)
        self.old_value = data[self.key]
        data[self.key] = self.new_value

    def undo(self, data: S | M) -> None:
        data[self.key] = self.old_value


@ACTIONS.register("insert")
class InsertAction(ActionSM):
    def __init__(self, key: Any, value: int) -> None:
        self.key = key
        self.value = value

    def apply(self, data: S | M) -> None:
        if isinstance(data, abc.MutableSequence):
            if not self.check_index(data, self.key):
                raise IndexError("Index out of range")
            data.insert(self.key, self.value)
            return
        data[self.key] = self.value

    def undo(self, data: S | M) -> None:
        del data[self.key]


@ACTIONS.register("del")
class DelAction(ActionSM):
    def __init__(self, key: Any) -> None:
        self.key = key
        self.value: int | None = None

    def apply(self, data: S | M) -> None:
        self.check_error(data, self.key)
        self.value = data[self.key]
        del data[self.key]

    def undo(self, data: S | M) -> None:
        if isinstance(data, abc.MutableSequence):
            data.insert(self.key, self.value)
            return
        data[self.key] = self.value


@ACTIONS.register("change_key")
class ChangeKeyAction(ActionM):
    def __init__(self, key_from: Any, key_to: Any) -> None:
        self.key_from = key_from
        self.key_to = key_to
        self.value: int | None = None

    def apply(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableMapping):
            raise AttributeError("This collection is immutable or not mapping")
        if not self.check_has_key(data, self.key_from):
            raise KeyError(f"There is no such key as '{self.key_from}'")
        if self.check_has_key(data, self.key_to):
            raise KeyError(f"There is such key as '{self.key_to}'")
        self.value = data.pop(self.key_from)
        data[self.key_to] = self.value

    def undo(self, data: S | M) -> None:
        if not isinstance(data, abc.MutableMapping):
            raise AttributeError("This collection is immutable or not mapping")
        del data[self.key_to]
        data[self.key_from] = self.value


class PCS(Generic[S, M]):
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
