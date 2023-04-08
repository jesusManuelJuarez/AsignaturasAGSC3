import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib
import time
import tkinter as Tk
matplotlib.use('TkAgg')

def grafica_fitness(generaciones):
    values_x, values_y_better, values_y_worst, average = [], [], [], []
    gen_contador = 0

    for g in generaciones:
        aux = g[0]
        values_x.append(gen_contador)

        fitness_max, fitness_min, media, conta = aux, aux, 0, 0
        for i in g:
            if i > fitness_max:
                fitness_max = i
            elif i < fitness_min:
                fitness_min = i
            media += i
            conta += 1
        gen_contador += 1
        media = media / conta
        values_y_better.append(fitness_max)
        values_y_worst.append(fitness_min)
        average.append(media)

    val_x, val_y_max, val_y_min, val_y_ave = values_x, [], [], []

    for value in values_y_better:
        aux = round(float(value), 3)
        val_y_max.append(aux)

    for value in values_y_worst:
        aux = round(float(value), 3)
        val_y_min.append(aux)

    for value in average:
        aux = round(float(value), 3)
        val_y_ave.append(aux)

    fig, ax = plt.subplots()
    # Creamos la Grafica
    ax.plot(val_x, val_y_max, label='Mejores', linestyle='-', marker='o')
    ax.plot(val_x, val_y_ave, label='Media', linestyle="--", marker='.')
    ax.plot(val_x, val_y_min, label='Peores', linestyle="-.", marker='x')
    ax.set_xlabel('Generación')
    ax.set_ylabel('Aptitud')
    ax.legend()
    ax.set_title('Gráfica de la evolución de la aptitud')

    fecha = str(datetime.datetime.now().date())
    tiempo = str(datetime.datetime.now().strftime('%H-%M-%S'))

    filename = 'Gráfica aptitud ' + fecha + '--' + tiempo + '.png'

    fig.set_size_inches(12, 8)
    plt.tight_layout()

    root = Tk.Tk()
    root.withdraw()
    root.after(0, show, filename, root)
    root.mainloop()


def show(filename, root):
    plt.savefig("./imagenes/" + filename, transparent=False, dpi=400, bbox_inches='tight')
    plt.show()
    plt.close()
    time.sleep(3)
    root.destroy()