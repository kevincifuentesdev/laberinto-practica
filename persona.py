from typing import List, Tuple, Optional, Union
from random import randint
from typing import Any
from laberinto import Laberinto
from arbol_general import GeneralTree, Node

MURO = 'X'

class Persona:
    def __init__(self, posicion_inicial: Tuple[int, int], laberinto: Laberinto) -> None:
        self.laberinto = laberinto
        self.salida = laberinto.salida
        self.posicion_actual: Tuple[int, int] = posicion_inicial
        self.posibles_movimientos: List[Tuple[int, int]] = [
            (0, -1), (0, 1), (1, 0), (-1, 0)
        ]
        self.ruta_corta: GeneralTree = self._calcular_ruta_corta(posicion_inicial)
        self.rutas_tomadas: GeneralTree = self._registrar_movimientos(posicion_inicial)

    def _perder_movimiento(self) -> None:
        if self.posibles_movimientos:
            idx = randint(0, len(self.posibles_movimientos) - 1)
            self.posibles_movimientos.pop(idx)

    def _calcular_ruta_corta(self, raiz: Tuple[int, int]) -> GeneralTree:
        # BFS en la matriz para hallar ruta más corta de raiz a self.salida
        start, end = raiz, self.salida
        n = self.laberinto.tamanno
        visited = {start}
        parent: dict = {}
        queue: List[Tuple[int,int]] = [start]
        found = False

        while queue:
            cur = queue.pop(0)

            if cur == end:
                found = True
                break

            for dx, dy in self.posibles_movimientos:
                nx, ny = cur[0] + dx, cur[1] + dy

                if 0 <= nx < n and 0 <= ny < n:
                    val = self.laberinto.matriz[ny][nx]

                    if val != MURO and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = cur
                        queue.append((nx, ny))

        if not found:
            return GeneralTree()
        # reconstruye camino
        path = []
        node = end

        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()

        # construye árbol lineal de la ruta
        tree = GeneralTree()
        tree.root = Node(start)
        
        for prev, nxt in zip(path, path[1:]):
            tree.insert(prev, nxt)
        return tree

    def _registrar_movimientos(self, raiz: Tuple[int, int]) -> GeneralTree:
        # inicializa árbol de movimientos tomados con la raíz
        tree = GeneralTree()
        tree.root = Node(raiz)
        return tree
