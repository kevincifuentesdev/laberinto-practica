from typing import List
import random
import heapq

# Constantes
muro = "X"
trampa = "T"
retrasador = "R"
personaje = "P"
camino = '.'
salida = 'S'

class PriorityQueue:
    def __init__(self):
        self.data = []

    def push(self, item):
        heapq.heappush(self.data, item)

    def pop(self):
        return heapq.heappop(self.data)

    def __len__(self):
        return len(self.data)

class Laberinto:
    def __init__(self, size=5, num_personas=1, num_salidas=2):
        self.size = size
        self.laberinto = self._crear_matriz()
        self.cantidad_salidas = num_salidas
        self.salidas = self._definir_salidas()
        self.personas = []
        self.num_personas = num_personas

    def _crear_matriz(self):
        return [[camino for _ in range(self.size)] for _ in range(self.size)]

    def _definir_salidas(self):
        sal, cnt = [], self.cantidad_salidas
        while cnt > 0:
            x, y = random.randrange(self.size), random.randrange(self.size)
            if self.laberinto[x][y] == camino:
                self.laberinto[x][y] = salida
                sal.append((x, y))
                cnt -= 1
        return sal

    def iniciar_laberinto(self):
        for _ in range(self.num_personas):
            p = self._iniciar_personaje()
            self.personas.append(p)

    def _iniciar_personaje(self):
        while True:
            x, y = random.randrange(self.size), random.randrange(self.size)
            if self.laberinto[x][y] == camino:
                self.laberinto[x][y] = personaje
                return Personaje((x, y))

    def _ubicar_elemento(self, elem):
        while True:
            x, y = random.randrange(self.size), random.randrange(self.size)
            if self.laberinto[x][y] == camino:
                self.laberinto[x][y] = elem
                break

    def _ubicar_bloqueo(self):
        self._ubicar_elemento(muro)

    def _ubicar_trampa(self):
        self._ubicar_elemento(trampa)

    def _ubicar_retrasador(self):
        self._ubicar_elemento(retrasador)

    def _mover_persona(self, persona):
        if not persona.ruta_mas_corta:
            return persona.posicion
        persona.ruta_mas_corta.pop(0)
        nx, ny = persona.ruta_mas_corta[0]
        px, py = persona.posicion
        if (px, py) in self.salidas:
            self.laberinto[px][py] = salida
        else:
            self.laberinto[px][py] = camino
        persona.posicion = (nx, ny)
        self.laberinto[nx][ny] = personaje
        return persona.posicion

    def __repr__(self):
        return "\n".join(" ".join(fila) for fila in self.laberinto)

class Personaje:
    def __init__(self, posicion):
        self.posicion = posicion
        self.direcciones = [(1,0), (0,1), (-1,0), (0,-1)]
        self.ruta_mas_corta: List[tuple] = []

    def obtener_ruta_mas_corta(self, lab: Laberinto):
        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.push((0, self.posicion, [self.posicion]))  

        while priority_queue:
            costo, posicion, ruta = priority_queue.pop()
            if posicion in visited:
                continue
            visited.add(posicion)
            if posicion in lab.salidas:
                self.ruta_mas_corta = ruta
                return
            x, y = posicion
            for dx, dy in self.direcciones:
                nx, ny = x + dx, y + dy
                if 0 <= nx < lab.size and 0 <= ny < lab.size:
                    valor = lab.laberinto[nx][ny]
                    if valor != muro and (nx, ny) not in visited:
                        priority_queue.push((costo + 1, (nx, ny), ruta + [(nx, ny)]))

        self.ruta_mas_corta = []  

def mostrar_menu():
    print("1) Iniciar simulación")
    print("2) Agregar muro")
    print("3) Agregar trampa")
    print("4) Agregar retrasador")
    print("5) Mostrar laberinto")
    print("6) Avanzar iteración")
    print("7) Salir")
    print("9) Ver ruta más corta")

def main():
    tamaño = int(input("Tamaño del laberinto: "))
    num_p = int(input("Número de personajes: "))
    lab = Laberinto(tamaño, num_personas=num_p)
    iniciado = False

    while True:
        mostrar_menu()
        opc = input("Opción: ").strip()

        if opc == "1":
            lab.iniciar_laberinto()
            iniciado = True
            print("\n" + str(lab) + "\n")

        elif opc in {"2", "3", "4"}:
            if not iniciado:
                print("Debe iniciar primero.\n")
                continue
            if opc == "2": lab._ubicar_bloqueo()
            if opc == "3": lab._ubicar_trampa()
            if opc == "4": lab._ubicar_retrasador()
            print("Elemento agregado.\n")

        elif opc == "5":
            print("\n" + str(lab) + "\n")

        elif opc == "6":
            if not iniciado:
                print("Debe iniciar primero.\n")
                continue

            eliminados = []
            for p in lab.personas:
                p.obtener_ruta_mas_corta(lab)

                if not p.ruta_mas_corta or len(p.ruta_mas_corta) < 2:
                    print(f"Persona en {p.posicion} ya alcanzó su destino o no tiene ruta.")
                    eliminados.append(p)
                    continue

                p.ruta_mas_corta.pop(0)
                nueva_pos = p.ruta_mas_corta[0]
                px, py = p.posicion
                if (px, py) in lab.salidas:
                    lab.laberinto[px][py] = salida
                else:
                    lab.laberinto[px][py] = camino
                nx, ny = nueva_pos
                p.posicion = (nx, ny)
                lab.laberinto[nx][ny] = personaje

                print(f"Persona se movió a {nueva_pos}")

                if (nx, ny) in lab.salidas:
                    print(f"🎉 Persona llegó a la salida en {nx, ny} y ha sido eliminada.")
                    lab.laberinto[nx][ny] = salida
                    eliminados.append(p)

            for p in eliminados:
                lab.personas.remove(p)

            print("\n" + str(lab) + "\n")

            if not lab.personas:
                print("✅ Todos los personajes han salido del laberinto. Simulación terminada.")
                break

        elif opc == "7":
            print("Saliendo...")
            break

        elif opc == "9":
            if not iniciado:
                print("Debe iniciar primero.\n")
                continue
            for i, p in enumerate(lab.personas, 1):
                p.obtener_ruta_mas_corta(lab)
                print(f"\nRuta más corta Persona {i}:")
                print(p.ruta_mas_corta)
            print()

        else:
            print("Opción inválida.\n")

if __name__ == "__main__":
    main()
