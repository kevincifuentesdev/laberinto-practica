from typing import List, Tuple, Optional, Union
from random import random
from arbol_general import GeneralTree

class Persona:
    def __init__(self, posicion_inicial: Tuple[int, int]) -> None:
        self.posicion_actual: Tuple[int, int] = posicion_inicial
        self.posibles_movimientos: List[Tuple[int, int]] = [
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0)
        ]
        self.ruta_corta: GeneralTree = self._calcular_ruta_corta(posicion_inicial)
        self.rutas_tomadas: GeneralTree = self._registrar_movimientos(posicion_inicial)
    
    def _perder_movimiento(self):
        ...

    def _calcular_ruta_corta(self, raiz: Tuple[int, int]) -> GeneralTree:
        ...

    def _registrar_movimientos(self, raiz: Tuple[int, int]) -> GeneralTree:
        ...
