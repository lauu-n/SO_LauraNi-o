# ACTIVIDAD I
## Algoritmo del Banquero

---

### Ejecución en Linux (Terminal)

1. Verificar que Python esté instalado.
```
$ python3 --version
```
2. Descargar el archivo *semaforo_algoritmo_banquero.py*.
3. Ubicarse en la carpeta donde se descargó el archivo:
```
$ cd "ubicación"
```
4. Ejecutar el archivo:
```
$ python3 semaforo_algoritmo_banquero.py
```
<img width="614" height="97" alt="image" src="https://github.com/user-attachments/assets/daf26a72-c3ac-4a27-b88d-d595a59d150d" />

---

### Resultados

- De ejecución:
```
laun@Nino-Rosas:~/SO/actividad_I$ python3 semaforo_algoritmo_banquero.py
==================================================
       ALGORITMO DEL BANQUERO - AUTOPISTA
==================================================

CARROS INICIALES
A -> B : 50
B -> A : 35
C -> D : 20
D -> C : 100

RECURSOS
R0 = INTERSECCIÓN HORIZONTAL
R1 = INTERSECCIÓN VERTICAL

AVAILABLE = [2, 2]

Estado inicial del sistema:
SEGURO ✓

==================================================
                    EJECUCIÓN
==================================================

TURNO 1
Semáforo: HORIZONTAL 
A -> B : 10 carros
B -> A : 10 carros
C -> D : espera
D -> C : espera

Banquero: ESTADO SEGURO 

TURNO 2
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 10 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 3
Semáforo: HORIZONTAL 
A -> B : 10 carros
B -> A : 10 carros
C -> D : espera
D -> C : espera

Banquero: ESTADO SEGURO 

TURNO 4
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 10 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 5
Semáforo: HORIZONTAL 
A -> B : 10 carros
B -> A : 5 carros
C -> D : espera
D -> C : espera

Banquero: ESTADO SEGURO 

TURNO 6
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 7
Semáforo: HORIZONTAL 
A -> B : 10 carros
B -> A : 0 carros
C -> D : espera
D -> C : espera

Banquero: ESTADO SEGURO 

TURNO 8
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 9
Semáforo: HORIZONTAL 
A -> B : 10 carros
B -> A : 0 carros
C -> D : espera
D -> C : espera

Banquero: ESTADO SEGURO 

TURNO 10
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 11
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 12
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 13
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 14
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 15
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 

TURNO 16
Semáforo: VERTICAL 
A -> B : espera
B -> A : espera
C -> D : 0 carros
D -> C : 10 carros

Banquero: ESTADO SEGURO 


==================================================
              ESTADO FINAL
==================================================

A -> B : 0
B -> A : 0
C -> D : 0
D -> C : 0

Total procesados: 205
Tiempo total teórico: 75 minutos

Estado del sistema: SEGURO 
```

---

### Algoritmo del Banquero aplicado

**0. ¿Qué es y cómo se aplica?**

- Es un algoritmo de control de concurrencia y deadlock (bloqueo mutuo) usado en sistemas operativos. Su objetivo es evitar que el sistema entre en un estado de deadlock asignando recursos de manera segura a los procesos.
     Funciona como un banquero que controla préstamos: antes de otorgar recursos a un proceso, el banquero verifica que el sistema pueda seguir siendo "seguro" (es decir, que todos los procesos puedan completarse eventualmente).

 - Conceptos clave:
    - Recursos: Son elementos limitados del sistema (memoria, procesadores, archivos, etc.)
    - Procesos: Son tareas que necesitan recursos para ejecutarse.
    - Estado seguro: Un estado donde existe un orden de ejecución de procesos tal que todos pueden completarse sin deadlock.
    - Estado inseguro: No existe tal orden, por lo que podría haber deadlock.

  - ¿Cómo funciona?
       Verifica antes de asignar cada recurso:
       1. Puede este proceso terminar con los recursos que tiene ahora?
       2. Si le doy el recurso solicitado, ¿seguirá habiendo un camino seguro para todos?
       3. Si la respuesta es SÍ → asigna el recurso.
       4. Si la respuesta es NO → rechaza o espera.
       
  - Aplicación:
    - Asignación segura de memoria.
    - Control de acceso a dispositivos.
    - Gestión de procesos concurrentes.
    - Prevención de deadlocks en sistemas multitarea.

**1. Datos del problema**
   Tiempo que tarda cada carro en cambiar de sentido: 30 segundos.
   
   |     Dato     | Valor |
   |--------------|-------|
   | Carros A → B |   50  |
   | Carros B → A |   35  |
   | Carros C → D |   20  |
   | Carros D → C |   100 |
   |    Total     |   205 |

<img width="1365" height="767" alt="image" src="https://github.com/user-attachments/assets/c12c592f-dad9-4ae1-bf2d-3d9af6124c6e" />


