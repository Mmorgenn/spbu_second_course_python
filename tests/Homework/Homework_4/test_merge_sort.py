from random import randint

import pytest

from src.Homework.Homework_4.merge_sort import MergeSort


@pytest.mark.parametrize(
    "random,range_list",
    ((10, range(10)), (100, range(100)), (1000, range(1000)), (2500, range(10**4)), (10**4, range(1000))),
)
def teste_merge_sort(random, range_list):
    list_int = [randint(0, random) for _ in range_list]
    merge = MergeSort(list_int)
    assert merge.merge_sort() == sorted(list_int)


@pytest.mark.parametrize(
    "random,range_list,threads",
    (
        (10, range(10), 2),
        (100, range(100), 4),
        (1000, range(1000), 6),
        (2500, range(10**4), 8),
        (10**4, range(1000), 10),
    ),
)
def teste_merge_sort_threads(random, range_list, threads):
    list_int = [randint(0, random) for _ in range_list]
    merge = MergeSort(list_int)
    assert merge.merge_sort_threads(threads) == sorted(list_int)


@pytest.mark.parametrize(
    "random,range_list,threads",
    (
        (10, range(10), 2),
        (100, range(100), 4),
        (1000, range(1000), 6),
        (2500, range(10**4), 8),
        (10**4, range(1000), 10),
    ),
)
def teste_merge_sort_process(random, range_list, threads):
    list_int = [randint(0, random) for _ in range_list]
    merge = MergeSort(list_int)
    assert merge.merge_sort_threads(threads, True) == sorted(list_int)


@pytest.mark.parametrize(
    "left_list,right_list,expected",
    (
        ([], [1], [1]),
        ([1], [2], [1, 2]),
        ([3, 6, 8], [3, 6, 8], [3, 3, 6, 6, 8, 8]),
        ([1, 4, 9], [0, 5, 5, 9], [0, 1, 4, 5, 5, 9, 9]),
    ),
)
def teste_merge(left_list, right_list, expected):
    assert MergeSort.merge(left_list, right_list) == expected
