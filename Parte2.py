import random
import queue
import time

#Definimos tipos de clientes
class Cliente:
    def _init_(self, tipo, subtipo):
        self.tipo = tipo
        self.subtipo = subtipo

# cefinimos ventanillas
class Ventanilla:
    def _init_(self):
        self.ocupada = False
        self.tiempo_restante = 0

#  lista de ventanillas
N = 5  # ventanillas
ventanillas = [Ventanilla() for _ in range(N)]

# cola de clientes
cola_de_clientes = queue.PriorityQueue()

# definir prioridades para clientes
# mayor prioridad prefer
prioridades = {
    'sin tarjeta': 3,
    'con tarjeta': 2,
    'preferencial': 1 
}

#llegada de clientes
tipos_de_clientes = ['con tarjeta', 'sin tarjeta', 'preferencial']
subtipos_de_clientes = {
    'con tarjeta': ['comunes', 'personas naturales VIP', 'personas jurídicas comunes', 'personas jurídicas VIP'],
    'sin tarjeta': [None],
    'preferencial': ['mayores de 60 años', 'con deficiencia física', 'con necesidades especiales']
}

#funcionamiento de las ventanillas
#First-Come, First-Served Shortest Job First)
def atender_clientes(ventanillas, cola_de_clientes):
    for ventanilla in ventanillas:
        if not ventanilla.ocupada:
            if not cola_de_clientes.empty():
                _, cliente = cola_de_clientes.get()
                print(f"Atendiendo a cliente {cliente.tipo} {cliente.subtipo if cliente.subtipo else ''} en ventanilla {ventanillas.index(ventanilla)+1}")
                ventanilla.ocupada = True
                ventanilla.tiempo_restante = random.randint(5, 15)  
                # Tiempo que cada persona se demora en ventanilla es aleatorio con distribución uniforme
                print(f"    Tiempo de atención: {ventanilla.tiempo_restante}")
        else:
            ventanilla.tiempo_restante -= 1
            if ventanilla.tiempo_restante == 0:
                ventanilla.ocupada = False
                print(f"Ventanilla {ventanillas.index(ventanilla)+1} libre")

# Simula una ventanilla que deja de atender
def pausa_ventanilla(ventanillas):
    ventanilla = random.choice(ventanillas)
    if ventanilla.ocupada:
        print(f"Ventanilla {ventanillas.index(ventanilla)+1} deja de atender por un momento")
        ventanilla.ocupada = False
        ventanilla.tiempo_restante = random.randint(3, 8)  # La ventanilla deja de atender durante un tiempo aleatorio entre 5 y 10 unidades de tiempo
        print(f"    Tiempo que estará inactivo: {ventanilla.tiempo_restante}")

# Simulamos el paso del tiempo
for t in range(400):
    # Simulamos la llegada de clientes
    if random.random() < 0.1:  # 10% de probabilidad de que llegue un cliente en cada unidad de tiempo
        tipo = random.choice(tipos_de_clientes)
        subtipo = random.choice(subtipos_de_clientes[tipo])
        cliente = Cliente(tipo, subtipo)
        cola_de_clientes.put((prioridades[tipo], cliente))
        print(f"Llega cliente {cliente.tipo} {cliente.subtipo if cliente.subtipo else ''} en tiempo {t}")

    atender_clientes(ventanillas, cola_de_clientes)
    if random.random() < 0.05:  # 5% de probabilidad de que una ventanilla deje de atender
        # Simulación de una ventanilla fuera de servicio
        pausa_ventanilla(ventanillas)

    time.sleep(0.4)
