from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor
from math import ceil, inf
from multiprocessing import Manager
from multiprocessing.managers import ListProxy
from queue import Queue

import requests
from bs4 import BeautifulSoup
from loguru import logger

URL = "https://en.wikipedia.org/wiki/"
TARGET = "Adolf_Hitler"


def get_wikipedia_pages(page_name: str) -> list[str]:
    url = URL + page_name
    page_names: set[str] = set()
    response = requests.get(url)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/wiki/") and ":" not in href:
            page_names.add(href[6:])
    page_names.remove("Main_Page")

    return list(page_names)


def check_page(page: str, queue: Queue, visited: set[str], path: list[str], depth: int) -> list[str] | None:
    pages = get_wikipedia_pages(page)

    for page in pages:
        if page in visited:
            continue
        if page == TARGET:
            return path + [page]
        visited.add(page)
        queue.put([page, path + [page], depth + 1])


def find_path(pages: list[str], max_depth: int, min_depth: ListProxy) -> list[str] | None:
    queue: Queue = Queue()
    visited: set[str] = set()
    for page in pages:
        if page == TARGET:
            logger.info(f"Find path! Depth: 1")
            min_depth[0] = 1
            return [page]
        queue.put([page, [page], 1])
        visited.add(page)

    while not queue.empty():
        current_page, path, depth = queue.get()
        if depth >= max_depth or depth + 1 >= min_depth[0]:
            return None

        result = check_page(current_page, queue, visited, path, depth)
        if result and depth + 1 < min_depth[0]:
            logger.info(f"Find path! Depth: {depth + 1}")
            min_depth[0] = depth + 1
            return result


def get_path(start_page: str, max_depth: int, processes_count: int) -> list[str]:
    if start_page == TARGET:
        return [TARGET]
    pages = get_wikipedia_pages(start_page)
    size = ceil(len(pages) / processes_count)
    min_depth = Manager().list()
    min_depth.append(inf)
    separated_pages = [pages[i : i + size] for i in range(0, len(pages), size)]

    logger.info(f"Starting WikipediaRace!")
    with ProcessPoolExecutor(max_workers=processes_count) as executor:
        futures = [executor.submit(find_path, page, max_depth, min_depth) for page in separated_pages]
        paths = list(filter(None, [future.result() for future in futures]))
    if not paths:
        return []
    return min(paths, key=lambda x: len(x))


def main(start_page: str, max_depth: int, processes_count: int) -> None:
    result = get_path(start_page, max_depth, processes_count)
    if not result:
        print("Path not found!")
    else:
        print(" >> ".join([start_page] + result))


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--page", type=str, default="Main_Page", help="Page name")
    argparser.add_argument("--depth", type=int, default=3, help="Max depth")
    argparser.add_argument("--processes", type=int, default=8, help="Process count")

    args = argparser.parse_args()
    main(args.page, args.depth, args.processes)
