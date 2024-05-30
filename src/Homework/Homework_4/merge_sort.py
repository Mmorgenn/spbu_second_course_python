from argparse import ArgumentParser
from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor
from math import log2
from random import randint
from timeit import timeit

import matplotlib.pyplot as plt
from loguru import logger


class MergeSort:
    def __init__(self, list_int: list[int]) -> None:
        self.list_int: list[int] = list_int
        self.pool: None | ThreadPoolExecutor | ProcessPoolExecutor = None

    @staticmethod
    def merge(left_list: list[int], right_list: list[int]) -> list[int]:
        sorted_list = []
        left_index, right_index = 0, 0
        while left_index != len(left_list) and right_index != len(right_list):
            if left_list[left_index] <= right_list[right_index]:
                sorted_list.append(left_list[left_index])
                left_index += 1
            else:
                sorted_list.append(right_list[right_index])
                right_index += 1
        if len(left_list) != left_index:
            return sorted_list + left_list[left_index:]
        return sorted_list + right_list[right_index:]

    def _merge_sort(self, list_int: list[int]) -> list[int]:
        if len(list_int) <= 1:
            return list_int
        mid = len(list_int) // 2 + len(list_int) % 2
        left_list = self._merge_sort(list_int[:mid])
        right_list = self._merge_sort(list_int[mid:])

        return self.merge(left_list, right_list)

    def merge_sort(self) -> list[int]:
        return self._merge_sort(self.list_int)

    def _merge_sort_threades(self, list_int: list[int], threads: int) -> list[int]:
        if len(list_int) <= 1:
            return list_int
        if threads < 2 or self.pool is None:
            return self._merge_sort(list_int)
        left = self.pool.submit(self._merge_sort_threades, list_int[: len(list_int) // 2], threads // 2)
        right = self.pool.submit(self._merge_sort_threades, list_int[len(list_int) // 2 :], threads // 2)
        return self.merge(left.result(), right.result())

    def merge_sort_threads(
        self,
        threads: int,
        multiprocessing: bool = False,
    ) -> list[int]:
        pool = ThreadPoolExecutor if multiprocessing else ThreadPoolExecutor
        self.pool = pool(max_workers=threads)
        result = self._merge_sort_threades(self.list_int, threads)
        self.pool.shutdown()
        self.pool = None
        return result

    def time_merge_sort(self) -> float:
        logger.info(f"Starting MergeSort <base>")
        return timeit(lambda: self.merge_sort(), number=1)

    def time_merge_sort_threads(self, threads: int, multiprocess: bool = False) -> float:
        logger.info(f"Starting MergeSort <threades {threads}> multiprocess: {multiprocess}")
        return timeit(lambda: self.merge_sort_threads(threads, multiprocess), number=1)


class SortPlot:
    def __init__(self) -> None:
        self.data: dict[int, list[MergeSort]] = {}
        self.plot_data: dict[int, dict[str, float]] = {}

    def add_data(self, len_list: int) -> None:
        if len_list <= 0:
            raise ValueError("The length of list should be at least 1")
        data = [MergeSort([randint(0, 10**4) for i in range(len_list)]) for _ in range(3)]
        self.data[len_list] = data

    def time_data(self, len_list: int, set_threades: set[int]) -> None:
        data = self.data.get(len_list, None)
        if data is None:
            raise KeyError("There is no suitable data here")
        min_thread = min(set_threades)
        if min_thread < 1:
            raise ValueError("Thread count mut be > 0")
        self.plot_data[len_list] = {}

        if min_thread == 1:
            result = 0.0
            for current_data in data:
                result += current_data.time_merge_sort()
            self.plot_data[len_list]["base"] = result / 3
            set_threades.remove(min_thread)

        for threades in set_threades:
            result_thread, result_process = 0.0, 0.0
            for current_data in data:
                result_thread = current_data.time_merge_sort_threads(threades)
                result_process = current_data.time_merge_sort_threads(threades, True)
            self.plot_data[len_list][f"threades_{threades}"] = result_thread / 3
            self.plot_data[len_list][f"process_{threades}"] = result_process / 3

    def get_plot_bar(self, len_list: int) -> None:
        data = self.plot_data.get(len_list, None)
        if data is None:
            raise KeyError("There is no suitable data here")
        data = sorted(list(data.items()), key=lambda x: x[1])
        sort_name = [key for key, value in data]
        sort_time = [value for key, value in data]

        bar_width = 0.8

        plt.bar(sort_name, sort_time, width=bar_width, color="blue")
        plt.xlabel("Sort")
        plt.ylabel("Time")
        plt.title(f"MergeSort for {len_list} elements")
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()


def main(len_list: int, threads: set[int]) -> None:
    plot = SortPlot()
    plot.add_data(len_list)
    plot.time_data(len_list, threads)
    plot.get_plot_bar(len_list)


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--len", type=int, default=10**5, help="Len of randm list")
    argparser.add_argument("--threads", type=set, default={1, 2, 4}, help="Set of Threads count")

    args = argparser.parse_args()
    main(args.len, args.threads)
