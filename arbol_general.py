from typing import Any, List, Optional

class Node:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.children: List['Node'] = []

class GeneralTree:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def insert(self, parent_value: Any, child_value: Any) -> bool:
        """Inserta child_value como hijo de parent_value (crea root si está vacío)."""
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
        """Busca un nodo cuyo .value sea value."""
        def _search(node: Node) -> Optional[Node]:
            if node.value == value:
                return node
            for ch in node.children:
                res = _search(ch)
                if res:
                    return res
            return None
        return _search(self.root) if self.root else None
    
    def find_path(self, target: Any) -> List[Any]:
        """
        Devuelve la ruta (lista de .value) desde la raíz hasta el nodo que contiene `target`.
        Si no se encuentra, devuelve [].
        """
        if self.root is None:
            return []
        
        queue = [(self.root, [self.root.value])]  # Tupla: (nodo, camino hasta aquí)
        
        while queue:
            current, path = queue.pop(0)
            if current.value == target:
                return path
            for child in current.children:
                queue.append((child, path + [child.value]))
        
        return []


    def display(self) -> None:
        """Imprime el árbol en formato ascii."""
        if not self.root:
            print("Tree is empty")
            return
        print(self.root.value)
        for i, ch in enumerate(self.root.children):
            last = (i == len(self.root.children)-1)
            self._display_tree(ch, "", last)

    def _display_tree(self, node: Node, prefix: str, is_last: bool) -> None:
        conn = "└── " if is_last else "├── "
        print(f"{prefix}{conn}{node.value}")
        new_pref = prefix + ("    " if is_last else "│   ")
        for i, ch in enumerate(node.children):
            last = (i == len(node.children)-1)
            self._display_tree(ch, new_pref, last)
