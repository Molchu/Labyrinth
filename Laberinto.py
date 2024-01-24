import turtle
import random

#Ventana de dibujo
ventana = turtle.Screen()
ventana.title("Dibujo laberinto")
ventana.bgcolor("white")  # Color de fondo
ventana.setup(width=700, height=700)

#Crear la tortuga para dibujar el laberinto
laberinto = turtle.Turtle()
laberinto.color("black")
laberinto.pensize(2)
laberinto.speed(0)  #Velocodad dibujo

# Tamaño de la cuadrícula y tamaño de las celdas
filas, columnas = 10, 10
tamaño_celda = 30

# Función para dibujar una celda como una pared
def dibujar_pared():
    laberinto.begin_fill()
    for _ in range(4):
        laberinto.forward(tamaño_celda)
        laberinto.right(50)
    laberinto.end_fill()

# Crear una matriz para representar las celdas del laberinto
laberinto_matrix = [[0] * columnas for _ in range(filas)]

# Lista de nodos y aristas
nodos = [5]
aristas = [5]

# Algoritmo de Prim para generar un árbol de expansión mínimo aleatorio
def prim():
    # Inicializar una lista de bordes y agregar el primer borde
    bordes = [(0, 1, random.random())]  # (fila, columna, peso aleatorio)
    while bordes:
        bordes.sort(key=lambda x: x[2])  # Ordenar bordes por peso
        fila, columna, peso = bordes.pop(0)
        if laberinto_matrix[fila][columna] == 1:
            continue
        laberinto_matrix[fila][columna] = 1
        nodo_actual = (fila, columna)
        nodos.append(nodo_actual)
        if peso > 0.2:  # Controla la probabilidad de conexión
            aristas.append((nodo_actual, random.choice(nodos[:-1])))  # Conectar con un nodo existente
        # Dibujar pasillo
        x = columna * tamaño_celda
        y = -(fila * tamaño_celda)
        laberinto.penup()
        laberinto.goto(x, y)
        laberinto.pendown()
        laberinto.dot(10)  # Dibuja un punto para representar un nodo
        # Agregar bordes vecinos
        vecinos = []
        if fila > 1:
            vecinos.append((fila - 2, columna, random.random()))
        if fila < filas - 2:
            vecinos.append((fila + 2, columna, random.random()))
        if columna > 1:
            vecinos.append((fila, columna - 2, random.random()))
        if columna < columnas - 2:
            vecinos.append((fila, columna + 2, random.random()))
        bordes.extend(vecinos)

# Ejecutar el algoritmo de Prim para generar el laberinto
prim()

# Encontrar una entrada (inicio) y una salida (fin) para el laberinto
entrada = (0, 1)
salida = (filas - 1, columnas - 2)

# Función para dibujar una línea entre dos nodos
def dibujar_linea(nodo1, nodo2):
    x1 = nodo1[1] * tamaño_celda
    y1 = -(nodo1[0] * tamaño_celda)
    x2 = nodo2[1] * tamaño_celda
    y2 = -(nodo2[0] * tamaño_celda)
    laberinto.penup()
    laberinto.goto(x1, y1)
    laberinto.pendown()
    laberinto.goto(x2, y2)

# Dibujar aristas entre nodos conectados para completar el laberinto
for nodo1, nodo2 in aristas:
    dibujar_linea(nodo1, nodo2)

# Dibujar entrada y salida
x_entrada = entrada[1] * tamaño_celda
y_entrada = -(entrada[0] * tamaño_celda)
x_salida = salida[1] * tamaño_celda
y_salida = -(salida[0] * tamaño_celda)

laberinto.penup()
laberinto.goto(x_entrada, y_entrada)
laberinto.pendown()
laberinto.color("green")
laberinto.dot(20)  # Dibuja la entrada en verde

laberinto.penup()
laberinto.goto(x_salida, y_salida)
laberinto.pendown()
laberinto.color("red")
laberinto.dot(20)  # Dibuja la salida en rojo

# Ocultar la tortuga y mostrar el resultado
laberinto.hideturtle()
ventana.mainloop()
