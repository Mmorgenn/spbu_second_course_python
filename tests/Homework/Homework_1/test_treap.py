from random import randint, shuffle

import pytest

from src.Homework.Homework_1.treap import *


def create_dummy_treap(elements_list: list[tuple[Key, Value]]) -> Treap:
    tree = Treap()
    shuffle(elements_list)
    for key, value in elements_list:
        tree[key] = value
    return tree


@pytest.mark.parametrize(
    "elements_list,expected",
    (
        ([(i, i * i) for i in range(10)], 10),
        ([(i, i + 20) for i in range(100)], 100),
        ([(i, i - 3) for i in range(1000)], 1000),
        ([("a", 12), ("b", "b"), ("da", "net"), ("text", None), ("for", 3), ("test", (1, 2, 3))], 6),
    ),
)
def test_insert(elements_list, expected):
    tree = create_dummy_treap(elements_list)
    assert len(tree) == expected


@pytest.mark.parametrize(
    "elements_list,key_list,len_expected",
    (
        ([(i, i * 23) for i in range(15)], [1, 5, 6, 9], 15),
        ([(i, "a" * i) for i in range(100)], [i for i in range(25)], 100),
        ([(i, i) for i in range(1000)], [i for i in range(1000)], 1000),
    ),
)
def test_delete(elements_list, key_list, len_expected):
    shuffle(key_list)
    tree = create_dummy_treap(elements_list)
    for key in key_list:
        len_expected -= 1
        del tree[key]
        assert len(tree) == len_expected


@pytest.mark.parametrize(
    "elements_list",
    (
        [(i, randint(1, 25)) for i in range(25)],
        [(i, randint(1, 10**4)) for i in range(250)],
        [(i, i**3) for i in range(1000)],
    ),
)
def test_get_item(elements_list):
    tree = create_dummy_treap(elements_list)
    shuffle(elements_list)
    for key, value in elements_list:
        assert tree[key] == value


@pytest.mark.parametrize(
    "elements_list,key_list",
    (
        ([(i**2, i) for i in range(25)], [i**2 for i in range(25)]),
        ([(i * 2, i - 1) for i in range(100)], [i * 2 for i in range(100)]),
        ([(i, i) for i in range(1000)], [i for i in range(1000)]),
        ([("a", 13), ("b", "b"), ("de", "1"), ("df", (1, 2, 3)), ("wow", "Vau")], ["a", "b", "de", "df", "wow"]),
    ),
)
def test_iter(elements_list, key_list):
    tree = create_dummy_treap(elements_list)
    assert [key for key in tree] == key_list


@pytest.mark.parametrize(
    "elements_list,key,value",
    (
        ([(i, i) for i in range(10)], 0, 0),
        ([(i, i * 2) for i in range(100)], 52, 52),
        ([("text", "for"), ("test", "test"), ("fantazii", "net")], "test", 12),
    ),
)
def test_insert_error(elements_list, key, value):
    tree = create_dummy_treap(elements_list)
    with pytest.raises(KeyError):
        tree[key] = value


@pytest.mark.parametrize(
    "elements_list,key",
    (
        ([], 12),
        ([(i, i) for i in range(10)], 10),
        ([(i, i * 2) for i in range(100)], -52),
        ([("text", "for"), ("test", "test"), ("fantazii", "net")], "12"),
    ),
)
def test_delete_error(elements_list, key):
    tree = create_dummy_treap(elements_list)
    with pytest.raises(KeyError):
        del tree[key]
