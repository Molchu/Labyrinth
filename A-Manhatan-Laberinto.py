import turtle
import random
from collections import deque

# Crear un enlace entre dos nodos
def crear_enlace(nodo1, nodo2):
    nodo1.adjacent.append(nodo2)
    nodo2.adjacent.append(nodo1)

# Encontrar el conjunto al que pertenece un nodo
def encontrar_conjunto(nodo):
    if nodo.conjunto != nodo:
        nodo.conjunto = encontrar_conjunto(nodo.conjunto)
    return nodo.conjunto

# Función para unir dos conjuntos en uno
def unir_conjuntos(conjunto1, conjunto2):
    if conjunto1.rank > conjunto2.rank:
        conjunto2.conjunto = conjunto1
    elif conjunto1.rank < conjunto2.rank:
        conjunto1.conjunto = conjunto2
    else:
        conjunto2.conjunto = conjunto1
        conjunto1.rank += 1

#---->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Función de heurística: Distancia de Manhattan
def distancia_manhattan(nodo1, nodo2):
    return abs(nodo1.x - nodo2.x) + abs(nodo1.y - nodo2.y)

# Definición de la clase Nodo
class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.adjacent = []
        self.conjunto = self
        self.rank = 0

# Configuración de la ventana de Turtle
ventana = turtle.Screen()
ventana.title("Laberinto Usando Heuristica y Turtle")
ventana.bgcolor("white")
ventana.setup(width=700, height=700)

# Tamaño de la cuadrícula y tamaño de las celdas
filas, columnas = 10, 10
tamaño_celda = 30

# Crear una lista de nodos
nodos = []
for fila in range(filas):
    for columna in range(columnas):
        nodo = Nodo(columna, fila)
        nodos.append(nodo)

# Algoritmo de Kruskal para generar el laberinto
enlaces = []
for nodo in nodos:
    if nodo.x > 0:
        enlaces.append((nodo, nodos[nodo.y * columnas + nodo.x - 1], random.randint(1, 100)))
    if nodo.y > 0:
        enlaces.append((nodo, nodos[(nodo.y - 1) * columnas + nodo.x], random.randint(1, 100)))

enlaces.sort(key=lambda enlace: enlace[2])
laberinto = []

for enlace in enlaces:
    nodo1, nodo2, peso = enlace
    conjunto1 = encontrar_conjunto(nodo1)
    conjunto2 = encontrar_conjunto(nodo2)

    if conjunto1 != conjunto2:
        unir_conjuntos(conjunto1, conjunto2)
        laberinto.append(enlace)
        crear_enlace(nodo1, nodo2)

# Función para dibujar una línea entre dos nodos
def dibujar_linea(nodo1, nodo2):
    x1 = nodo1.x * tamaño_celda
    y1 = -nodo1.y * tamaño_celda
    x2 = nodo2.x * tamaño_celda
    y2 = -nodo2.y * tamaño_celda
    laberinto_turtle.penup()
    laberinto_turtle.goto(x1, y1)
    laberinto_turtle.pendown()
    laberinto_turtle.goto(x2, y2)

# Dibujar el laberinto
laberinto_turtle = turtle.Turtle()
laberinto_turtle.speed(0)
laberinto_turtle.color("black")
laberinto_turtle.pensize(2)

for nodo1, nodo2, _ in laberinto:
    dibujar_linea(nodo1, nodo2)

# Dibujar la entrada (nodo inicial)
entrada = nodos[0]
laberinto_turtle.penup()
laberinto_turtle.goto(entrada.x * tamaño_celda, -entrada.y * tamaño_celda)
laberinto_turtle.pendown()
laberinto_turtle.dot(10, "green")

# Dibujar la salida (nodo final)
salida = nodos[-1]
laberinto_turtle.penup()
laberinto_turtle.goto(salida.x * tamaño_celda, -salida.y * tamaño_celda)
laberinto_turtle.pendown()
laberinto_turtle.dot(10, "red")

# Coordenadas de inicio y objetivo para A* con heurística
inicio = nodos[0]
objetivo = nodos[-1]

# Función para resolver el laberinto utilizando A* con heurística
def resolver_laberinto_astar_manhattan(inicio, objetivo):
    queue = deque()
    queue.append((inicio, []))

    while queue:
        nodo_actual, camino = queue.popleft()
        if nodo_actual == objetivo:
            return camino + [nodo_actual]

        # Calcular la heurística (distancia de Manhattan) desde el nodo actual al objetivo
        heuristica = distancia_manhattan(nodo_actual, objetivo)

        for vecino in nodo_actual.adjacent:
            if vecino not in camino:
                # Calcular el costo (g) desde el nodo inicial hasta el vecino
                costo_g = len(camino) + 1

                # Calcular el costo total (f) usando la heurística
                costo_f = costo_g + heuristica

                # Agregar el vecino y el camino al vecino a la cola de prioridad
                queue.append((vecino, camino + [nodo_actual]))

        # Ordenar la cola de prioridad por costo total (f)
        queue = deque(sorted(queue, key=lambda x: distancia_manhattan(x[0], objetivo)))

    # Si no se encuentra una solución, regresar None
    return None

# Resolver el laberinto utilizando A* con heurística de distancia de Manhattan
solucion_astar_manhattan = resolver_laberinto_astar_manhattan(inicio, objetivo)

if solucion_astar_manhattan:
    print("Se encontró una solución utilizando A* con heurística de distancia de Manhattan:")
    for i in range(len(solucion_astar_manhattan) - 1):
        nodo1 = solucion_astar_manhattan[i]
        nodo2 = solucion_astar_manhattan[i + 1]
        dibujar_linea(nodo1, nodo2)
else:
    print("No se encontró una solución utilizando A* con heurística de distancia de Manhattan.")

# Cerrar la ventana de Turtle al hacer clic
ventana.exitonclick()