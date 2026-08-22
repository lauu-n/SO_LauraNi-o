import threading
import time

TIEMPO_CARRO = 0.05       # Pueba para la real son 30
TAM_LOTE = 10

NOMBRES = [ #Procesos
    "A -> B", # P0
    "B -> A", # P1
    "C -> D",# P2
    "D -> C"# P3
]
carros = [50, 35, 20, 100]


# Recursos del baquero , R0 = intersección horizontal,  R1 = intersección vertical

AVAILABLE = [2, 2]

MAX = [
    [1, 0],       # P0 -> horizontal
    [1, 0],       # P1 -> horizontal
    [0, 1],       # P2 -> vertical
    [0, 1]        # P3 -> vertical
]

ALLOCATION = [
    [0, 0],       # P0
    [0, 0],       # P1
    [0, 0],       # P2
    [0, 0]        # P3
]


lock = threading.RLock() #sincronización

condicion = threading.Condition(lock) #Bloqueo d elos hilos

# Semáforo lógico actual
grupo_actual = "HORIZONTAL"
generacion = 0
ultima_generacion = [-1, -1, -1, -1]
procesos_esperados = 0
procesos_terminados = 0

# Matriz NEED
def calcular_need():

    need = []

    for i in range(4):
        fila = []
        
        for j in range(2):
            fila.append(
                MAX[i][j] - ALLOCATION[i][j]
            )

        need.append(fila)
    return need

#Algoritmo del banquero

def estado_seguro():

    work = AVAILABLE.copy()
    finish = [False, False, False, False]
    need = calcular_need()
    secuencia = []

    while True:
        encontrado = False

        for i in range(4):
            if finish[i]:
                continue
            puede = True

            # Comprobar Need[i] <= Work
            for j in range(2):
                if need[i][j] > work[j]:
                    puede = False
                    break

            if puede:
                for j in range(2):
                    work[j] += ALLOCATION[i][j]
                finish[i] = True
                secuencia.append(i)
                encontrado = True
        if not encontrado:
            break
    return all(finish), secuencia


# Solicitar recursos al banquero
def solicitar_recurso(proceso, recurso):

    with lock:
        # Comprobar disponibiliad
        if AVAILABLE[recurso] <= 0:
            return False
        # Asignación provisional
        AVAILABLE[recurso] -= 1
        ALLOCATION[proceso][recurso] += 1
        # Comprobar estado seguro
        seguro, secuencia = estado_seguro()

        if seguro:
            return True
        # Si el estado no es seguro, deshacer la asignación.
        AVAILABLE[recurso] += 1
        ALLOCATION[proceso][recurso] -= 1

        return False

# Liberar recurso 
def liberar_recurso(proceso, recurso):

    with lock:
        ALLOCATION[proceso][recurso] -= 1
        AVAILABLE[recurso] += 1

# Procesar carros
def procesar(cantidad):

    for _ in range(cantidad):
        time.sleep(TIEMPO_CARRO)

#Horizontal
def proceso_horizontal(indice):
    recurso = 0
    while True:
        with condicion: #Esperar el semaforo horizontal
            while (
                grupo_actual != "HORIZONTAL"
                or ultima_generacion[indice] == generacion
                or carros[indice] <= 0
            ):

                if carros[indice] <= 0:
                    return
                condicion.wait()
            ultima_generacion[indice] = generacion

            # Cantidad que debe procesar
            cantidad = min(
                TAM_LOTE,
                carros[indice]
            )

        while not solicitar_recurso(indice, recurso): #solicitar recurso
            time.sleep(0.01)
            
        procesar(cantidad) #procesar lote
        
        with condicion: #actualizar lote
            carros[indice] -= cantidad
            liberar_recurso(indice, recurso)
            global procesos_terminados
            procesos_terminados += 1
            condicion.notify_all()

#Vertical
def proceso_vertical(indice):
    recurso = 1
    
    while True: #esperar semaforo vertical
        with condicion:
            while (
                grupo_actual != "VERTICAL"
                or ultima_generacion[indice] == generacion
                or carros[indice] <= 0
            ):
                if carros[indice] <= 0:
                    return
                condicion.wait()
            ultima_generacion[indice] = generacion
            cantidad = min( # Cantidad que debe procesar
                TAM_LOTE,
                carros[indice]
            )

        while not solicitar_recurso(indice, recurso):

            time.sleep(0.01)

        procesar(cantidad) #procesar lote

        with condicion: #actualizar

            carros[indice] -= cantidad
            liberar_recurso(indice, recurso)
            global procesos_terminados
            procesos_terminados += 1
            condicion.notify_all()

#mostrar turno

