from copy import deepcopy
from random import random
from typing import Generic, Iterator, MutableMapping, Optional, TypeVar

Value = TypeVar("Value")
Key = TypeVar("Key", int, str)


class Node(Generic[Key, Value]):
    def __init__(self, key: Key, value: Value) -> None:
        self.key: Key = key
        self.value: Value = value
        self.priority: float = random()
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.size: int = 1

    def __eq__(self, other_node: object) -> bool:
        return isinstance(other_node, Node) and (self.key, self.value) == (other_node.key, other_node.value)

    def __str__(self) -> str:
        return f"Node('key': {self.key}, 'value': {self.value})"

    def __repr__(self) -> str:
        return f"{self.__dict__}"

    @staticmethod
    def get_size(node: Optional["Node"]) -> int:
        if node is None:
            return 0
        return node.size

    def update_size(self) -> None:
        self.size = Node.get_size(self.left) + Node.get_size(self.right) + 1

    def split(self, key: Key, deepcopy_on: bool = False) -> tuple[Optional["Node"], Optional["Node"]]:

        def _split(node: Optional["Node"]) -> tuple[Optional["Node"], Optional["Node"]]:
            if node is None:
                return None, None
            if key > node.key:
                node_first, node_second = _split(node.right)
                node.right = node_first
                node.update_size()
                return node, node_second
            else:
                node_first, node_second = _split(node.left)
                node.left = node_second
                node.update_size()
                return node_first, node

        if deepcopy_on:
            return _split(deepcopy(self))
        return _split(self)

    def merge(self, other: Optional["Node"], deepcopy_on: bool = False) -> "Node":

        def _merge(node: "Node", other: Optional["Node"]) -> "Node":
            if other is None:
                return node
            if node.priority > other.priority:
                if node.right is None:
                    node.right = other
                else:
                    node.right = _merge(node.right, other)
                node.update_size()
                return node
            else:
                other.left = _merge(node, other.left)
                other.update_size()
                return other

        if deepcopy_on:
            return _merge(deepcopy(self), deepcopy(other))
        return _merge(self, other)

    def _del_smallest(self) -> Optional["Node"]:

        def recursion_del(node: "Node") -> Optional["Node"]:
            if node.left is None:
                return node.right
            node.left = recursion_del(node.left)
            node.update_size()
            return node

        return recursion_del(self)


class Treap(MutableMapping):
    def __init__(self, root: Node | None = None) -> None:
        self.root: Node | None = root

    def __getitem__(self, key: Key) -> Value | None:
        node = self._get_node(key)
        if node is None:
            raise KeyError("There is no such key!")
        return node.value

    def __setitem__(self, key: Key, value: Value) -> None:
        if self._has_key(key):
            raise KeyError("Such key is already added")
        node_additional = Node(key, value)
        if self.root is None:
            self.root = node_additional
            return
        node_smaller, node_bigger = self.root.split(key)
        if node_smaller is None:
            self.root = node_additional.merge(node_bigger)
            return
        node_with_key = node_smaller.merge(node_additional)
        self.root = node_with_key.merge(node_bigger)

    def __delitem__(self, key: Key) -> None:
        if self.root is None or not self._has_key(key):
            raise KeyError("There is no such key")
        node_smaller, node_bigger = self.root.split(key)
        if node_bigger is None:
            # Otherwise mypy will not understand
            raise KeyError("There is no such key")
        node_bigger = node_bigger._del_smallest()
        if node_smaller is None:
            self.root = node_bigger
            return
        self.root = node_smaller.merge(node_bigger)

    def __iter__(self) -> Iterator[Value]:
        keys = []

        def recursion_iterator(node: Node) -> None:
            current_nodes = filter(None, (node.left, node, node.right))
            for current_node in current_nodes:
                if current_node != node:
                    recursion_iterator(current_node)
                else:
                    keys.append(current_node.key)

        if self.root is None:
            return iter(keys)
        recursion_iterator(self.root)
        return iter(keys)

    def __len__(self) -> int:
        return Node.get_size(self.root)

    def __str__(self) -> str:
        return f"Treap{str(self.items())[9:]}"

    def __repr__(self) -> str:
        return f"{self.__dict__}"

    def _get_node(self, key: Key) -> Node | None:

        def recursion_find(node: Node | None) -> Node | None:
            if node is None:
                return None
            if node.key == key:
                return node
            if node.key > key:
                return recursion_find(node.left)
            else:
                return recursion_find(node.right)

        return recursion_find(self.root)

    def _has_key(self, key: Key) -> bool:
        node = self._get_node(key)
        return not (node is None)
