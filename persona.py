from typing import List, Tuple, Optional, Union
from random import randint
from typing import Any
from arbol_general import GeneralTree, Node

MURO = 'X'

class Persona:
    def __init__(self, posicion_inicial: Tuple[int, int], laberinto) -> None:
        self.laberinto = laberinto
        self.salida = laberinto.salida
        self.posicion_actual: Tuple[int, int] = posicion_inicial
        self.posibles_movimientos: List[Tuple[int, int]] = [
            (0, -1), (0, 1), (1, 0), (-1, 0)
        ]
        self.ruta_corta: GeneralTree = self._calcular_ruta_corta(posicion_inicial)
        self.rutas_tomadas: GeneralTree = self._registrar_movimientos(posicion_inicial)

    def _perder_movimiento(self) -> Optional[str]:
        """
        Elimina un movimiento al azar y retorna la dirección perdida.
        """
        if self.posibles_movimientos:
            idx = randint(0, len(self.posibles_movimientos) - 1)
            mov = self.posibles_movimientos.pop(idx)
            direcciones = {
                (0, -1): "arriba",
                (0, 1): "abajo",
                (1, 0): "derecha",
                (-1, 0): "izquierda"
            }
            return direcciones.get(mov, str(mov))
        return None

    def _calcular_ruta_corta(self, raiz: Tuple[int, int]) -> GeneralTree:
        """
        Calcula la ruta más corta desde la posición actual hasta la salida
        utilizando BFS y devuelve un árbol con la ruta.
        """
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
        path = []
        node = end

        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()

        tree = GeneralTree()
        tree.root = Node(start)

        for i in range(len(path) - 1):
            tree.insert(path[i], path[i + 1])
        return tree

    def _registrar_movimientos(self, raiz: Tuple[int, int]) -> GeneralTree:
        """
        Inicializa el árbol de decisiones con la posición inicial como raíz.
        """
        tree = GeneralTree()
        tree.root = Node(raiz)  
        return tree

    def registrar_decision(self, posicion_anterior: Tuple[int, int], nueva_posicion: Tuple[int, int], alternativas: List[Tuple[int, int]]) -> None:
        """
        Registra una decisión en el árbol de movimientos tomados, marcando cuál fue elegida y cuáles no.
        """
        nodo_padre = self.rutas_tomadas._search(posicion_anterior, self.rutas_tomadas.root)

        if nodo_padre:
            nodo_padre.children.append(Node((nueva_posicion, True)))  # True indica que fue elegida

            for alternativa in alternativas:
                if alternativa != nueva_posicion:
                    nodo_padre.children.append(Node((alternativa, False)))  # False indica que no fue elegida
