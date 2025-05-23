from typing import List, Tuple, Optional, Union, Any
from persona import Persona
import random

MURO = 'X'
CAMINO = ' '
TRAMPA = 'T'
RETRASADOR = 'R'
SALIDA = 'S'
PERSONA = '\U0001F642'

class Laberinto:
    def __init__(self, tamanno: int) -> None:
        self.tamanno: int = tamanno
        self.iteracion: int = 0
        self.matriz: List[List[Any]] = self._crear_laberinto(self.tamanno)
        self.salida: Tuple[int, int] = self._ubicar_salida()
        # pasamos referencia entera al laberinto
        self.persona: Persona = Persona(self._posicionar_persona(), self)
        self.bloqueo: List[Tuple[int, int]] = []
        self.trampas: List[Tuple[int, int]] = []
        self.retrasador: List[Tuple[int, int]] = []
        self.posiciones_libres: List[Tuple[int, int]] = []

    
    def _crear_laberinto(self, tamanno: int) -> List[List]:
        return [[CAMINO for _ in range(tamanno)] for _ in range(tamanno)]
    
    
    def _ubicar_salida(self) -> Tuple[int, int]:
        while True:
            x = random.randint(0, self.tamanno - 1)
            y = random.randint(0, self.tamanno - 1)

            if self.matriz[y][x] == CAMINO:
                self.matriz[y][x] = SALIDA
                return (x, y)
    
    def _posicionar_persona(self) -> Tuple[int, int]:
        while True:
            x = random.randint(0, self.tamanno - 1)
            y = random.randint(0, self.tamanno - 1)

            if self.matriz[y][x] == CAMINO:
                self.matriz[y][x] = PERSONA
                return (x, y)
        
    def _verificar_posiciones_libres(self) -> None:
        libres: List[Tuple[int, int]] = []
        
        for y in range(self.tamanno):

            for x in range(self.tamanno):

                if self.matriz[y][x] == CAMINO:
                    libres.append((x, y))

        self.posiciones_libres = libres

    def _es_posicion_valida(self, posicion_futura: Tuple[int, int]) -> bool:
        x, y = posicion_futura

        while x < 0 or x >= self.tamanno or y < 0 or y >= self.tamanno:
            x = random.randint(0, self.tamanno - 1)
            y = random.randint(0, self.tamanno - 1)
        valor = self.matriz[y][x]

        if valor == MURO:
            return False
        
        if valor == TRAMPA:
            perdida = self.persona._perder_movimiento()
            if perdida:
                print(f"\n¡Trampa! Se perdió el movimiento hacia {perdida}.")
            return True
        
        if valor == RETRASADOR:
            self.matriz[y][x] = CAMINO

            if (x, y) in self.retrasador:
                self.retrasador.remove((x, y))
            return False
        
        return True
    
    def _mover_persona(self) -> Tuple[int, int]:
        # 1) recalcular ruta más corta desde la posición actual
        self.persona.ruta_corta = self.persona._calcular_ruta_corta(self.persona.posicion_actual)
        ruta = self.persona.ruta_corta.bfs()

        if len(ruta) < 2:
            return self.persona.posicion_actual
        
        siguiente = ruta[1]

        # 2) validar celda destino
        if not self._es_posicion_valida(siguiente):
            return self.persona.posicion_actual
        
        # 3) actualizar matriz: limpiar vieja posición y poner PERSONA
        ox, oy = self.persona.posicion_actual
        nx, ny = siguiente
        self.matriz[oy][ox] = CAMINO
        self.matriz[ny][nx] = PERSONA
        
        # 4) registrar movimiento
        previo = self.persona.posicion_actual
        self.persona.posicion_actual = siguiente
        self.persona.rutas_tomadas.insert(previo, siguiente)
        return siguiente
    
    def _ubicar_bloqueo(self) -> None:
        self._verificar_posiciones_libres()

        if not self.posiciones_libres:
            return
        
        idx = random.randint(0, len(self.posiciones_libres) - 1)
        x, y = self.posiciones_libres.pop(idx)
        self.matriz[y][x] = MURO
        self.bloqueo.append((x, y))

    def _ubicar_trampa(self) -> None:
        self._verificar_posiciones_libres()

        if not self.posiciones_libres:
            return
        
        idx = random.randint(0, len(self.posiciones_libres) - 1)
        x, y = self.posiciones_libres.pop(idx)
        self.matriz[y][x] = TRAMPA
        self.trampas.append((x, y))

    def _ubicar_retrasador(self) -> None:
        self._verificar_posiciones_libres()

        if not self.posiciones_libres:
            return
        
        idx = random.randint(0, len(self.posiciones_libres) - 1)
        x, y = self.posiciones_libres.pop(idx)
        self.matriz[y][x] = RETRASADOR
        self.retrasador.append((x, y))

    def iniciar_laberinto(self) -> None:
        self._ubicar_bloqueo()
        self._ubicar_trampa()
        self._ubicar_retrasador()

    def __repr__(self) -> str:
        return "\n".join(str(row) for row in self.matriz)
    
if __name__ == "__main__":
    laberinto = Laberinto(4)

    laberinto.iniciar_laberinto()

    print(laberinto)