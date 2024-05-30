from argparse import ArgumentParser
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from copy import copy
from dataclasses import dataclass
from multiprocessing import Manager
from typing import Optional

import requests
from bs4 import BeautifulSoup
from loguru import logger

URL = "https://en.wikipedia.org/wiki/"


def get_wikipedia_pages(page_name: str) -> set[str]:
    url = URL + page_name
    page_names: set[str] = set()
    response = requests.get(url)
    if response.status_code != 200:
        return set()
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/wiki/") and ":" not in href:
            page_names.add(href[6:])
    page_names.remove("Main_Page")

    return page_names


@dataclass(unsafe_hash=True)
class Node:
    page: str
    previous: Optional["Node"] = None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and self.page == other.page

    def get_path(self) -> list[str]:
        if self.previous is None:
            return [self.page]
        return self.previous.get_path() + [self.page]

    def get_all_pages(self, visited: set[str]) -> set["Node"]:
        pages = get_wikipedia_pages(self.page) - visited
        nodes = set()
        for page in pages:
            nodes.add(Node(page, self))
        return nodes


class BFS:
    def __init__(self, start_page: str, target_page: str, visited: set[str]) -> None:
        self.start_page: str = start_page
        self.target_page: str = target_page
        self.current_nodes: set[Node] = set()
        self.visited: set[str] = visited

    def find_path_between_two(self, process: int, depth_limit: int = 4) -> list[str]:
        if self.start_page == self.target_page:
            return [self.start_page]
        self.visited.add(self.start_page)
        self.current_nodes.add(Node(self.start_page, None))
        with ProcessPoolExecutor(max_workers=process) as executor:
            # By depth
            for depth in range(1, depth_limit + 1):
                logger.info(f"Dropped to the depth {depth}")
                nodes_chunks = [executor.submit(Node.get_all_pages, node, self.visited) for node in self.current_nodes]
                deeper_nodes = set()
                # By wave
                for future in as_completed(nodes_chunks):
                    nodes = future.result()
                    for node in nodes:
                        if node.page not in self.visited:
                            self.visited.add(node.page)
                            deeper_nodes.add(node)
                        else:
                            continue
                        if node.page == self.target_page:
                            logger.info(f"Find target page: {self.target_page}")
                            for chunk in nodes_chunks:
                                chunk.cancel()
                            return node.get_path()
                        deeper_nodes.add(node)
                self.current_nodes = deeper_nodes
            return []


def get_wiki_path(pages: list[str], process: int, unique: bool, max_depth: int = 4) -> list[str]:
    visited: set[str] = set()
    final_path = []
    for i in range(len(pages) - 1):
        logger.info(f"{i}) {pages[i]}")
        path = BFS(pages[i], pages[i + 1], copy(visited)).find_path_between_two(process, max_depth)
        if path is []:
            logger.info(f"Path is not found for {max_depth} depth")
            return path
        if unique:
            visited.union(set(path))
        if i > 0:
            path = path[1:]
        final_path += path
    return final_path


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--pages", type=list[str], default=["Germany", "Adolf_Hitler"], help="Page names")
    argparser.add_argument("--depth", type=int, default=4, help="Max depth")
    argparser.add_argument("--processes", type=int, default=8, help="Process count")
    argparser.add_argument("--unique", type=bool, default=False)

    args = argparser.parse_args()
    print(get_wiki_path(args.pages, args.processes, args.unique, args.depth))
