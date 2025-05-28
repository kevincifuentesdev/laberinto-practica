from typing import List, Tuple, Any
from persona import Persona
import random

MURO = 'X'; CAMINO = ' '; TRAMPA = 'T'; RETRASADOR = 'R'
SALIDA = 'S'; PERSONA = '\U0001F642'

class Laberinto:
    """
    Representa un laberinto cuadrado con muros, trampas, retrasadores y múltiples personas.
    """
    def __init__(self, size: int, num_personas: int = 2) -> None:
        """
        size: dimensión del laberinto NxN.
        num_personas: cantidad de agentes exploradores.
        """
        self.tamanno = size
        self.iteracion = 0
        self.matriz: List[List[Any]] = self._crear_laberinto(self.tamanno)
        self.salida: List[Tuple[int,int]] = self._ubicar_salida()
        self.personas: List[Persona] = []
        for _ in range(num_personas):
            pos = self._posicionar_persona()
            self.personas.append(Persona(pos, self))
        self.bloqueo: List[Tuple[int, int]] = []
        self.trampas: List[Tuple[int, int]] = []
        self.retrasador: List[Tuple[int, int]] = []
        self.posiciones_libres: List[Tuple[int, int]] = []

    def _crear_laberinto(self, tamanno: int) -> List[List[str]]:
        """Retorna una matriz llenada de celdas de camino."""
        return [[CAMINO for _ in range(tamanno)] for _ in range(tamanno)]

    def _ubicar_salida(self) -> List[Tuple[int,int]]:
        """Ubica dos salidas aleatorias en celdas de camino."""
        salidas = 0
        x = 0
        y = 0

        posiciones_salida = []

        while salidas < 2:
            x = random.randint(0, self.tamanno - 1)
            y = random.randint(0, self.tamanno - 1)

            if self.matriz[y][x] == CAMINO:
                self.matriz[y][x] = SALIDA
                posiciones_salida.append((x, y))
                salidas += 1

        return posiciones_salida
    
    def _posicionar_persona(self) -> Tuple[int,int]:
        """Elige aleatoriamente una celda libre y coloca un PERSONA."""
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

    def _es_posicion_valida(self,
                          persona: Persona,
                          posicion_futura: Tuple[int,int]) -> bool:
        """
        Verifica si mover actual puede avanzar a target:
        - No sale del laberinto.
        - No colisiona con muros ni otras personas.
        - Procesa trampas y retrasadores.
        """
        x, y = posicion_futura

        while x < 0 or x >= self.tamanno or y < 0 or y >= self.tamanno:
            x = random.randint(0, self.tamanno - 1)
            y = random.randint(0, self.tamanno - 1)
        valor = self.matriz[y][x]
        # impedir solapamiento con otras personas
        if valor == PERSONA:
            return False

        if valor == MURO:
            return False
        
        if valor == TRAMPA:
            perdida = persona._perder_movimiento()
            if perdida:
                print(f"\n¡Trampa! Se perdió el movimiento hacia {perdida}.")
            return True
        
        if valor == RETRASADOR:
            self.matriz[y][x] = CAMINO

            if (x, y) in self.retrasador:
                self.retrasador.remove((x, y))
            return False
        
        return True
    
    def _mover_persona(self, persona: Persona) -> Tuple[int,int]:
        """
        Recalcula ruta corta del agente y guía su siguiente paso.
        Actualiza matriz y registra movimiento en su árbol.
        """
        # 1) recalcular ruta más corta para esta persona
        persona.ruta_corta = persona._calcular_ruta_salida_corta(persona.posicion_actual, self.salida)
        ruta = persona.ruta_corta.bfs()

        if len(ruta) < 2:
            return persona.posicion_actual
        
        siguiente = ruta[1]

        # 2) validar celda destino
        if not self._es_posicion_valida(persona, siguiente):
            return persona.posicion_actual
        
        # 3) actualizar matriz: limpiar vieja posición y poner PERSONA
        ox, oy = persona.posicion_actual
        nx, ny = siguiente
        self.matriz[oy][ox] = CAMINO
        self.matriz[ny][nx] = PERSONA
        
        # 4) registrar movimiento en su árbol
        previo = persona.posicion_actual
        persona.posicion_actual = siguiente
        persona.rutas_tomadas.insert(previo, siguiente)
        return siguiente
    
    def _ubicar_bloqueo(self) -> None:
        """Coloca un muro en una celda libre y actualiza árboles."""
        self._verificar_posiciones_libres()

        if not self.posiciones_libres:
            return
        
        idx = random.randint(0, len(self.posiciones_libres) - 1)
        x, y = self.posiciones_libres.pop(idx)
        self.matriz[y][x] = MURO
        self.bloqueo.append((x, y))
        for p in self.personas:
            p.arbol_rutas_todas = p._calcular_arbol_rutas_todas(
                p.posicion_actual, self.salida)

    def _ubicar_trampa(self) -> None:
        self._verificar_posiciones_libres()

        if not self.posiciones_libres:
            return
        
        idx = random.randint(0, len(self.posiciones_libres) - 1)
        x, y = self.posiciones_libres.pop(idx)
        self.matriz[y][x] = TRAMPA
        self.trampas.append((x, y))
        for p in self.personas:
            p.arbol_rutas_todas = p._calcular_arbol_rutas_todas(
                p.posicion_actual, self.salida)

    def _ubicar_retrasador(self) -> None:
        self._verificar_posiciones_libres()

        if not self.posiciones_libres:
            return
        
        idx = random.randint(0, len(self.posiciones_libres) - 1)
        x, y = self.posiciones_libres.pop(idx)
        self.matriz[y][x] = RETRASADOR
        self.retrasador.append((x, y))
        for p in self.personas:
            p.arbol_rutas_todas = p._calcular_arbol_rutas_todas(
                p.posicion_actual, self.salida)

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