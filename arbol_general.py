from typing import Any, List, Optional

class Node:
    """Nodo de árbol con valor y lista de hijos."""
    def __init__(self, value: Any) -> None:
        self.value = value
        self.children: List['Node'] = []

class GeneralTree:
    """
    Estructura de árbol donde cada nodo puede tener varios hijos.
    Soporta recorridos en anchura y profundidad y conteo recursivo de nodos.
    """
    def __init__(self) -> None:
        """Inicializa un árbol vacío."""
        self.root: Optional[Node] = None

    def breadth_first_traversal(self) -> List[Any]:
        """
        Retorna una lista de valores recorriendo el árbol en anchura (BFS).
        """
        if self.root is None:
            return []
        result: List[Any] = []
        queue: List[Node] = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            queue.extend(node.children)
        return result

    def depth_first_traversal(self) -> List[Any]:
        """
        Retorna una lista de valores recorriendo el árbol en profundidad (preorden).
        """
        def _dfs(node: Node, acc: List[Any]) -> None:
            acc.append(node.value)
            for child in node.children:
                _dfs(child, acc)

        if self.root is None:
            return []
        result: List[Any] = []
        _dfs(self.root, result)
        return result

    def insert(self, parent_value: Any, child_value: Any) -> bool:
        """
        Inserta un nodo con valor `child_value` como hijo de quien tenga `parent_value`.
        Si el árbol está vacío, crea raíz y le añade el hijo.
        """
        if self.root is None:
            self.root = Node(parent_value)
            self.root.children.append(Node(child_value))
            return True

        parent_node = self.search(parent_value)
        if parent_node is None:
            return False

        parent_node.children.append(Node(child_value))
        return True

    def search(self, value: Any) -> Optional[Node]:
        """
        Busca y retorna el nodo con `value` usando DFS, o None si no existe.
        """
        def _search(node: Node) -> Optional[Node]:
            if node.value == value:
                return node
            for ch in node.children:
                found = _search(ch)
                if found:
                    return found
            return None

        return _search(self.root) if self.root else None

    def display(self) -> None:
        """
        Imprime el árbol en formato ASCII con conectores ├── y └──.
        """
        if self.root is None:
            print("Tree is empty")
            return
        print(self.root.value)
        for i, child in enumerate(self.root.children):
            is_last = i == len(self.root.children) - 1
            self._display_tree(child, "", is_last)

    def _display_tree(self, node: Node, prefix: str, is_last: bool) -> None:
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{node.value}")
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            is_last_child = i == len(node.children) - 1
            self._display_tree(child, new_prefix, is_last_child)

    def node_count(self) -> int:
        """
        Retorna el número total de nodos en el árbol (recursivo).
        """
        def _count(node: Node) -> int:
            return 1 + sum(_count(child) for child in node.children)

        return _count(self.root) if self.root else 0

    def bfs(self) -> List[Any]:
        """Alias para breadth_first_traversal."""
        return self.breadth_first_traversal()

    def dfs(self) -> List[Any]:
        """Alias para depth_first_traversal."""
        return self.depth_first_traversal()

    def length(self) -> int:
        """Alias para node_count."""
        return self.node_count()
