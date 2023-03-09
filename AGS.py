from Individuo import *

class AGS(object):
    # ATRIBUTOS PROPIOS DE CLASE
    num_epoch = 0
    pob_total = []
    univer_mg = []
    #  CONSTRUCTOR DE LA CLASE AGS QUE SE INICIALIZA AL SER INSTANCIADA
    def __init__(self, epoch, pc, po, cu_a, matricula, materias):
        #LIMPIAZA DE POBLACION DE INIVDUOS PARA CADA ITERACIÓN
        self.pob_total.clear()
        # PARARAMETROS DE LA INTERFAZ GRAFICA
        self.epoch = epoch
        self.pc = pc
        self.po = po
        self.cu_a = cu_a
        self.matricula = matricula
        self.materias = materias

        #EJECUTA HASTA EL NUMERO DE EPOCAS ASIGNADAS EN epoch
        while True:
            # IMPLEMETANCION DE METODOS AGS
            self.create()
            self.selection()
            self.cross()
            self.mutates()
            self.pruning()

            self.num_epoch+= 1
            if self.num_epoch ==epoch:
                break;

    # FUNCION PARA LA CREACION DE INDIVIDUOS
    def create(self):
        print("----------CREACION-------------")

    # FUNCION PARA SELECCION A LOS INVIDUOS QUE PASARAN A PROCESO DE CRUZA |PC|
    def selection(self):
        print("---------INDIVIDUOS SELECCIONADOS-------")

    # FUNCION PARA LA CRUZA
    def cross(self):
        print(".........CRUZA.........")
    # FUNCION PARA PROCESO DE MUTA
    def mutates(self):
        print("---------MUTA........")

    def pruning(self):
        print("-----PODA......")