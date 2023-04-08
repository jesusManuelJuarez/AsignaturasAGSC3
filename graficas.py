import matplotlib.pyplot as plt
import numpy as np
import datetime

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
        gen_contador +=1
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
    #Creamos la Grafica
    ax.plot(val_x, val_y_max, label = 'Mejores',linestyle = '-', marker = 'o')
    ax.plot(val_x, val_y_ave, label = 'Media', linestyle = "--", marker = '.')
    ax.plot(val_x, val_y_min, label = 'Peores', linestyle = "-.", marker = 'x')
    ax.set_xlabel('Generación')
    ax.set_ylabel('Aptitud')
    ax.legend()
    ax.set_title('Gráfica de la evolución de la aptitud')
    
    fecha = str(datetime.datetime.now().date())
    tiempo = str(datetime.datetime.now().strftime('%H-%M-%S'))
    
    filename = 'Gráfica aptitud ' + fecha + '--' + tiempo + '.png'

    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    fig.set_size_inches(12, 8)
    plt.savefig("./imagenes/" + filename, transparent=False, dpi=400, bbox_inches='tight')
    plt.show()


def tablas(generaciones):
    conta, gen_contador = 1, 0
    for generacion in generaciones:
        if conta == round(len(generaciones) * 0.2):
            conta = 0
            row = []
            fig, ax = plt.subplots()
            
            columns_lbl = ('Generación', 'Aptitud', 'Plan académico')

            for individuo in generacion:
                row.append([gen_contador, individuo.get_fitness(), individuo.get_lista_asignaturas()])
            ax.set_title("Generación " + str(gen_contador))
            ax.axis('off')
            tabla = ax.table(
                cellText=row,
                colLabels=columns_lbl,
                loc='center',
            )
            tabla.auto_set_font_size(False)
            tabla.set_fontsize(9)
            manager = plt.get_current_fig_manager()
            manager.window.state('zoomed')
            
            fecha = str(datetime.datetime.now().date())
            tiempo = str(datetime.datetime.now().strftime('%H-%M-%S'))
    
            filename = "Generación " + str(gen_contador)+ "_" + fecha + '--' + tiempo + '.png'

            
            fig.set_size_inches(12, 8)
            plt.savefig("./imagenes/" + filename,
                        transparent=False, dpi=400, bbox_inches='tight')
            plt.show()
            plt.close()      
        conta += 1
        gen_contador += 1