**2. Matriz de procesos**
   Reconocer cada sentido como un proceso.
   
   | Proceso | Sentido | Cantidad de carros |
   |---------|---------|--------------------|
   |   P0    |  A → B  |         50         |
   |   P1    |  B → A  |         35         |
   |   P2    |  C → D  |         20         |
   |   P3    |  D → C  |         100        |
   
**3. Matriz de recurso**
   Los recursos representan los cuatro carriles que tenemos en la intersección.
   
   | Recurso | Representa | Capacidad |
   |---------|------------|-----------|
   |   P0    |    A → B   |     1     |
   |   P1    |    B → A   |     1     |
   |   P2    |    C → D   |     1     |
   |   P3    |    D → C   |     1     |

   La capacidad es 1 porque, un carro demora 30 segundos en pasar de un lado al otro, por lo que no puede entrar otro carro en ese mismo sentido durante ese período de tiempo.

**4. Matriz Max**
   Indica el máximo recurso que necesita cada proceso.
   
   |  Proceso | R1 A→B | R2 B→A | R3 C→D | R4 D→C |
   |----------|--------|--------|--------|--------|
   | P0 A → B |    1   |    0   |    0   |    0   |
   | P1 B → A |    0   |    1   |    0   |    0   |
   | P2 C → D |    0   |    0   |    1   |    0   |
   | P3 D → C |    0   |    0   |    0   |    1   |
   
**5. Matriz Allocation Inicial**
   Al comenzar, ningún carro está dentro de la intersección.
   
   |  Proceso | R1 A→B | R2 B→A | R3 C→D | R4 D→C |
   |----------|--------|--------|--------|--------|
   | P0 A → B |    0   |    0   |    0   |    0   |
   | P1 B → A |    0   |    0   |    0   |    0   |
   | P2 C → D |    0   |    0   |    0   |    0   |
   | P3 D → C |    0   |    0   |    0   |    0   |

**6. Matriz Need**
   La fórmula:
   ```
   NEED = MAX - ALLOCATION
   ```

   Por tanto:
   
   |  Proceso | R1 A→B | R2 B→A | R3 C→D | R4 D→C |
   |----------|--------|--------|--------|--------|
   | P0 A → B |    1   |    0   |    0   |    0   |
   | P1 B → A |    0   |    1   |    0   |    0   |
   | P2 C → D |    0   |    0   |    1   |    0   |
   | P3 D → C |    0   |    0   |    0   |    1   |

**7. Vector AVAILABLE**
   Al inicio, todos los recursos están libres.
   
   | R1 A→B | R2 B→A | R3 C→D | R4 D→C |
   |--------|--------|--------|--------|
   |    1   |    1   |    1   |    1   |

   Entonces:
   *Available = (1, 1, 1, 1)**

**8. Tabla de comprobación del Banquero**
   ```
   Need ≤ Work
   ```

   Al principio:
   ```
   Work = Available = (1, 1, 1, 1)
   ```

   |  Paso | Proceso | Need del proceso | Work antes | ¿Need ≤ Work? | Work después |
   |-------|---------|------------------|------------|---------------|--------------|
   |   1   |    P0   |     (1,0,0,0)    |  (1,1,1,1) |       Sí      |   (1,1,1,1)  |
   |   2   |    P1   |     (0,1,0,0)    |  (1,1,1,1) |       Sí      |   (1,1,1,1)  |
   |   3   |    P2   |     (0,0,1,0)    |  (1,1,1,1) |       Sí      |   (1,1,1,1)  |
   |   4   |    P3   |     (0,0,0,1)    |  (1,1,1,1) |       Sí      |   (1,1,1,1)  |

   El sistema funciona correctamente aunque no es la única manera de funcionar.

**9. Dos semáforos, cada uno controlará un sentido, horizontal y vertical, respectivamente.**

   | Semáforo |  Controla  | Estado |
   |----------|------------|--------|
   |    S1    | Horizontal |   0/1  |
   |    S2    |  Vertical  |   0/1  |

   Solo puede estar uno activo a la vez.

**10. Carros por fase horizontal**
    - A→B: 50 carros
    - B→A: 35 carros
    Se necesitan como máximo 50 turnos horizontales.

   | Fase | A→B | B→A | Duración (s)|
   |------|-----|-----|-------------|
   |  H1  |  1  |  1  |      30     |
   |  H2  |  1  |  1  |      30     |
   |  H3  |  1  |  1  |      30     |
   |  ..  |  .  |  .  |      ..     |
   |  H35 |  1  |  1  |      30     |
   |  H36 |  1  |  0  |      30     |
   |  ..  |  .  |  .  |      ..     |
   |  H50 |  1  |  0  |      30     |

   Resultado:
   ```
   50 · 30 = 1500 segundos = 25 minutos
   ```   
   Así que al terminar los 50 turnos, todos los carros habrán pasado al otro lado.

