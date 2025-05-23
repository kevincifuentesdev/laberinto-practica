from typing import Any, List, Optional

class Node:
    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.children: List['Node'] = []

class GeneralTree:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def bfs(self) -> List[Any]:
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            for child in node.children:
                queue.append(child)
        return result

    def insert(self, parent: Any, child: Any) -> bool:
        """
        Inserta un nodo con valor `child` bajo el nodo cuyo valor es `parent`.
        Si el árbol está vacío, crea la raíz con `parent` y le añade `child`.
        Devuelve True si la inserción fue exitosa, False si no encontró `parent`.
        """
        if self.root is None:
            self.root = Node(parent)
            self.root.children.append(Node(child))
            return True

        parent_node = self._search(parent, self.root)
        if parent_node is None:
            return False

        parent_node.children.append(Node(child))
        return True

    def _search(self, value: Any, node: Node) -> Optional[Node]:
        """
        Busca en profundidad un nodo con valor `value` a partir de `node`.
        Retorna el nodo si lo encuentra, o None.
        """
        if node.value == value:
            return node
        for ch in node.children:
            found = self._search(value, ch)
            if found:
                return found
        return None

    def display(self) -> None:
        """
        Muestra el árbol en consola con información adicional sobre las decisiones.
        """
        if self.root is None:
            print("Tree is empty")
            return
        self._display_tree(self.root, "", True)

    def _display_tree(self, node: Node, prefix: str, is_last: bool) -> None:
        """
        Muestra un nodo y sus hijos en formato jerárquico.
        """
        connector = "└── " if is_last else "├── "
        value = node.value
        if isinstance(value, tuple) and len(value) == 2:
            posicion, elegida = value
            estado = "✔" if elegida else "✘"
            print(f"{prefix}{connector}Celda {posicion} ({estado})")
        else:
            print(f"{prefix}{connector}{value}")
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            is_last_child = i == len(node.children) - 1
            self._display_tree(child, new_prefix, is_last_child)
