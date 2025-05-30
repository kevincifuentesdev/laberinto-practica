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
        posicion_actual: posición de inicio (x, y).
        laberinto: instancia de Laberinto.
        """
        self.laberinto = laberinto
        self.salidas = laberinto.salida
        self.posicion_actual: Tuple[int, int] = posicion_inicial
        self.direcciones_perdidas: Set[Tuple[int,int]] = set()
        self.ruta_corta = self.obtener_ruta_mas_corta(posicion_inicial, self.salidas)
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


    def _calcular_arbol_rutas(self,
                            posicion_inicial: Tuple[int, int],
                            salidas: List[Tuple[int, int]]) -> GeneralTree:
        """
        Calcula un árbol con todas las rutas posibles desde posicion_inicial
        hasta cualquiera de las salidas usando BFS.
        Retorna un árbol que contiene todas las rutas.
        """
        tree = GeneralTree()
        tree.root = Node(posicion_inicial)
        n = self.laberinto.tamanno
        visited = {posicion_inicial}
        queue: List[Tuple[int, List[Tuple[int, int]]]] = [(posicion_inicial, [posicion_inicial])]

        while queue:
            current, path = queue.pop(0)
            if current in salidas:
                continue
            for dx, dy in [d for d in DIRECCIONES if d not in self.direcciones_perdidas]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < n and 0 <= ny < n:
                    if self.laberinto.matriz[ny][nx] != MURO and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(nx, ny)]))
        return tree



    def obtener_ruta_mas_corta(self, tree: GeneralTree) -> List[Any]:
        """
        Identifica la ruta más corta en el árbol usando el método de conteo de nodos.
        Retorna la ruta más corta como una lista de coordenadas.
        """
        rutas = tree.bfs()  # Obtiene todas las rutas en anchura
        if not rutas:
            return []
        return min(rutas, key=len)  # Retorna la ruta más corta
    