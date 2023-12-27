import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fcfs(procesos):
    tiempo_total = 0
    gantt = []
    tiempos_espera = []

    for duracion in procesos:
        espera = max(0, tiempo_total)
        tiempo_total += duracion
        gantt.append((espera, tiempo_total, len(gantt) + 1))  # Agregar orden de llegada
        tiempos_espera.append(espera)

    return gantt, tiempos_espera

def sjf(procesos):
    procesos_ordenados = sorted(enumerate(procesos, 1), key=lambda x: x[1])
    gantt = []
    tiempos_espera = []

    tiempo_total = 0
    for proceso, duracion in procesos_ordenados:
        espera = max(0, tiempo_total)
        tiempo_total += duracion
        gantt.append((espera, tiempo_total, proceso))  # Agregar orden de llegada
        tiempos_espera.append(espera)

    return gantt, tiempos_espera

def round_robin(procesos, quantum):
    gantt = []
    tiempos_espera = []

    tiempo_total = 0
    while any(procesos):
        for i, duracion in enumerate(procesos):
            if duracion > 0:
                espera = max(0, tiempo_total)
                ejecucion = min(quantum, duracion)
                tiempo_total += ejecucion
                gantt.append((espera, tiempo_total, i + 1))  # Agregar orden de llegada
                tiempos_espera.append(espera)
                procesos[i] -= ejecucion

    return gantt, tiempos_espera

def prioritaria(procesos, prioridades):
    procesos_con_prioridad = sorted(zip(procesos, prioridades, range(1, len(procesos) + 1)), key=lambda x: (x[1], x[2]))
    gantt = []
    tiempos_espera = []

    tiempo_total = 0
    for duracion, _, orden_llegada in procesos_con_prioridad:
        espera = max(0, tiempo_total)
        tiempo_total += duracion
        gantt.append((espera, tiempo_total, orden_llegada))
        tiempos_espera.append(espera)

    return gantt, tiempos_espera

def round_robin_prioridad(procesos, prioridades, quantum):
    procesos_con_prioridad = sorted(zip(procesos, prioridades, range(1, len(procesos) + 1)), key=lambda x: (x[1], x[2]))
    gantt = []
    tiempos_espera = []

    tiempo_total = 0
    while any(procesos):
        for duracion, prioridad, orden_llegada in procesos_con_prioridad:
            if duracion > 0:
                espera = max(0, tiempo_total)
                ejecucion = min(quantum, duracion)
                tiempo_total += ejecucion
                gantt.append((espera, tiempo_total, orden_llegada))  # Agregar orden de llegada
                tiempos_espera.append(espera)
                procesos[orden_llegada - 1] -= ejecucion

    return gantt, tiempos_espera

def calcular_tiempo_promedio(tiempos_espera):
    return sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0

