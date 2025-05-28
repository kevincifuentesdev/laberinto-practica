from typing import List, Tuple, Optional, Any, Set
from random import randint
from arbol_general import GeneralTree, Node

MURO = 'X'
DIRECCIONES = [(0, -1), (0, 1), (1, 0), (-1, 0)]

class Persona:
    """
    Representa un agente que explora el laberinto,
    mantiene árboles de la ruta más corta, movimientos y todas las rutas.
    """
    def __init__(self, posicion_inicial: Tuple[int, int], laberinto) -> None:
        """
        initial_position: posición de inicio (x, y).
        maze: instancia de Laberinto.
        """
        self.laberinto = laberinto
        self.salidas = laberinto.salida
        self.posicion_actual: Tuple[int, int] = posicion_inicial
        self.direcciones_perdidas: Set[Tuple[int,int]] = set()
        self.ruta_corta = self._calcular_ruta_salida_corta(posicion_inicial, self.salidas)
        self.rutas_tomadas = self._registrar_movimientos(posicion_inicial)
        self.arbol_rutas_todas = self._calcular_arbol_rutas_todas(posicion_inicial, self.salidas)

    def _perder_movimiento(self) -> Optional[str]:
        """
        Elige al azar una dirección que todavía no se perdió,
        la marca como inhabilitada y retorna su nombre.
        """
        disponibles = [d for d in DIRECCIONES if d not in self.direcciones_perdidas]
        if not disponibles:
            return None

        mov = disponibles[randint(0, len(disponibles)-1)]
        self.direcciones_perdidas.add(mov)
        etiquetas = {
            (0, -1): "arriba",
            (0, 1): "abajo",
            (1, 0): "derecha",
            (-1, 0): "izquierda"
        }
        return etiquetas[mov]

    def _calcular_ruta_salida_corta(self,
                                    posicion_inicial: Tuple[int, int],
                                    salidas: List[Tuple[int, int]]) -> GeneralTree:
        """
        Calcula el árbol de la ruta más corta desde posicion_inicial
        hasta cualquiera de las salidas. Usa BFS.
        """
        candidate_trees: List[GeneralTree] = []
        for salida in salidas:
            start = posicion_inicial
            end = salida
            n = self.laberinto.tamanno
            visited = {start}
            parent: dict = {}
            queue: List[Tuple[int,int]] = [start]
            encontrado = False

            while queue:
                current = queue.pop(0)
                if current == end:
                    encontrado = True
                    break
                for dx, dy in [d for d in DIRECCIONES if d not in self.direcciones_perdidas]:
                    nx, ny = current[0]+dx, current[1]+dy
                    if 0 <= nx < n and 0 <= ny < n:
                        if self.laberinto.matriz[ny][nx] != MURO and (nx,ny) not in visited:
                            visited.add((nx,ny))
                            parent[(nx,ny)] = current
                            queue.append((nx,ny))

            if not encontrado:
                continue
            # reconstruir camino
            path, node = [], end
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            # crear árbol de esta ruta
            tree = GeneralTree()
            tree.root = Node(start)
            for i in range(len(path)-1):
                tree.insert(path[i], path[i+1])
            candidate_trees.append(tree)

        if not candidate_trees:
            return GeneralTree()
        
        return min(candidate_trees, key=lambda t: t.node_count())
    
    def _registrar_movimientos(self, raiz: Tuple[int, int]) -> GeneralTree:
        """
        Inicializa y retorna un árbol que registrará los movimientos realizados.
        """
        tree = GeneralTree()
        tree.root = Node(raiz)
        return tree

    def _calcular_arbol_rutas_todas(self,
                                   start: Tuple[int, int],
                                   salidas: List[Tuple[int, int]]) -> GeneralTree:
        """
        Construye un árbol cuyas ramas representan todas las rutas simples
        hasta cada salida, evitando muros y posiciones repetidas.
        """
        tree = GeneralTree()
        tree.root = Node(start)
        collected_paths: List[List[Tuple[int,int]]] = []
        size = self.laberinto.tamanno

        def dfs(position: Tuple[int,int],
                path: List[Tuple[int,int]],
                visited: Set[Tuple[int,int]]) -> None:
            if position in salidas:
                collected_paths.append(path.copy())
                return
            for dx, dy in [d for d in DIRECCIONES if d not in self.direcciones_perdidas]:
                next_x, next_y = position[0] + dx, position[1] + dy
                if 0 <= next_x < size and 0 <= next_y < size and (next_x, next_y) not in visited:
                    if self.laberinto.matriz[next_y][next_x] != MURO:
                        visited.add((next_x, next_y))
                        path.append((next_x, next_y))
                        dfs((next_x, next_y), path, visited)
                        path.pop()
                        visited.remove((next_x, next_y))

        dfs(start, [start], {start})
        for route in collected_paths:
            node = tree.root
            for coord in route[1:]:
                child = next((c for c in node.children if c.value == coord), None)
                if not child:
                    child = Node(coord)
                    node.children.append(child)
                node = child
        return tree
