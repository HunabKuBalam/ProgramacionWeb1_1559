import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

class Arbol:
    def __init__(self, n):
        self.n = n
        self.nodos = [Nodo(i) for i in range(1, n + 1)]

    def agregar_arista(self, x, y):
        self.nodos[x - 1].hijos.append(self.nodos[y - 1])
        self.nodos[y - 1].hijos.append(self.nodos[x - 1])

    def mostrar_grafo(self):
        for fila in self.matriz_adyacencia:
            print(fila)

    def visualizar_grafo_grafico(self, titulo):
        G = nx.Graph()
        for nodo in self.nodos:
            for hijo in nodo.hijos:
                G.add_edge(nodo.valor, hijo.valor)
        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', width=1)
        plt.title(titulo)
        plt.show()

def leer_entrada():
    datos = entry_datos.get("1.0", "end-1c").split()
    n = int(datos[0])
    r = int(datos[1])
    arbol = Arbol(n)
    indice = 2
    for _ in range(n - 1):
        x = int(datos[indice])
        y = int(datos[indice + 1])
        arbol.agregar_arista(x, y)
        indice += 2
    return n, r, arbol

def calcular_distancias(nodo_inicial, n):
    distancia = [-1] * n
    distancia[nodo_inicial.valor - 1] = 0
    cola = deque([nodo_inicial])
    while cola:
        nodo = cola.popleft()
        for hijo in nodo.hijos:
            if distancia[hijo.valor - 1] == -1:
                distancia[hijo.valor - 1] = distancia[nodo.valor - 1] + 1
                cola.append(hijo)
    return distancia

def hash_subarbol(nodo, padre, distancia, r):
    hijos_hash = []
    for hijo in nodo.hijos:
        if hijo != padre and distancia[hijo.valor - 1] <= r:
            hijos_hash.append(hash_subarbol(hijo, nodo, distancia, r))
    hijos_hash.sort()
    return tuple(hijos_hash)

def contar_subarboles_distintos(arbol, r):
    n = arbol.n
    subarboles_hash = set()
    for nodo in arbol.nodos:
        distancia = calcular_distancias(nodo, n)
        hash_arbol = hash_subarbol(nodo, None, distancia, r)
        subarboles_hash.add(hash_arbol)
    return len(subarboles_hash)

def visualizar_arbol():
    n, r, arbol = leer_entrada()
    arbol.visualizar_grafo_grafico("Árbol Original")
    resultado = contar_subarboles_distintos(arbol, r)
    messagebox.showinfo("Resultado", f"Número de subárboles distintos: {resultado}")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Visualización de Árboles")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_datos = tk.Label(frame, text="Introduce los datos (n, r y aristas):")
label_datos.grid(row=0, column=0, pady=5)

entry_datos = tk.Text(frame, height=10, width=30)
entry_datos.grid(row=1, column=0, pady=5)

button_visualizar = tk.Button(frame, text="Visualizar Árbol y Calcular Subárboles", command=visualizar_arbol)
button_visualizar.grid(row=2, column=0, pady=10)

# Ejemplo de uso: Introduce este texto en la interfaz:
# 7 1
# 1 2
# 1 3
# 1 4
# 1 5
# 2 6
# 2 7

root.mainloop()