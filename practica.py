import random
from arbol_general import GeneralTree, Node


muro = "X"
trampa = "T"
retrasador = "R"
personaje = "P"
camino = '.'
salida = 'S'


class Laberinto:
    def __init__(self):
     self.size: int = 5
     self.laberinto = self.crear_matriz()
     self.cantidad_salidas = 2
     self.salidas: list[tuple] = self.definir_salidas()
     self.personajes: list = []
     self.posiciones_libres = []
     
        
    def crear_matriz(self):
        matriz = []
        for i in range(self.size):
            fila =[]
            for j in range(self.size):
                fila.append(camino)
        
            matriz.append(fila)
        return matriz
     
    def definir_salidas(self):
        cantidad_salidas = self.cantidad_salidas
        salidas = []
        while cantidad_salidas > 0:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)

                if self.laberinto[x][y] == camino:
                    self.laberinto[x][y] = salida
                    salidas.append((x, y))
                    cantidad_salidas -= 1
        return salidas
    
        
    def iniciar_personaje(self):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.laberinto[x][y] == camino:
                self.laberinto[x][y] = personaje
                nuevo = Personaje((x, y)) 
                self.personajes.append(nuevo)
                return (x, y) 
            


    def verificar_posiciones_libres(self) -> None:
        libres: list[tuple[int, int]] = []
        
        for x in range(self.tamanno):

            for y in range(self.tamanno):

                if self.matriz[x][y] == camino:
                    libres.append((x, y))
                    
                
    def __repr__(self):
        return '\n'.join(' '.join(str(cell) for cell in fila) for fila in self.laberinto)

    
            
            
    
    
class Personaje:
    def __init__(self, posicion):
     self.posicion: tuple = posicion 
     self.direcciones: list[tuple] = [(0,1),(1,0),(0,-1),(-1,0)]
     self.arbol_decision = []
     self.rutas = []
     self.ruta_mas_corta = []
     
    
    def calcular_todas_las_rutas(self, laberinto: Laberinto, posicion_inicio: tuple, 
                                 salidas: list[tuple]) -> GeneralTree:
        
        arbol = GeneralTree()
        arbol.root = Node(posicion_inicio)
        len_laberinto = laberinto.size
        
        
    
    



    
def iniciar_simulacion():
    laberinto = Laberinto()
    laberinto.iniciar_personaje()
    laberinto.iniciar_personaje()
    print(laberinto)
    
    
iniciar_simulacion()