from laberinto import Laberinto

def mostrar_menu() -> None:
    print("""
1) Iniciar simulación
2) Colocar bloqueo
3) Colocar trampa
4) Colocar retrasador
5) Visualizar laberinto
6) Ejecutar siguiente iteración
7) Salir
8) Visualizar árbol de movimientos
9) Visualizar árbol de ruta más corta
""")

def main():
    tamaño = int(input("Ingrese tamaño del laberinto: "))
    lab = Laberinto(tamaño)
    iniciado = False

    while True:
        mostrar_menu()
        opc = input("Seleccione opción: ").strip()
        if opc == "1":
            lab.iniciar_laberinto()
            iniciado = True
            print("Simulación iniciada.")
            print("\n")
            print(lab)
            print("\n")
        elif opc == "2":
            if iniciado:
                lab._ubicar_bloqueo()
                print("Bloqueo agregado.")
                print("\n")
            else:
                print("Debe iniciar simulación primero.")
                print("\n")
        elif opc == "3":
            if iniciado:
                lab._ubicar_trampa()
                print("Trampa agregada.")
                print("\n")
            else:
                print("Debe iniciar simulación primero.")
                print("\n")
        elif opc == "4":
            if iniciado:
                lab._ubicar_retrasador()
                print("Retrasador agregado.")
                print("\n")
            else:
                print("Debe iniciar simulación primero.")
                print("\n")
        elif opc == "5":
            print("\n")
            print(lab)
            print("\n")
        elif opc == "6":
            if iniciado:
                pos = lab._mover_persona()
                lab.iteracion += 1
                print("\n")
                print(lab)
                print("\n")
                print(f"Iteración {lab.iteracion}: persona en {pos}")
                if pos == lab.salida:
                    print("¡La persona llegó a la salida!")
                    break
            else:
                print("Debe iniciar simulación primero.")
                print("\n")
        elif opc == "7":
            print("Saliendo...")
            break
        elif opc == "8":
            if iniciado:
                print("\nÁrbol de movimientos tomados:")
                lab.persona.rutas_tomadas.display()
                print("\n")
            else:
                print("Debe iniciar simulación primero.\n")
        elif opc == "9":
            if iniciado:
                # Recalcular árbol de ruta corta según el laberinto actual
                lab.persona.ruta_corta = lab.persona._calcular_ruta_corta(lab.persona.posicion_actual)
                print("\nÁrbol de ruta más corta:")
                lab.persona.ruta_corta.display()
                print("\n")
            else:
                print("Debe iniciar simulación primero.\n")
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