def mostrar_turno(numero, grupo, lotes):
    print(f"\nTURNO {numero}")
    print(f"Semáforo: {grupo} ")
    
    if grupo == "HORIZONTAL":
        print(f"A -> B : {lotes[0]} carros")
        print(f"B -> A : {lotes[1]} carros")
        print("C -> D : espera")
        print("D -> C : espera")

    else:
        print("A -> B : espera")
        print("B -> A : espera")
        print(f"C -> D : {lotes[2]} carros")
        print(f"D -> C : {lotes[3]} carros")

    seguro, secuencia = estado_seguro()

    if seguro:
        print("\nBanquero: ESTADO SEGURO ")

    else:
        print("\nBanquero: ESTADO INSEGURO ")


# Controlador de semaforos
def controlador():
    global grupo_actual
    global generacion
    global procesos_esperados
    global procesos_terminados
    turno = 1

    while True:
        with condicion: #horizontal
            # Comprobar si quedan carros horizontales
            hay_horizontal = (
                carros[0] > 0
                or
                carros[1] > 0
            )

            if hay_horizontal: #Apagar horizontal prender vertical
                grupo_actual = "HORIZONTAL"
                procesos_terminados = 0
                generacion += 1
                # Cuántos procesos realmente tienen carros
                procesos_esperados = 0

                if carros[0] > 0:
                    procesos_esperados += 1

                if carros[1] > 0:
                    procesos_esperados += 1

                lotes = [
                    min(TAM_LOTE, carros[0]),
                    min(TAM_LOTE, carros[1]),
                    0,
                    0
                ]

                mostrar_turno(
                    turno,
                    "HORIZONTAL",
                    lotes
                )
                turno += 1
                # Despertar P0 y P1
                condicion.notify_all()

            else:
                hay_horizontal = False

        if hay_horizontal: #esperar que termine P0 Y P1

            with condicion:
                while procesos_terminados < procesos_esperados:
                    condicion.wait()

        # Vertical
        with condicion:
            # Comprobar si quedan carros verticales
            hay_vertical = (
                carros[2] > 0
                or
                carros[3] > 0
            )

            if hay_vertical: #Apagaar horizontal prender vertical
                grupo_actual = "VERTICAL"
                procesos_terminados = 0
                generacion += 1
                procesos_esperados = 0

                if carros[2] > 0:
                    procesos_esperados += 1

                if carros[3] > 0:
                    procesos_esperados += 1

                lotes = [
                    0,
                    0,
                    min(TAM_LOTE, carros[2]),
                    min(TAM_LOTE, carros[3])
                ]

                mostrar_turno(
                    turno,
                    "VERTICAL",
                    lotes
                )

                turno += 1
                # Despertar P2 y P3
                condicion.notify_all()

            else:
                hay_vertical = False
                
        if hay_vertical: #esperar que terminen P2 Y P3

            with condicion:
                while procesos_terminados < procesos_esperados:
                    condicion.wait()

        with condicion: # Verificar si ya terminaron todos
            if sum(carros) == 0:
                break

    with condicion:  # finalizar semaforo
        grupo_actual = "NINGUNO"
        condicion.notify_all()

# MAIN
def main():
    print("=" * 50)
    print("       ALGORITMO DEL BANQUERO - AUTOPISTA")
    print("=" * 50)
    print("\nCARROS INICIALES")
    print("A -> B : 50")
    print("B -> A : 35")
    print("C -> D : 20")
    print("D -> C : 100")
    print("\nRECURSOS")
    print("R0 = INTERSECCIÓN HORIZONTAL")
    print("R1 = INTERSECCIÓN VERTICAL")
    print("\nAVAILABLE =", AVAILABLE)

    # Estado inicial
    seguro, secuencia = estado_seguro()
    print("\nEstado inicial del sistema:")
    
    if seguro:
        print("SEGURO ✓")

    else:
        print("INSEGURO ✗")

    print("\n" + "=" * 50)
    print("                    EJECUCIÓN")
    print("=" * 50)

    #Crear los 4 hilos
    hilos = [
        threading.Thread( # P0 = A -> B
            target=proceso_horizontal,
            args=(0,)
        ),

        threading.Thread( # P1 = B -> A
            target=proceso_horizontal,
            args=(1,)
        ),
        
        threading.Thread(  # P2 = C -> D
            target=proceso_vertical,
            args=(2,)
        ),

        threading.Thread( # P3 = D -> C
            target=proceso_vertical,
            args=(3,)
        )
    ]

    # Iniciar los 4 hilos
    for hilo in hilos:
        hilo.start()

    controlador()
    #Despertar los hilos
    with condicion:
        condicion.notify_all()

    for hilo in hilos: #Esperar 4 hilos
        hilo.join()

    # Resultado final
    print("\n")
    print("=" * 50)
    print("              ESTADO FINAL")
    print("=" * 50)
    print("\nA -> B : 0")
    print("B -> A : 0")
    print("C -> D : 0")
    print("D -> C : 0")
    print("\nTotal procesados: 205")
    print("Tiempo total teórico: 75 minutos")
    print("\nEstado del sistema: SEGURO ")


if __name__ == "__main__":

    main()