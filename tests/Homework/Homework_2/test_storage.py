import pytest

from src.Homework.Homework_2.command_storage import *


class Tester_PCS:
    def __init__(self, data, data_exp, action):
        self.storage = PerformedCommandStorage(data)
        self.data = data
        self.data_exp = data_exp
        self.action = action

    def apply_test(self):
        self.storage.apply_action(self.action)
        return self.storage.data == self.data_exp

    def undo_test(self):
        self.storage.undo_action()
        return self.storage.data == self.data


@pytest.mark.parametrize(
    "data,data_exp,value",
    ((deque(), deque([12]), 12), ([1, 2, 3, 4], [0, 1, 2, 3, 4], 0), ([1, 1, 1], [1, 1, 1, 1], 1)),
)
def test_first_insert(data, data_exp, value):
    tester = Tester_PCS(data, data_exp, FirstInsertAction(value))
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,data_exp,value", (([], [12], 12), ([1, 2, 3, 4], [1, 2, 3, 4, 5], 5), ([1, 1, 1], [1, 1, 1, 1], 1))
)
def test_last_insert(data, data_exp, value):
    tester = Tester_PCS(data, data_exp, LastInsertAction(value))
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,data_exp", (([12], []), ([1, 2, 3, 4], [2, 3, 4]), ([1, 1, 1], [1, 1]), ([33, 55, 33, 55], [55, 33, 55]))
)
def test_first_del(data, data_exp):
    tester = Tester_PCS(data, data_exp, FirstDelAction())
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,data_exp", (([12], []), ([1, 2, 3, 4], [1, 2, 3]), ([1, 1, 1], [1, 1]), ([33, 55, 33, 55], [33, 55, 33]))
)
def test_last_del(data, data_exp):
    tester = Tester_PCS(data, data_exp, LastDelAction())
    assert tester.apply_test() and tester.undo_test()


def test_empty_data():
    pcs = PerformedCommandStorage([])
    with pytest.raises(IndexError):
        pcs.apply_action(FirstDelAction())


@pytest.mark.parametrize(
    "data,data_exp,key,value",
    (
        ([100], [0], 0, -100),
        ([1, 1, 1, 1, 1], [1, 1, 2, 1, 1], 2, 1),
        ({"a": 123, "b": 78, "c": 56}, {"a": 123, "b": 78, "c": 78}, "c", 22),
        (deque([12, 13, 14]), deque([12, 13, 0]), 2, -14),
    ),
)
def test_add_value(data, data_exp, key, value):
    tester = Tester_PCS(data, data_exp, AddValueAction(key, value))
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,data_exp,key,value",
    (
        ([100], [0], 0, 100),
        ([1, 1, 1, 1, 1], [1, 1, 5, 1, 1], 2, -4),
        ({"a": 123, "b": 78, "c": 56}, {"a": 123, "b": 78, "c": 78}, "c", -22),
        (deque([12, 13, 14]), deque([12, 13, 12]), 2, 2),
    ),
)
def test_subtract_value(data, data_exp, key, value):
    tester = Tester_PCS(data, data_exp, SubtractValueAction(key, value))
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,data_exp,key_from,key_to",
    (
        (
            ([1, 2], [2, 1], 1, 0),
            ([1, 3, 1, 4, 1], [1, 4, 1, 3, 1], 1, 3),
            ({"amogus": 707, "a": 101, "b": 102}, {"amogus": 707, "b": 101, "a": 102}, "a", "b"),
            (deque([12, 13, 14]), deque([13, 12, 14]), 0, 1),
        )
    ),
)
def test_move(data, data_exp, key_from, key_to):
    tester = Tester_PCS(data, data_exp, MoveAction(key_from, key_to))
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,data_exp,key,value",
    (
        ([100], [-100], 0, -100),
        ([1, 1, 1, 1, 1], [1, 1, 2, 1, 1], 2, 2),
        ({"a": 123, "b": 78, "c": 56}, {"a": 123, "b": 78, "c": 7878}, "c", 7878),
        (deque([12, 13, 14]), deque([12, 13, -14]), 2, -14),
    ),
)
def test_change_value(data, data_exp, key, value):
    tester = Tester_PCS(data, data_exp, ChangeValueAction(key, value))
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,data_exp,key,value",
    (
        ([], [100], 0, 100),
        ([1, 1, 1, 1], [1, 1, 2, 1, 1], 2, 2),
        ([1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], 0, 0),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 6, 5], 4, 6),
        ({"a": 123, "b": 78}, {"a": 123, "b": 78, "c": 56}, "c", 56),
        (deque([12, 14]), deque([12, 13, 14]), 1, 13),
    ),
)
def test_change_value(data, data_exp, key, value):
    tester = Tester_PCS(data, data_exp, InsertAction(key, value))
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,data_exp,key,key_new",
    (
        ({"amogus": 0}, {"sus": 0}, "amogus", "sus"),
        ({"SPB": 10, "MOS": 20, "NOV": 9}, {"SPB": 10, "BSP": 20, "NOV": 9}, "MOS", "BSP"),
        ({"merge": 0, "split": 1}, {"need_merge": 0, "split": 1}, "merge", "need_merge"),
    ),
)
def test_change_key(data, data_exp, key, key_new):
    tester = Tester_PCS(data, data_exp, ChangeKeyAction(key, key_new))
    assert tester.apply_test() and tester.undo_test()


@pytest.mark.parametrize(
    "data,action",
    (
        (dict(), FirstInsertAction(12)),
        ([1, 2, 3, 4], ChangeKeyAction(0, 2)),
        ({"a": 123}, FirstDelAction())
    ),
)
def test_wrong_collection(data, action):
    pcs = PerformedCommandStorage(data)
    with pytest.raises(AttributeError):
        pcs.apply_action(action)


@pytest.mark.parametrize(
    "data,action",
    (
        ([1, 2, 3, 4], AddValueAction(4, 100)),
        ([1], InsertAction(-2, 2)),
        (deque([1, 2, 3, 4]), DelAction(100)),
        (deque([1, 2, 3, 4]), ChangeValueAction(-1, 200)),
    ),
)
def test_index_error(data, action):
    pcs = PerformedCommandStorage(data)
    with pytest.raises(IndexError):
        pcs.apply_action(action)


@pytest.mark.parametrize(
    "data,action",
    (
        ([1, 2, 3, 4], AddValueAction("chtoto_ne_tak?", 100)),
        ([1], InsertAction("slomalos", 2)),
        ({"bup": 123, "super": 856}, DelAction("good")),
        ({"weather": 0, "city": 1, "name": 0}, ChangeValueAction("position", 1)),
        ({"tut_nichego": 8348, "tochno_nichego": 454}, MoveAction("chtoto_est", "chegoto_net")),
    ),
)
def test_wrong_key(data, action):
    pcs = PerformedCommandStorage(data)
    with pytest.raises(KeyError):
        pcs.apply_action(action)


@pytest.mark.parametrize(
    "data,key,key_new",
    (
        ({"apple": 100, "banana": 26, "mango": 99}, "orange", "mango"),
        ({"apple": 100, "banana": 26, "mango": 99}, "apple", "banana"),
        ({"apple": 100, "banana": 26, "mango": 99}, "berry", "mango"),
    ),
)
def test_change_key_error(data, key, key_new):
    pcs = PerformedCommandStorage(data)
    with pytest.raises(KeyError):
        pcs.apply_action(ChangeKeyAction(key, key_new))