**11. Carros por fase vertical**
    - C→D: 20 carros
    - D→C: 100 carros
    Se necesitan 100 turnos verticales.

   | Fase  | C→D | D→C | Duración (s)|
   |-------|-----|-----|-------------|
   |  V1   |  1  |  1  |      30     |
   |  V2   |  1  |  1  |      30     |
   |  ..   |  .  |  .  |      ..     |
   |  V20  |  1  |  1  |      30     |
   |  V21  |  1  |  0  |      30     |
   |  ..   |  .  |  .  |      ..     |
   |  V100 |  1  |  0  |      30     |

   Resultado:
   ```
   50 · 30 = 1500 segundos = 25 minutos
   ```   
   Así que al terminar los 50 turnos, todos los carros habrán pasado al otro lado.

**12. Resumen de tiempos**
    
   |    Grupo   |  Carros | Turnos | Tiempo (minutos) |
   |------------|---------|--------|------------------|
   | Horizontal | 50 + 35 |   50   |         25       |
   |  Vertical  | 50 + 35 |   100  |         50       |
   |    Total   | 50 + 35 |   150  |         75       |
   
   En este caso, hay 150 turnos porque dos carros pueden pasar simultáneamente cuando van en sentidos opuestos (A→B + B→A y C→D + D→C). Por consiguiente, la cantidad de turnos será menor que la cantidad de vehículos.

**13. Tabla de ejecución propuesta**
  - Se utilizan intervalos de 10 carros por sentido hasta finalizar las colas, con el objetivo de disminuir el tiempo de espera. De esta manera, los vehículos que circulan en sentido vertical no tienen que esperar a que todos los vehículos del sentido horizontal terminen de pasar, sino que ambos grupos van alternando su paso.

   | Fase | Semáforo verde | A→B | B→A | C→D | D→C | Tiempo (minutos)|
   |------|----------------|-----|-----|-----|-----|-----------------|
   |   1  |  S1 Horizontal |  10 |  10 |  0  |  0  |        5        |
   |   2  |   S2 Vertical  |  0  |  0  |  10 |  10 |        5        |
   |   3  |  S1 Horizontal |  10 |  10 |  0  |  0  |        5        |
   |   4  |   S2 Vertical  |  0  |  0  |  10 |  10 |        5        |
   |   5  |  S1 Horizontal |  10 |  10 |  0  |  0  |        5        |
   |   6  |   S2 Vertical  |  0  |  0  |  0  |  10 |        5        |
   |   7  |  S1 Horizontal |  10 |  5  |  0  |  0  |        5        |
   |   8  |   S2 Vertical  |  0  |  0  |  0  |  10 |        5        |
   |   9  |  S1 Horizontal |  10 |  0  |  0  |  0  |        5        |
   |  10  |   S2 Vertical  |  0  |  0  |  0  |  10 |        5        |
   |  11  |   S2 Vertical  |  0  |  0  |  0  |  10 |        5        |
   |  12  |   S2 Vertical  |  0  |  0  |  0  |  10 |        5        |
   |  13  |   S2 Vertical  |  0  |  0  |  0  |  10 |        5        |
   |  14  |   S2 Vertical  |  0  |  0  |  0  |  10 |        5        |
   |  15  |   S2 Vertical  |  0  |  0  |  0  |  10 |        5        |
   |   .  |      Total     |  50 |  35 |  20 | 100 |        75       |


   - El mejor código.
     
   |   Elemento   |              Representación                    |
   |--------------|------------------------------------------------|
   |      P0      |                Hilo A → B                      |
   |      P1      |                Hilo B → A                      |
   |      P2      |                Hilo C → D                      |
   |      P3      |                Hilo D → C                      |
   |      R0      |          Intersección horizontal               |
   |      R1      |           Intersección vertical                |   
   |   Banquero   | Decide si una solicitud deja el sistema seguro |
   |   Semáforos  |      Controlan horizontal / vertical           |
   |     Lote     |             Máximo 10 carros                   |
   |    Tiempo    |          30 segundos por carro                 |

**14. Implementación mediante hilos**
    Se utilizaron cuatro (4) hilos.

   | Hilo | Sentido |
   |------|---------|
   |  P0  |  A → B  |
   |  P1  |  B → A  |
   |  P2  |  C → D  |
   |  P3  |  D → C  |

   - Los hilos permanecen activos durante toda la simulación, pero solo pueden ejecutarse cuando su semáforo está en verde. Los demás quedan bloqueados mediante una *Condition*.
   - La circulación se realiza en lotes de 10 carros. El controlador espera a que los hilos del turno terminen su lote antes de cambiar el semáforo. Así, los sentidos horizontales pueden circular simultáneamente y lo mismo ocurre con los verticales, pero horizontal y vertical nunca circulan al mismo tiempo.
   - El Algoritmo del Banquero verifica que la asignación de los recursos mantenga el sistema en un estado seguro.

---

#### Integrantes

- Carol Mariana Arenas Cardona
- Yeimy Estefanía Beltrán Sandoval
- Laura Valentina Niño Rosas