class PlanificadorApp:
    def _init_(self, master):
        self.master = master
        self.master.title("Planificador de Procesos")

        self.algoritmo_var = tk.StringVar()
        self.algoritmo_var.set("FCFS")  # Valor predeterminado

        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(expand=True, fill=tk.BOTH)

        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.canvas = tk.Canvas(self.canvas_frame, yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_x.config(command=self.canvas.xview)

        self.figures_frame = ttk.Frame(self.canvas)

        self.figures = []
        self.tiempo_promedio = []

        self.init_gui()

    def init_gui(self):
        tk.Label(self.master, text="Seleccionar algoritmo de planificación:").pack(pady=10)

        algoritmos = ["FCFS", "SJF", "Round Robin", "Prioritaria", "Round Robin con Prioridad"]
        for algoritmo in algoritmos:
            tk.Radiobutton(self.master, text=algoritmo, variable=self.algoritmo_var, value=algoritmo).pack(pady=5)

        tk.Button(self.master, text="Ingresar Datos", command=self.ingresar_datos).pack(pady=10)

    def ingresar_datos(self):
        algoritmo = self.algoritmo_var.get()

        procesos = self.obtener_datos("Número de procesos", "Ingrese el número de procesos:")
        if procesos is not None:
            duraciones = self.obtener_lista_datos("Duración del proceso", procesos)

            if algoritmo == "Prioritaria":
                prioridades = self.obtener_lista_datos("Prioridad del proceso", procesos)
                gantt_resultado, tiempos_espera = prioritaria(duraciones, prioridades)
            elif algoritmo == "Round Robin":
                quantum = self.obtener_dato("Quantum", "Ingrese el quantum:")
                if quantum is not None:
                    gantt_resultado, tiempos_espera = round_robin(duraciones, quantum)
            elif algoritmo == "FCFS":
                gantt_resultado, tiempos_espera = fcfs(duraciones)
            elif algoritmo == "SJF":
                gantt_resultado, tiempos_espera = sjf(duraciones)
            elif algoritmo == "Round Robin con Prioridad":
                prioridades = self.obtener_lista_datos("Prioridad del proceso", procesos)
                quantum = self.obtener_dato("Quantum", "Ingrese el quantum:")
                if quantum is not None:
                    gantt_resultado, tiempos_espera = round_robin_prioridad(duraciones, prioridades, quantum)

            tiempo_promedio = calcular_tiempo_promedio(tiempos_espera)
            self.mostrar_diagrama_gantt(gantt_resultado, tiempos_espera, tiempo_promedio, duraciones)

    def obtener_dato(self, titulo, mensaje):
        return simpledialog.askinteger(titulo, mensaje)

    def obtener_lista_datos(self, titulo, n):
        datos = []
        for i in range(n):
            dato = simpledialog.askinteger(f"{titulo} {i+1}", f"Ingrese la {titulo.lower()} del proceso P{i + 1}:")
            if dato is not None:
                datos.append(dato)
            else:
                break
        return datos

    def obtener_datos(self, titulo, mensaje):
        return simpledialog.askinteger(titulo, mensaje)

    def mostrar_diagrama_gantt(self, gantt, tiempos_espera, tiempo_promedio, procesos):
        fig, gnt = plt.subplots()

        gantt.sort(key=lambda x: x[0])  # Ordenar por orden de llegada

        gnt.set_xlim(0, gantt[-1][1])
        gnt.set_ylim(0, 2)
        gnt.set_xlabel('Tiempo')
        gnt.set_yticks([])

        for i, (inicio, fin, orden_llegada) in enumerate(gantt):
            # Agregar borde negro entre bloques
            gnt.broken_barh([(inicio, fin - inicio)], (0.4, 0.2), facecolors=('tab:blue'), edgecolor='black')

            # Mostrar etiquetas de proceso
            gnt.text(inicio + 0.5, 0.5, f'P{orden_llegada}', ha='center', va='center', color='white')

        # Establecer ticks y etiquetas en el inicio y final de todos los procesos
        finales_procesos = [0] + [fin for _, fin, _ in gantt]
        gnt.set_xticks(finales_procesos)
        gnt.set_xticklabels([str(int(tick)) for tick in finales_procesos])

        # Mostrar tiempo promedio de espera en el título
        plt.title(f'Diagrama de Gantt - {self.algoritmo_var.get()} - Tiempo Promedio de Espera: {tiempo_promedio:.2f}')

        # Añadir la figura a la lista
        self.figures.append(fig)

        # Crear un nuevo Canvas para mostrar la figura
        self.actualizar_cuadricula()

    def actualizar_cuadricula(self):
        # Limpiar el frame antes de actualizar
        for widget in self.figures_frame.winfo_children():
            widget.destroy()

        # Crear una cuadrícula de 3x3 para organizar las figuras
        row, col = 0, 0
        for i, fig in enumerate(self.figures):
            canvas = FigureCanvasTkAgg(fig, master=self.figures_frame)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Incrementar la fila y columna para el próximo gráfico
            col += 1
            if col == 3:
                col = 0
                row += 1

        # Configurar el grid para que las celdas se expandan
        self.figures_frame.grid_rowconfigure(0, weight=1)
        self.figures_frame.grid_columnconfigure(0, weight=1)

        # Empacar el frame de las figuras en el canvas
        self.canvas.create_window((0, 0), window=self.figures_frame, anchor='nw')
        self.canvas.update_idletasks()

        # Configurar el scrollbar para que funcione con la cuadrícula
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Empacar el canvas en el frame principal
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlanificadorApp(root)
    root.mainloop()
