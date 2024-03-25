from random import random
from typing import Generic, Iterator, MutableMapping, Optional, TypeVar

Value = TypeVar("Value")
Key = TypeVar("Key")


class Node(Generic[Key, Value]):
    def __init__(self, key: Key, value: Value) -> None:
        self.key: Key = key
        self.value: Value = value
        self.priority: float = random()
        self.left: Node | None = None
        self.right: Node | None = None
        self.size: int = 1

    def __eq__(self, other_node: object) -> bool:
        return isinstance(other_node, Node) and (self.key, self.value) == (other_node.key, other_node.value)

    def __str__(self) -> str:
        return f"Node(value={self.value}, key={self.key}, priority={self.priority}, left={self.left}, right={self.right}, size={self.size})"

    def __repr__(self) -> str:
        return f"{self.__dict__}"

    @staticmethod
    def get_size(node: Optional["Node"]) -> int:
        if node is None:
            return 0
        return node.size

    @staticmethod
    def update_size(node: Optional["Node"]) -> Optional["Node"]:
        if node is not None:
            node.size = Node.get_size(node.left) + Node.get_size(node.right) + 1
        return node


class Treap(MutableMapping):
    def __init__(self) -> None:
        self.root: Node | None = None

    def __getitem__(self, key: Key) -> Value | None:

        def recursion_find(node: Node | None) -> Value:
            if node is None:
                raise KeyError("No such key")
            if node.key == key:
                return node.value
            if node.key > key:
                return recursion_find(node.left)
            else:
                return recursion_find(node.right)

        return recursion_find(self.root)

    def __setitem__(self, key: Key, value: Value) -> None:
        if self._has_key(key):
            raise KeyError("Such key is already added")
        tree_additional = Treap()
        node_additional = Node(key, value)
        tree_additional.root = node_additional
        tree_smaller, tree_bigger = self._split(key)
        tree_with_key = Treap._merge(tree_smaller, tree_additional)
        self.root = Treap._merge(tree_with_key, tree_bigger).root

    def __delitem__(self, key: Key) -> None:
        if not self._has_key(key):
            raise KeyError("There is no such key")
        tree_smaller, tree_bigger = self._split(key)
        tree_bigger._del_smaller()
        self.root = Treap._merge(tree_smaller, tree_bigger).root

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
        return f"Treap(root={self.root})"

    def __repr__(self) -> str:
        return f"{self.__dict__}"

    @staticmethod
    def _split_node(node: Node | None, key: Key) -> tuple[Optional[Node], Optional[Node]]:
        if node is None:
            return None, None
        if key > node.key:
            node_first, node_second = Treap._split_node(node.right, key)
            node.right = node_first
            return Node.update_size(node), node_second
        else:
            node_first, node_second = Treap._split_node(node.left, key)
            node.left = node_second
            return node_first, Node.update_size(node)

    def _split(self, key: Key) -> tuple["Treap", "Treap"]:
        node_first, node_second = Treap._split_node(self.root, key)
        tree_first, tree_second = Treap(), Treap()
        tree_first.root = node_first
        tree_second.root = node_second
        return tree_first, tree_second

    @staticmethod
    def _merge_node(node_first: Node | None, node_second: Node | None) -> Node | None:
        if node_first is None:
            return node_second
        if node_second is None:
            return node_first
        if node_first.priority > node_second.priority:
            node_first.right = Treap._merge_node(node_first.right, node_second)
            return Node.update_size(node_first)
        else:
            node_second.left = Treap._merge_node(node_first, node_second.left)
            return Node.update_size(node_second)

    @staticmethod
    def _merge(tree_first: "Treap", tree_second: "Treap") -> "Treap":
        tree_new = Treap()
        node_new = Treap._merge_node(tree_first.root, tree_second.root)
        tree_new.root = node_new
        return tree_new

    def _del_smaller(self) -> None:
        if self.root is None:
            return

        def recursion_del(node: Node) -> Node | None:
            if node.left is None:
                return node.right
            node.left = recursion_del(node.left)
            return Node.update_size(node)

        self.root = recursion_del(self.root)

    def _has_key(self, key: Key) -> bool:

        def recursion_find(node: Node | None) -> bool:
            if node is None:
                return False
            if node.key == key:
                return True
            if node.key > key:
                return recursion_find(node.left)
            else:
                return recursion_find(node.right)

        return recursion_find(self.root)
