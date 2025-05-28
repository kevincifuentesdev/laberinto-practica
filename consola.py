from laberinto import Laberinto

def mostrar_menu() -> None:
    """Muestra las opciones disponibles para el usuario."""
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
10) Visualizar árbol de todas las rutas posibles
""")

def main():
    """
    Punto de entrada: configura el laberinto, procesa el menú y despliega resultados.
    """
    tamaño = int(input("Ingrese tamaño del laberinto: "))
    lab = Laberinto(tamaño, num_personas=2)
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
                lab.iteracion += 1
                print()
                salida_alcanzada = False
                for idx, persona in enumerate(lab.personas, 1):
                    pos = lab._mover_persona(persona)
                    print(f"Persona {idx} → {pos}")
                    if pos in lab.salida:
                        print(f"¡Persona {idx} llegó a la salida!")
                        salida_alcanzada = True
                        break
                print(); print(lab); print()
                if salida_alcanzada:
                    break
            else:
                print("Debe iniciar simulación primero.")
                print("\n")
        elif opc == "7":
            print("Saliendo...")
            break
        elif opc == "8":
            if iniciado:
                for idx, p in enumerate(lab.personas, 1):
                    print(f"\nÁrbol movimientos Persona {idx}:")
                    p.rutas_tomadas.display()
                print("\n")
            else:
                print("Debe iniciar simulación primero.\n")
        elif opc == "9":
            if iniciado:
                for idx, p in enumerate(lab.personas, 1):
                    p.ruta_corta = p._calcular_ruta_salida_corta(p.posicion_actual, lab.salida)
                    print(f"\nÁrbol ruta más corta Persona {idx}:")
                    p.ruta_corta.display()
                print("\n")
            else:
                print("Debe iniciar simulación primero.\n")
        elif opc == "10":
            if iniciado:
                for idx, p in enumerate(lab.personas, 1):
                    p.arbol_rutas_todas = p._calcular_arbol_rutas_todas(
                        p.posicion_actual, lab.salida)
                    print(f"\nÁrbol todas rutas Persona {idx}:")
                    p.arbol_rutas_todas.display()
                print("\n")
            else:
                print("Debe iniciar simulación primero.\n")
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
