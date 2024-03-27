from dataclasses import dataclass
from typing import Mapping, MutableMapping

import pytest

from src.Homework.Homework_1.registry import *


@dataclass
class TestRegistry:
    logs = Registry[Mapping]()
    logs_arg = Registry[dict](default=dict)
    empty_logs = Registry[MutableMapping]()
    empty_logs_arg = Registry[list](default=list)

    def __post_init__(self):
        @self.logs.register("foo")
        class Foo(Mapping):
            pass

        @self.logs.register("boo")
        class Boo(Mapping):
            pass

        @self.logs.register("doo")
        class Doo(Mapping):
            pass

        @self.logs_arg.register("super_dict")
        class SuperDict(dict):
            pass

        @self.logs_arg.register("slow_dict")
        class SlowDict(dict):
            pass

        class Sui(Mapping):
            pass

        self.mapping_class = Sui


TESTER = TestRegistry()


@pytest.mark.parametrize(
    "logs,expected",
    (
        (TESTER.logs, ["foo", "boo", "doo"]),
        (TESTER.logs_arg, ["super_dict", "slow_dict"]),
        (TESTER.empty_logs, []),
        (TESTER.empty_logs_arg, []),
    ),
)
def test_register(logs, expected):
    assert list(logs.storage.keys()) == expected


@pytest.mark.parametrize(
    "logs,name,parent_class",
    (
        (TESTER.logs, "foo", Mapping),
        (TESTER.logs_arg, "slow_dict", dict),
    ),
)
def test_dispatch(logs, name, parent_class):
    assert issubclass(logs.dispatch(name), parent_class) is True


@pytest.mark.parametrize(
    "logs,name,expected", ((TESTER.logs_arg, "fast_dict", dict), (TESTER.empty_logs_arg, "any_name", list))
)
def test_default_dispatch(logs, name, expected):
    assert logs.dispatch(name) == expected


@pytest.mark.parametrize("logs,name", ((TESTER.logs, "dummy_dict"), (TESTER.empty_logs, "any_name")))
def test_dispatch_error(logs, name):
    with pytest.raises(ValueError):
        logs.dispatch(name)


@pytest.mark.parametrize(
    "logs,name,cls", ((TESTER.logs, "foo", TESTER.mapping_class), (TESTER.logs_arg, "super_dict", Counter))
)
def test_register_error(logs, name, cls):
    with pytest.raises(ValueError):
        logs.register(name)(cls)
